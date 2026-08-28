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
The current 10 kOhm/100 uF plant is temporary and responds slowly (`RC ≈ 1 s`).

PI control remains `Not Tested`.
