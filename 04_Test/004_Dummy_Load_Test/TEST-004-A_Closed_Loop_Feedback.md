# TEST-004-A Closed-Loop Feedback

## Purpose

Verify the minimum closed-loop control path:

```text
Setpoint
→ Error
→ PWM Duty
→ RC Plant
→ VOUT
→ ADC Feedback
→ Controller
```

## Hardware

```text
MCU: STM32F103C8T6
ADC: PA0 / ADC1_IN0
PWM: PA6 / TIM3_CH1
PWM frequency: approximately 1 kHz theoretical
UART: USART1 / 115200 / 8N1
RC Plant: 10 kOhm + 100 uF
RC time constant: approximately 1 s
Feedback: VOUT → PA0
Target: ADC_RAW = 2048
Control update: approximately 100 ms
```

## Controller

Accurate algorithm name:

```text
Deadband Incremental Controller
```

This is not a proportional (P) controller.

Control rule:

```text
error > +20   → duty +1%
error < -20   → duty -1%
|error| <= 20 → duty unchanged
```

The timer compare value is updated as:

```text
CCR1 = duty × 10
```

## Observations

The test began with feedback above the target:

```text
ADC ≈ 3061
TARGET = 2048
ERR ≈ -1013
DUTY = 49%
```

The controller correctly reduced duty from approximately 49% toward 36%.
During that interval, representative ADC samples decreased through:

```text
3061, 2813, 2731, 2665, 2605, 2533, 2464,
2416, 2345, 2285, 2223, 2175, 2118, 2070
```

Because the RC plant continued responding after duty had been reduced, the
feedback crossed below the target. Representative samples included:

```text
2015, 1983, 1937, 1906, 1897, 1870, 1857, 1855, 1849
```

The error then became positive and the controller reversed direction,
increasing duty from approximately 36% toward 57%. Repeated correction and
target crossings were observed before the system remained near the target.

Representative near-target samples:

```text
ADC=2051,TARGET=2048,ERR=-3,DUTY=52
ADC=2047,TARGET=2048,ERR=1,DUTY=52
ADC=2055,TARGET=2048,ERR=-7,DUTY=52
ADC=2046,TARGET=2048,ERR=2,DUTY=52
ADC=2047,TARGET=2048,ERR=1,DUTY=52
ADC=2045,TARGET=2048,ERR=3,DUTY=52
ADC=2043,TARGET=2048,ERR=5,DUTY=51
ADC=2047,TARGET=2048,ERR=1,DUTY=51
```

Observed final duty values near the target were approximately 48% to 52% in
the available samples. No precise steady-state statistics are claimed.

## Result

PASS

- Closed-loop direction: PASS
- Target convergence: PASS
- Feedback path: PASS
- PWM control response: PASS

The STM32 adjusted PWM duty automatically from ADC feedback. The control
direction was correct: feedback above target reduced duty, and feedback below
target increased duty. The system eventually remained near `ADC_RAW = 2048`.

## Limitations

- True P Controller: Not Implemented
- PI Controller: Not Implemented
- Step Response Characterization: Not Tested
- Python Host Plotting: Not Implemented
- Precise overshoot and settling statistics: Not Measured
