# Control Loop

The controlled variable is simulated pipe-to-reference potential. The manipulated variable will be a bounded low-voltage output command. Sign convention, plant gain and sample time are `TBD` and must be measured before enabling a controller.

Development order: open-loop acquisition → PWM characterization → RC plant characterization → bounded P → bounded PI. The PI code present in this repository is an inactive interface skeleton, not a validated control algorithm.

## Verified Controller Progression

- **Day 4:** Deadband Incremental Controller. It adjusted duty by ±1% outside
  a ±20-count deadband. This was not a P controller.
- **Day 5:** True P Controller with base-duty bias, verified with
  `target_raw = 2048`, `base duty = 50%`, and `Kp = 0.01`.

```text
error = target_raw - adc_raw
control_output = 50% + Kp × error
```

The output is limited to 0% through 100%. PWM CCR is calculated directly from
the bounded floating-point output to avoid early 1% integer-duty quantization.

- **Day 6:** PI Controller with integral clamping, verified with
  `Kp = 0.010`, `Ki = 0.002`, and `dt ≈ 0.1 s`.

```text
integral = integral + error × dt
control_output = 50% + Kp × error + Ki × integral
```

The integral state is clamped to `[-5000, +5000]`. This prevents unlimited
state accumulation but is not full anti-windup; conditional integration and
back-calculation are not implemented.

The I term supplies retained compensation for long-lived error. Therefore the
instantaneous error can be zero while the integral remains non-zero and holds a
non-50% control output.

The original 10 kOhm/100 uF temporary plant (`RC ≈ 1 s`) was replaced by a
10 kOhm/1 uF test plant. Static 25%, 50%, and 75% PWM-to-feedback points passed
hardware verification.

## Day 7 Validation Evidence

The stable baseline remains `Kp=0.010`, `Ki=0.002`, with approximately 0.1 s
control updates, ±5000 integral clamp, and 0% to 100% output clamp. A host-side
Python tool parses ADC, Target, Integral, Error, gains, output×100, and Duty;
it plots Target/ADC and stores CSV data.

The tested step profile was `2048 → 2400 → 2048`. Feedback moved in the command
direction and returned toward the original target. Exact settling time was not
measured.

Gain comparison showed a practical stability trade-off on the temporary plant:

- `Kp=0.010`, `Ki=0.002`: stable but slow; retained baseline.
- `Kp≈0.015`, `Ki=0.002`: sustained oscillation observed.
- `Kp=0.020`, `Ki=0.002`: stronger sustained oscillation observed.

Isolated ADC spikes were observed but did not form sustained oscillation; root
cause remains TBD. This evidence validates only the low-voltage minimum closed
loop, not a complete industrial cathodic-protection system.

## Day 8 ADC Averaging Validation

The retained baseline is `Kp=0.010`, `Ki=0.002`, `dt≈0.1 s`, and an approximately
100 ms control update. Each update attempts eight software-triggered ADC
conversions, excludes failed conversions, and uses `adc_sum / adc_count`. The PI
and PWM states are not updated if no conversion succeeds.

The hardware completed the `2048 -> 2400 -> 2048` profile without sustained
oscillation. Compared with single-sample feedback, the measured curve was
visibly smoother and isolated ADC spikes were reduced. Their root cause is not
fully confirmed. Response remained slow, and exact settling time was not
measured. A tested 20 ms control period showed more visible variation without a
clear response-speed benefit, so it was not retained.

This averaging is a practical MVP acquisition improvement, not a claim of a
production industrial filtering or EMC solution.
