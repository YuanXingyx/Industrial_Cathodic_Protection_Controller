# TEST-005-A Day 5 P Controller

## Objective

Verify a true proportional controller with base-duty bias on the existing
STM32F103 PWM/RC/ADC feedback path, and distinguish it from the Day 4 deadband
incremental controller.

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

The 100 uF capacitor is a temporary test component, not the final plant
design. Its approximate time constant with 10 kOhm is 1 s.

## Control Algorithm

Day 4 used a **Deadband Incremental Controller** that moved duty by ±1% outside
a deadband.

Day 5 uses a **True P Controller with base-duty bias**:

```text
Error = Target - Measured
P correction = Kp × Error
Control Output = Base Duty + P correction
```

The implemented control output is limited to 0% through 100%.

## Key Equations

```text
error = target_raw - adc_raw
control_output = 50.0 + Kp × error
```

PWM compare is calculated directly from the floating-point control output:

```text
compare = round((ARR + 1) × control_output / 100)
compare <= ARR
```

The firmware does not first truncate `control_output` to an integer duty before
calculating CCR.

## Parameters

| Parameter | Value | Status |
|---|---:|---|
| target_raw | 2048 ADC counts | Tested |
| base duty | 50% | Tested |
| Kp | 0.01 | Tested |
| control update | approximately 100 ms | Tested configuration |
| temporary R | 10 kOhm | Tested |
| temporary C | 100 uF | Tested |

Other Kp values: Not Tested.

## Test Procedure

1. Calibrate ADC once during initialization.
2. Start TIM3_CH1 PWM once during initialization.
3. Read ADC feedback from PA0.
4. Calculate error and the bounded P output.
5. Calculate CCR directly from the bounded floating-point output.
6. Transmit ADC, target, error, Kp label, and rounded duty over UART.
7. Allow several seconds or longer for the temporary slow RC plant to approach
   steady behavior before interpreting samples.

## Observed Results

### P-Control Run

With `target_raw = 2048`, `Kp = 0.01`, and 50% base duty, the closed-loop
feedback direction was correct:

```text
ADC below target → positive error → control output increases → PWM increases
ADC above target → negative error → control output decreases → PWM decreases
```

One steady P-control observation showed approximately:

```text
ADC: 1983 to 1994
TARGET: 2048
ERR: approximately 54 to 65
UART DUTY: approximately 51%
```

This observation demonstrates stable P-control operation but is not claimed as
a universal or fixed 60-count steady-state error.

### Fixed 50% Baseline Diagnostic

P control was temporarily disabled for a separate 50% duty baseline check.
Later stable observations were approximately:

```text
ADC: 2056 to 2065
Duty: 50%
VOUT measured by multimeter: approximately 1.599 V
```

A brief `ADC ≈ 2200` value was observed during an abnormal/transient state and
is not treated as the final steady result.

The final firmware is restored to P control; fixed 50% duty is not the Day 5
control strategy.

## Issues Found

1. The temporary 100 uF capacitor creates an approximately 1 s plant time
   constant, so experiments require several seconds or longer to settle.
2. Calculating CCR through an integer duty introduced unnecessary quantization:
   a value such as 49.99% became 49% before compare calculation.
3. P-only behavior may retain an offset depending on actual plant gain,
   hardware conditions, and the selected base-duty bias.

## Fixes

CCR is now calculated directly from the bounded floating-point
`control_output`, with rounding and an ARR limit. Integer `duty` is retained
only as rounded UART telemetry.

## Engineering Interpretation

Result: **PASS**

- True P control with base-duty bias ran stably on the hardware loop.
- Feedback direction was correct.
- The result is consistent with the possibility of P-only steady-state offset.
- The baseline diagnostic shows that observed offset depends on the real plant
  and bias, so a fixed 60-count error is not claimed.

## Limitations

- Precise convergence time: Not Measured
- Oscilloscope waveform: Not Tested
- Step-response characterization: Not Tested
- Additional Kp sweep: Not Tested
- Approximately 1 uF replacement plant: Not Tested
- PI Controller: Not Tested

## Next Step

Day 6 / PI Controller — planned only, not implemented:

- Add the integral term.
- Observe whether steady-state offset decreases further.
- Add integral limiting/basic anti-windup protection.

Hardware TODO:

Replace the temporary 100 uF capacitor with approximately 1 uF when the new
capacitor arrives. The replacement configuration remains `Not Tested`.
