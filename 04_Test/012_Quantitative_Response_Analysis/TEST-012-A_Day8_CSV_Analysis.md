# TEST-012-A Day 8 CSV Quantitative Analysis

## Objective

Establish a repeatable, transparent quantitative evaluation of the recorded Day 8 PI step response without changing firmware or controller gains.

## Source Data

- File: `05_Data/ADC/Day8_1uF_8Sample_Step_Response.csv`
- Rows: 2370
- Fields: `time_s, adc, target, integral, error, kp, ki, output_x100, duty`
- Original samples are analyzed without removing spikes or trimming the capture.

## Metric Definitions

- Step boundaries are detected from changes in the `target` column, not hard-coded timestamps.
- Error is recomputed as `target - adc` and checked against the logged `error` field.
- Step statistics use samples from the detected target change up to, but not including, the next target change; the final step uses data through the end of the CSV.
- Overshoot is excursion beyond the new target in the commanded direction.
- Undershoot is excursion beyond the previous target opposite the commanded direction.
- Plateau statistics use the final five seconds of each target plateau, or all available data when shorter.
- Standard deviation is the population standard deviation of raw ADC samples in the selected plateau window.

## Settling Criterion

`|ADC - TARGET| <= 20 counts` continuously for at least `2.0 s`.

Settling time starts at the detected target-change sample. The qualifying hold window cannot cross the next target step. This is a project evaluation criterion, not an industrial cathodic-protection acceptance standard.

## Detected Steps and Quantitative Results

| Step | Time (s) | Transition | Amplitude | Initial ADC | Settling time | Peak ADC | Min ADC | Overshoot | Undershoot | Max abs error | Mean abs error |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 10.991 | 2048 -> 2400 | 352 | 2030 | Not Settled | 2325 | 2032 | 0 | 16 | 368 | 157.250 |
| 2 | 31.049 | 2400 -> 2048 | -352 | 2302 | 58.744 s | 2313 | 2033 | 15 | 0 | 265 | 16.100 |

## Steady-State Statistics

| Plateau | Target | Data range (s) | Window (s) | Samples | Mean ADC | Mean error | Mean abs error | ADC std | Min ADC | Max ADC | Max abs error |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2048 | 0.000-10.882 | 4.861 | 46 | 2027.978 | 20.022 | 20.022 | 3.326 | 2021 | 2035 | 27 |
| 2 | 2400 | 10.991-30.941 | 4.795 | 45 | 2298.022 | 101.978 | 101.978 | 9.763 | 2274 | 2325 | 126 |
| 3 | 2048 | 31.049-256.702 | 4.980 | 244 | 2047.668 | 0.332 | 5.020 | 6.821 | 2035 | 2068 | 20 |

## Exploratory Spike Metric

- Candidate definition: `abs(adc - centered rolling median[5]) > 50 counts`
- Candidates: 4 of 2366 assessed samples (0.169%)
- Exploratory only; threshold is not an industrial acceptance criterion.
- Candidate detection does not establish spike root cause.

## Data Quality and Limitations

- Required fields were present, numeric values were finite, timestamps were strictly increasing, and logged error matched `target - adc`.
- Recorded interval min/median/mean/max: 0.011003/0.108050/0.108359/22.472988 s.
- 240 intervals were below 50 ms and 2 were at least 200 ms. Host buffering or capture gaps may therefore affect time-window sample weighting.
- Host timestamps are used directly as required; CSV capture start and MCU reset are not assumed to be synchronized.
- Raw spike candidates remain in all step and plateau calculations.
- The settling threshold and hold duration are project-defined, not an industrial acceptance standard.
- This single capture does not isolate ADC noise, contact noise, timing jitter, or plant/controller effects.

## Conclusion

The analysis converts the Day 8 qualitative observations into reproducible step, settling, error, plateau, and exploratory spike metrics. Results describe this recorded low-voltage MVP run only and do not establish industrial cathodic-protection performance.
