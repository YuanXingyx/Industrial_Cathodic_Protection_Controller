# TEST-003-A PWM RC Filter

## Purpose

Verify conversion of PWM duty cycle into a low-frequency analog control
voltage using an RC low-pass filter.

## Hardware

```text
MCU: STM32F103C8T6
PWM: TIM3_CH1 / PA6
PWM frequency: 1 kHz theoretical
Measured VDD: 3.245 V
R: 100 kOhm
C: 100 nF
Output node: VOUT
```

Connection:

```text
PA6 PWM
   |
  100 kOhm
   |
 VOUT ---- 100 nF ---- GND
```

The multimeter red probe was connected to VOUT and the black probe to STM32
GND.

## Calculation

```text
RC = 100 kOhm × 100 nF
   = 0.01 s

fc = 1 / (2 × pi × RC)
   ≈ 15.9 Hz
```

PWM frequency: 1 kHz theoretical.

The PWM frequency is much higher than the RC cutoff frequency, so the RC
network attenuates the switching component and preserves the average voltage.

The expected DC output is:

```text
VOUT ≈ VDD × Duty
```

## Results

Theoretical values use the measured `VDD = 3.245 V`. Error is calculated as
`Measured - Theoretical`; displayed values are rounded to 0.001 V to match the
available measurement resolution.

| Duty | Theoretical VOUT | Measured VOUT | Error |
|---:|---:|---:|---:|
| 10% | 0.325 V | 0.324 V | -0.001 V |
| 25% | 0.811 V | 0.809 V | -0.002 V |
| 50% | 1.623 V | 1.620 V | -0.003 V |
| 75% | 2.434 V | 2.423 V | -0.011 V |
| 90% | 2.921 V | 2.906 V | -0.015 V |

## Conclusion

PASS

Observed VOUT increased monotonically with PWM duty cycle.

Measured output voltage closely followed:

```text
VOUT ≈ VDD × Duty
```

This verifies PWM-to-analog conversion for the MVP control path. It does not
claim true DAC accuracy.

## Limitations

Ripple:
Not Measured

Settling Time:
Not Measured

Oscilloscope Verification:
Not Tested

Load Drive Capability:
Not Tested

PWM Frequency Hardware Measurement:
Not Tested

## Final Firmware State

The default compare value is restored to `CCR1 = 500`, corresponding to an
approximately 50% duty cycle with `ARR = 999`.
