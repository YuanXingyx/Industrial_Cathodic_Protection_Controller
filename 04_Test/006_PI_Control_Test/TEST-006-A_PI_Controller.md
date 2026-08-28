# TEST-006-A Day 6 PI Controller

## Objective

Verify PI closed-loop operation on the STM32F103 PWM/RC/ADC feedback path,
including integral accumulation, integral reduction for negative error,
retained integral compensation at zero error, and basic integral clamping.

## Hardware Setup

```text
MCU: STM32F103C8T6
System clock: HSI 8 MHz
ADC feedback: ADC1_IN0 / PA0
PWM output: TIM3_CH1 / PA6
UART: USART1 / 115200 / 8N1
TIM3: PSC = 7, ARR = 999, PWM ≈ 1 kHz theoretical

PA6 PWM → 10 kOhm → VOUT → PA0 ADC
                        |
                      100 uF
                        |
                       GND
```

The 100 uF capacitor is a temporary test component, not the final hardware
design. With 10 kOhm, the temporary plant time constant is approximately 1 s.

## PI Algorithm

```text
error = target_raw - adc_raw
integral = integral + error × dt
control_output = base duty + Kp × error + Ki × integral
```

The firmware limits `control_output` to 0% through 100% and calculates PWM CCR
directly from the bounded floating-point output.

## Parameters

| Parameter | Value | Status |
|---|---:|---|
| target_raw | 2048 ADC counts | Tested |
| base duty | 50% | Tested |
| Kp | 0.010 | Tested |
| Ki | 0.002 | Tested |
| dt | approximately 0.1 s | Tested configuration |
| integral minimum | -5000 | Implemented |
| integral maximum | +5000 | Implemented |
| temporary R | 10 kOhm | Tested |
| temporary C | 100 uF | Tested |

Other Kp and Ki values: Not Tested.

## Integral Clamp

The current implementation clamps the stored integral state:

```text
-5000 <= integral <= 5000
```

This is a basic measure against unlimited integral accumulation. It is not a
complete advanced anti-windup implementation.

- Conditional integration: Not Implemented
- Back-calculation anti-windup: Not Implemented

## Test Procedure

1. Calibrate ADC once during initialization.
2. Start TIM3_CH1 PWM once during initialization.
3. Sample ADC feedback approximately every 100 ms.
4. Update error, integral state, bounded PI output, and PWM compare only after a
   successful ADC conversion poll.
5. Observe `ADC`, `TARGET`, `INT`, `ERR`, `KP`, `KI`, and `DUTY` over UART.
6. Allow for the slow response of the temporary 1 s RC plant.

## Observed Results

Status: **PASS**

Steady observations were generally near:

```text
ADC ≈ 2042 to 2054
ERR ≈ -6 to +6
INT ≈ 295 to 301
DUTY ≈ 51%
```

No precise settling time or statistical distribution is claimed.

## Evidence that Integral Accumulates

The observed integral state increased from approximately:

```text
INT = 111
```

to approximately:

```text
INT = 299 to 301
```

while positive error accumulated. Integral accumulation: PASS.

## Evidence that Integral Decreases for Negative Error

With a negative error, one observation showed:

```text
INT ≈ 176
ERR = -44
```

followed by an integral value near:

```text
INT ≈ 172
```

Integral decrease for negative error: PASS.

## Evidence that Error Can Reach Zero While Integral Remains Non-zero

Multiple observations included:

```text
ADC = 2048
ERR = 0
INT ≈ 296
DUTY = 51
```

At that instant, the proportional term was zero while the integral term
retained historical compensation:

```text
Ki × integral ≈ 0.002 × 296 ≈ 0.592%
control output ≈ 50% + 0% + 0.592% ≈ 50.59%
```

Rounded UART telemetry therefore displayed `DUTY=51`. Zero error with retained
integral compensation: PASS.

## Stability Observation

The PI loop remained near the target for most observed samples. Isolated ADC
values such as 1955, 2092, and 2070 were observed, followed by immediate return
near the target. No continuous large divergence or sustained oscillation was
observed.

These isolated points are recorded as possible sampling, contact, or transient
noise. Their root cause remains TBD; they are not classified as PI instability.

## Verified Outcomes

- PI loop operation: PASS
- Integral accumulation: PASS
- Integral decrease for negative error: PASS
- Zero-error with retained integral compensation: PASS
- Integral clamping implemented: PASS

## Limitations

- Other Ki values: Not Tested
- Other Kp values: Not Tested
- Precise settling time: Not Measured
- Oscilloscope waveform: Not Tested
- Approximately 1 uF RC plant: Not Tested
- Conditional integration: Not Implemented
- Back-calculation anti-windup: Not Implemented
- Python host plotting: Not Implemented

## Next Step

Day 7 / Host-side visualization and step-response logging — planned only:

- Read UART data with Python.
- Plot Target, ADC, and Duty in real time.
- Save raw data to CSV.
- Perform one setpoint step-response test.

No Day 7 implementation is included in this stage.

Hardware TODO:

Replace the temporary 100 uF capacitor with approximately 1 uF when the new
capacitor arrives. The replacement remains `Not Tested`.
