"""Quantitative step-response analysis for Industrial_Potentiostat CSV logs."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


DEFAULT_CSV = Path("05_Data/ADC/Day8_1uF_8Sample_Step_Response.csv")
SETTLING_BAND = 20.0
SETTLING_HOLD_S = 2.0
STEADY_WINDOW_S = 5.0
SPIKE_WINDOW = 5
SPIKE_THRESHOLD = 50.0
REQUIRED_FIELDS = (
    "time_s",
    "adc",
    "target",
    "integral",
    "error",
    "kp",
    "ki",
    "output_x100",
    "duty",
)
MCU_TICK_FIELD = "mcu_tick_ms"
UINT32_MODULUS = 1 << 32


@dataclass(frozen=True)
class Sample:
    host_time_s: float
    time_s: float
    mcu_tick_ms: int | None
    adc: float
    target: int
    integral: float
    error: float
    kp: float
    ki: float
    output_x100: float
    duty: float


@dataclass(frozen=True)
class Plateau:
    start: int
    end: int
    target: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze target steps and steady-state behavior in a UART CSV log."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        type=Path,
        default=DEFAULT_CSV,
        help=f"input CSV (default: {DEFAULT_CSV.as_posix()})",
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        help="also write the analysis as a Markdown report",
    )
    return parser.parse_args()


def load_samples(path: Path) -> tuple[list[Sample], list[str], str]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        missing = [field for field in REQUIRED_FIELDS if field not in fields]
        if missing:
            raise ValueError(f"missing required CSV fields: {', '.join(missing)}")

        use_mcu_tick = MCU_TICK_FIELD in fields
        samples: list[Sample] = []
        first_unwrapped_tick: int | None = None
        previous_tick: int | None = None
        tick_epoch = 0
        for line_number, row in enumerate(reader, start=2):
            try:
                values = [float(row[field]) for field in REQUIRED_FIELDS]
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid numeric value at CSV line {line_number}") from exc
            if not all(math.isfinite(value) for value in values):
                raise ValueError(f"non-finite numeric value at CSV line {line_number}")
            host_time_s = float(row["time_s"])
            mcu_tick_ms: int | None = None
            analysis_time_s = host_time_s
            if use_mcu_tick:
                try:
                    mcu_tick_ms = int(row[MCU_TICK_FIELD])
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"invalid MCU tick at CSV line {line_number}") from exc
                if not 0 <= mcu_tick_ms < UINT32_MODULUS:
                    raise ValueError(f"MCU tick outside uint32 range at CSV line {line_number}")
                if previous_tick is not None and mcu_tick_ms < previous_tick:
                    if previous_tick - mcu_tick_ms > UINT32_MODULUS // 2:
                        tick_epoch += UINT32_MODULUS
                    else:
                        raise ValueError(f"MCU tick moved backward at CSV line {line_number}")
                unwrapped_tick = tick_epoch + mcu_tick_ms
                if first_unwrapped_tick is None:
                    first_unwrapped_tick = unwrapped_tick
                analysis_time_s = (unwrapped_tick - first_unwrapped_tick) / 1000.0
                previous_tick = mcu_tick_ms
            samples.append(
                Sample(
                    host_time_s=host_time_s,
                    time_s=analysis_time_s,
                    mcu_tick_ms=mcu_tick_ms,
                    adc=float(row["adc"]),
                    target=int(row["target"]),
                    integral=float(row["integral"]),
                    error=float(row["error"]),
                    kp=float(row["kp"]),
                    ki=float(row["ki"]),
                    output_x100=float(row["output_x100"]),
                    duty=float(row["duty"]),
                )
            )

    if not samples:
        raise ValueError("CSV contains no data rows")
    if any(current.host_time_s <= previous.host_time_s for previous, current in zip(samples, samples[1:])):
        raise ValueError("host time_s must be strictly increasing")
    if any(current.time_s <= previous.time_s for previous, current in zip(samples, samples[1:])):
        raise ValueError("selected analysis time must be strictly increasing")
    if any(sample.error != sample.target - sample.adc for sample in samples):
        raise ValueError("logged error is inconsistent with target - adc")
    return samples, fields, "MCU TICK" if use_mcu_tick else "Host time_s"


def find_plateaus(samples: Sequence[Sample]) -> list[Plateau]:
    plateaus: list[Plateau] = []
    start = 0
    for index in range(1, len(samples)):
        if samples[index].target != samples[index - 1].target:
            plateaus.append(Plateau(start, index, samples[start].target))
            start = index
    plateaus.append(Plateau(start, len(samples), samples[start].target))
    return plateaus


def settling_time(samples: Sequence[Sample], start: int, end: int) -> float | None:
    for candidate in range(start, end):
        candidate_time = samples[candidate].time_s
        hold_reached = False
        for index in range(candidate, end):
            sample = samples[index]
            if abs(sample.adc - sample.target) > SETTLING_BAND:
                break
            if sample.time_s - candidate_time >= SETTLING_HOLD_S:
                hold_reached = True
                break
        if hold_reached:
            return candidate_time - samples[start].time_s
    return None


def analyze_steps(samples: Sequence[Sample], plateaus: Sequence[Plateau]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for number, plateau in enumerate(plateaus[1:], start=1):
        previous_target = plateaus[number - 1].target
        final_target = plateau.target
        window = samples[plateau.start : plateau.end]
        adc_values = [sample.adc for sample in window]
        errors = [sample.target - sample.adc for sample in window]
        upward = final_target > previous_target
        peak = max(adc_values)
        minimum = min(adc_values)
        if upward:
            overshoot = max(0.0, peak - final_target)
            undershoot = max(0.0, previous_target - minimum)
        else:
            overshoot = max(0.0, final_target - minimum)
            undershoot = max(0.0, peak - previous_target)
        results.append(
            {
                "number": number,
                "step_time": samples[plateau.start].time_s,
                "previous_target": previous_target,
                "new_target": final_target,
                "amplitude": final_target - previous_target,
                "initial_adc": samples[plateau.start - 1].adc,
                "settling_time": settling_time(samples, plateau.start, plateau.end),
                "peak_adc": peak,
                "minimum_adc": minimum,
                "overshoot": overshoot,
                "undershoot": undershoot,
                "max_abs_error": max(abs(error) for error in errors),
                "mean_abs_error": statistics.fmean(abs(error) for error in errors),
            }
        )
    return results


def analyze_plateaus(samples: Sequence[Sample], plateaus: Sequence[Plateau]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for number, plateau in enumerate(plateaus, start=1):
        plateau_end_time = (
            samples[plateau.end].time_s
            if plateau.end < len(samples)
            else samples[plateau.end - 1].time_s
        )
        cutoff = max(samples[plateau.start].time_s, plateau_end_time - STEADY_WINDOW_S)
        window = [sample for sample in samples[plateau.start : plateau.end] if sample.time_s >= cutoff]
        adc_values = [sample.adc for sample in window]
        errors = [sample.target - sample.adc for sample in window]
        results.append(
            {
                "number": number,
                "target": plateau.target,
                "start_time": samples[plateau.start].time_s,
                "end_time": samples[plateau.end - 1].time_s,
                "window_duration": window[-1].time_s - window[0].time_s,
                "sample_count": len(window),
                "mean_adc": statistics.fmean(adc_values),
                "mean_error": statistics.fmean(errors),
                "mean_abs_error": statistics.fmean(abs(error) for error in errors),
                "std_adc": statistics.pstdev(adc_values),
                "min_adc": min(adc_values),
                "max_adc": max(adc_values),
                "max_abs_error": max(abs(error) for error in errors),
            }
        )
    return results


def analyze_spikes(samples: Sequence[Sample]) -> dict[str, float | int]:
    radius = SPIKE_WINDOW // 2
    count = 0
    assessed = 0
    for index in range(radius, len(samples) - radius):
        local = [sample.adc for sample in samples[index - radius : index + radius + 1]]
        assessed += 1
        if abs(samples[index].adc - statistics.median(local)) > SPIKE_THRESHOLD:
            count += 1
    return {
        "count": count,
        "assessed": assessed,
        "percentage": 100.0 * count / assessed if assessed else 0.0,
    }


def analyze_timing(samples: Sequence[Sample]) -> dict[str, float | int]:
    intervals = [current.time_s - previous.time_s for previous, current in zip(samples, samples[1:])]
    return {
        "minimum": min(intervals),
        "median": statistics.median(intervals),
        "mean": statistics.fmean(intervals),
        "maximum": max(intervals),
        "below_50_ms": sum(interval < 0.050 for interval in intervals),
        "at_least_200_ms": sum(interval >= 0.200 for interval in intervals),
    }


def terminal_report(
    path: Path,
    fields: Sequence[str],
    samples: Sequence[Sample],
    steps: Sequence[dict[str, object]],
    plateaus: Sequence[dict[str, object]],
    spikes: dict[str, float | int],
    timing: dict[str, float | int],
    time_source: str,
) -> str:
    lines = [
        f"Source: {path.as_posix()}",
        f"Rows: {len(samples)}",
        f"Fields: {', '.join(fields)}",
        f"Time source: {time_source}",
        "",
    ]
    for step in steps:
        settled = step["settling_time"]
        settling_text = "Not Settled" if settled is None else f"{settled:.3f} s"
        lines.extend(
            [
                f"=== Step {step['number']} ===",
                f"Step: {step['previous_target']} -> {step['new_target']}",
                f"Step time: {step['step_time']:.3f} s",
                f"Step amplitude: {step['amplitude']} counts",
                f"Initial ADC: {step['initial_adc']:.0f}",
                f"Final target: {step['new_target']}",
                f"Settling time: {settling_text}",
                f"Peak ADC: {step['peak_adc']:.0f}",
                f"Minimum ADC: {step['minimum_adc']:.0f}",
                f"Overshoot: {step['overshoot']:.0f} counts",
                f"Undershoot: {step['undershoot']:.0f} counts",
                f"Maximum absolute error: {step['max_abs_error']:.0f} counts",
                f"Mean absolute error: {step['mean_abs_error']:.3f} counts",
                "",
            ]
        )
    for plateau in plateaus:
        lines.extend(
            [
                f"=== Plateau {plateau['number']}: TARGET={plateau['target']} ===",
                f"Plateau range: {plateau['start_time']:.3f} to {plateau['end_time']:.3f} s",
                f"Analysis window: final {plateau['window_duration']:.3f} s ({plateau['sample_count']} samples)",
                f"Mean ADC: {plateau['mean_adc']:.3f}",
                f"Mean error: {plateau['mean_error']:.3f} counts",
                f"Mean absolute error: {plateau['mean_abs_error']:.3f} counts",
                f"ADC standard deviation: {plateau['std_adc']:.3f} counts",
                f"Minimum ADC: {plateau['min_adc']:.0f}",
                f"Maximum ADC: {plateau['max_adc']:.0f}",
                f"Maximum absolute error: {plateau['max_abs_error']:.0f} counts",
                "",
            ]
        )
    lines.extend(
        [
            "=== Timestamp Quality ===",
            f"Interval min / median / mean / max: {timing['minimum']:.6f} / {timing['median']:.6f} / {timing['mean']:.6f} / {timing['maximum']:.6f} s",
            f"Intervals below 50 ms: {timing['below_50_ms']}",
            f"Intervals at least 200 ms: {timing['at_least_200_ms']}",
            f"Intervals use the selected analysis time source: {time_source}.",
            "",
            "=== Exploratory Spike Metric ===",
            f"Candidates: {spikes['count']} / {spikes['assessed']} ({spikes['percentage']:.3f}%)",
            f"Definition: abs(adc - centered rolling median[{SPIKE_WINDOW}]) > {SPIKE_THRESHOLD:.0f} counts",
            "Exploratory only; threshold is not an industrial acceptance criterion.",
        ]
    )
    return "\n".join(lines)


def markdown_report(
    source: Path,
    fields: Sequence[str],
    samples: Sequence[Sample],
    steps: Sequence[dict[str, object]],
    plateaus: Sequence[dict[str, object]],
    spikes: dict[str, float | int],
    timing: dict[str, float | int],
    time_source: str,
) -> str:
    lines = [
        "# TEST-012-A Day 8 CSV Quantitative Analysis",
        "",
        "## Objective",
        "",
        "Establish a repeatable, transparent quantitative evaluation of the recorded Day 8 PI step response without changing firmware or controller gains.",
        "",
        "## Source Data",
        "",
        f"- File: `{source.as_posix()}`",
        f"- Rows: {len(samples)}",
        f"- Fields: `{', '.join(fields)}`",
        f"- Time source: `{time_source}`",
        "- Original samples are analyzed without removing spikes or trimming the capture.",
        "",
        "## Metric Definitions",
        "",
        "- Step boundaries are detected from changes in the `target` column, not hard-coded timestamps.",
        "- Error is recomputed as `target - adc` and checked against the logged `error` field.",
        "- Step statistics use samples from the detected target change up to, but not including, the next target change; the final step uses data through the end of the CSV.",
        "- Overshoot is excursion beyond the new target in the commanded direction.",
        "- Undershoot is excursion beyond the previous target opposite the commanded direction.",
        "- Plateau statistics use the final five seconds of each target plateau, or all available data when shorter.",
        "- Standard deviation is the population standard deviation of raw ADC samples in the selected plateau window.",
        "",
        "## Settling Criterion",
        "",
        "`|ADC - TARGET| <= 20 counts` continuously for at least `2.0 s`.",
        "",
        "Settling time starts at the detected target-change sample. The qualifying hold window cannot cross the next target step. This is a project evaluation criterion, not an industrial cathodic-protection acceptance standard.",
        "",
        "## Detected Steps and Quantitative Results",
        "",
        "| Step | Time (s) | Transition | Amplitude | Initial ADC | Settling time | Peak ADC | Min ADC | Overshoot | Undershoot | Max abs error | Mean abs error |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for step in steps:
        settling = "Not Settled" if step["settling_time"] is None else f"{step['settling_time']:.3f} s"
        lines.append(
            f"| {step['number']} | {step['step_time']:.3f} | {step['previous_target']} -> {step['new_target']} | "
            f"{step['amplitude']} | {step['initial_adc']:.0f} | {settling} | {step['peak_adc']:.0f} | "
            f"{step['minimum_adc']:.0f} | {step['overshoot']:.0f} | {step['undershoot']:.0f} | "
            f"{step['max_abs_error']:.0f} | {step['mean_abs_error']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Steady-State Statistics",
            "",
            "| Plateau | Target | Data range (s) | Window (s) | Samples | Mean ADC | Mean error | Mean abs error | ADC std | Min ADC | Max ADC | Max abs error |",
            "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for plateau in plateaus:
        lines.append(
            f"| {plateau['number']} | {plateau['target']} | {plateau['start_time']:.3f}-{plateau['end_time']:.3f} | "
            f"{plateau['window_duration']:.3f} | {plateau['sample_count']} | {plateau['mean_adc']:.3f} | "
            f"{plateau['mean_error']:.3f} | {plateau['mean_abs_error']:.3f} | {plateau['std_adc']:.3f} | "
            f"{plateau['min_adc']:.0f} | {plateau['max_adc']:.0f} | {plateau['max_abs_error']:.0f} |"
        )
    lines.extend(
        [
            "",
            "## Exploratory Spike Metric",
            "",
            f"- Candidate definition: `abs(adc - centered rolling median[{SPIKE_WINDOW}]) > {SPIKE_THRESHOLD:.0f} counts`",
            f"- Candidates: {spikes['count']} of {spikes['assessed']} assessed samples ({spikes['percentage']:.3f}%)",
            "- Exploratory only; threshold is not an industrial acceptance criterion.",
            "- Candidate detection does not establish spike root cause.",
            "",
            "## Data Quality and Limitations",
            "",
            "- Required fields were present, numeric values were finite, timestamps were strictly increasing, and logged error matched `target - adc`.",
            f"- Recorded interval min/median/mean/max: {timing['minimum']:.6f}/{timing['median']:.6f}/{timing['mean']:.6f}/{timing['maximum']:.6f} s.",
            f"- {timing['below_50_ms']} intervals were below 50 ms and {timing['at_least_200_ms']} were at least 200 ms. Host buffering or capture gaps may therefore affect time-window sample weighting.",
            f"- Metric time source: `{time_source}`. MCU tick is normalized to the first captured tick when present; otherwise host `time_s` is used directly.",
            "- The uint32 MCU tick is unwrapped across a normal rollover. Day 10's short capture is not expected to reach the approximately 49.7-day rollover interval.",
            "- Raw spike candidates remain in all step and plateau calculations.",
            "- The settling threshold and hold duration are project-defined, not an industrial acceptance standard.",
            "- This single capture does not isolate ADC noise, contact noise, timing jitter, or plant/controller effects.",
            "",
            "## Conclusion",
            "",
            "The analysis converts the Day 8 qualitative observations into reproducible step, settling, error, plateau, and exploratory spike metrics. Results describe this recorded low-voltage MVP run only and do not establish industrial cathodic-protection performance.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    samples, fields, time_source = load_samples(args.csv_path)
    plateau_ranges = find_plateaus(samples)
    if len(plateau_ranges) < 2:
        raise ValueError("no target steps detected")
    steps = analyze_steps(samples, plateau_ranges)
    plateaus = analyze_plateaus(samples, plateau_ranges)
    spikes = analyze_spikes(samples)
    timing = analyze_timing(samples)
    print(terminal_report(args.csv_path, fields, samples, steps, plateaus, spikes, timing, time_source))
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(
            markdown_report(args.csv_path, fields, samples, steps, plateaus, spikes, timing, time_source),
            encoding="utf-8",
        )
        print(f"\nMarkdown report written: {args.markdown.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
