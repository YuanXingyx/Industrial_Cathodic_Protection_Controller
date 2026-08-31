# TEST-011-A 1 uF RC ADC Averaging

## Objective

Evaluate whether averaging eight valid ADC conversions per control update reduces isolated ADC spikes while preserving stable PI closed-loop tracking and step-response behavior.

## Hardware Setup

- MCU: STM32F103C8T6
- ADC feedback: ADC1_IN0 / PA0
- PWM output: TIM3_CH1 / PA6
- UART: USART1 / 115200 / 8N1
- RC plant: 10 kOhm + 1 uF
- RC time constant: approximately 10 ms

The 1 uF capacitor is the current low-voltage MVP test configuration. It is not presented as a final industrial hardware design.

## Static Validation Results

The 1 uF RC path was verified before adding ADC averaging:

| PWM Duty | VOUT | ADC RAW |
| --- | --- | --- |
| 25% | approximately 0.812 V | approximately 994-1008 |
| 50% | approximately 1.60-1.63 V | approximately 2000-2050 |
| 75% | approximately 2.4 V | approximately 3058-3083 |

**Static 1 uF RC validation: PASS**

With the 1 uF RC, a 100 ms control period, and single-sample ADC feedback, the PI loop tracked the fixed target near 2048 without sustained oscillation. The step direction for 2048 to 2400 and back to 2048 was also verified. Isolated ADC spikes and more visible curve variation were observed; their root cause remains TBD / not confirmed.

These baseline observations are not results of the new eight-sample averaging experiment.

## Firmware Configuration

- Target schedule: 2048 for 0-10 s, 2400 for 10-30 s, then 2048
- Base duty: 50%
- Kp: 0.010
- Ki: 0.002
- Control period and integration dt: approximately 0.1 s
- Integral clamp: -5000 to +5000
- Control output clamp: 0% to 100%
- ADC processing: arithmetic mean of up to eight valid conversions per control update

The PI update is performed only when at least one ADC conversion succeeds. Failed conversions are excluded from the average. If all eight conversions fail, the existing controller state and PWM output are retained for that cycle.

## Test Procedure

1. Build and flash the Day 8 firmware.
2. Connect the existing UART telemetry path to the Python host tool at 115200 / 8N1.
3. Record the full automatic step profile: 2048 to 2400 to 2048.
4. Compare the CSV and real-time plot with the previous 1 uF, 100 ms, single-sample ADC baseline.
5. Check isolated-spike frequency, stability, tracking direction, and return toward the target.
6. Calculate settling time only if a formal threshold and CSV-based measurement method are defined.

## Comparison with Single-Sample ADC

The eight-sample firmware completed the same `2048 -> 2400 -> 2048` step profile. Compared with the prior single-sample acquisition, the recorded curve was visibly smoother and isolated ADC spikes were reduced. No spike count, RMS value, standard deviation, or other unmeasured quantitative improvement is claimed.

## Observations

- Hardware execution of eight-sample averaging firmware: PASS
- PI steady-state stability: PASS
- Step direction tracking: PASS
- Closed-loop stability: PASS; no sustained oscillation observed
- ADC noise/spike reduction: Observed
- Return after the 2400-to-2048 step: stabilized near the target
- Response speed: Slow / improvement needed
- Exact settling time: Not Measured
- Spike root cause: Not fully confirmed

## Evidence

- CSV: `05_Data/ADC/Day8_1uF_8Sample_Step_Response.csv`
- Response plot: `05_Data/Control_Response/Day8_1uF_8Sample_Step_Response.png`

## Result

**Status: PASS**

Static 1 uF RC validation, PI steady-state operation, eight-sample ADC averaging, step-direction tracking, and closed-loop stability passed hardware verification. Eight-sample averaging visibly improved curve smoothness and reduced isolated spikes while preserving stability.

## Limitations and Open Issues

- Root cause of the isolated ADC spikes: TBD / not fully confirmed
- Eight consecutive software-triggered samples are averaged without timing separation.
- Exact settling time: Not Measured
- No oscilloscope noise or ripple measurement is available for this experiment.
- Response remains slow and requires further engineering analysis; the 20 ms control-period trial did not provide a clear speed benefit and produced more visible variation, so it was not retained.
- This remains a low-voltage minimum closed-loop validation, not a complete industrial potentiostat.
