# TEST-002-A PWM Basic Output

## Purpose

Verify STM32F103 TIM3_CH1 PWM output on PA6.

## Configuration

```text
MCU: STM32F103C8T6
Timer: TIM3
Channel: CH1
Pin: PA6
Timer Clock: 8 MHz
PSC: 7
ARR: 999
PWM Mode: PWM Mode 1
Polarity: High
Default CCR1 after test: 500
```

## Frequency Calculation

```text
fPWM =
8,000,000 /
((7 + 1) × (999 + 1))
= 1000 Hz
```

Theoretical PWM Frequency: 1 kHz

Measured Frequency:
Not Tested

The theoretical value above is derived from the configured timer clock, PSC,
and ARR. It is not a hardware frequency measurement.

## PWM Principle

PSC controls the timer counting rate.

ARR defines the PWM period.

CCR1 defines the compare point and therefore the duty cycle.

For the current configuration:

```text
Timer Tick =
8 MHz / (PSC + 1)
= 1 MHz

PWM Period =
ARR + 1
= 1000 timer counts

PWM Frequency =
1 MHz / 1000
= 1 kHz
```

Duty-cycle relation:

```text
Duty ≈ CCR1 / (ARR + 1)
```

Example:

```text
CCR1 = 500
Duty ≈ 500 / 1000
= 50%
```

## Duty Cycle Test Results

| CCR1 | Target Duty | Hardware Result |
|---:|---:|---|
| 100 | 10% | PASS |
| 250 | 25% | PASS |
| 500 | 50% | PASS |
| 750 | 75% | PASS |
| 900 | 90% | PASS |

Measured duty cycle matched the configured target values within the resolution
of the available measurement tool. No unsupported decimal precision is claimed.

## Final Firmware State

- `HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1)` executes once after peripheral initialization.
- `__HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, 500)` leaves the default output at approximately 50% duty.
- PWM start and compare configuration are not repeated in the main loop.

## Result

Day 2 / PWM Basic Output: PASS / Completed

PWM Frequency Hardware Measurement: Not Tested

PWM RC Filter: Not Tested

PWM Analog Output: Not Tested
