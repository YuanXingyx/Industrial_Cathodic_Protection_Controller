# Debug Log

Create an entry only for a real observed problem; never pre-fill a root cause.

## 2026-08-26 - BUG-ADC-001 ADC full-scale reading lower than expected before calibration

### Problem

PA0 was directly connected to the STM32 3.3 V rail.

Multimeter measurements:

```text
VDD_3V3 = 3.245 V
V_PA0   = 3.245 V
```

ADC output before calibration:

```text
4030 ~ 4039
```

### Expected

```text
ADC_RAW near 4095
```

### Actual

The uncalibrated full-scale reading remained approximately 56 to 65 counts
below 4095.

### Measurement

- GND endpoint: `ADC_RAW = 0`
- 3.3 V rail and PA0: `3.245 V`
- Full-scale endpoint before calibration: `ADC_RAW ≈ 4030 ~ 4039`

### Hypothesis

The ADC initialization sequence did not perform the STM32F103 ADC calibration
step before conversions were used.

### Investigation

- Measured PA0 voltage directly.
- Confirmed no significant voltage drop between the 3.3 V rail and PA0.
- Confirmed the ADC low endpoint at GND was 0.
- Checked the ADC initialization sequence.

### Root Cause

ADC calibration had not been executed after ADC initialization.

### Fix

Added one-time startup calibration after `MX_ADC1_Init()` and before the main
loop:

```c
if (HAL_ADCEx_Calibration_Start(&hadc1) != HAL_OK)
{
  Error_Handler();
}
```

### Verification

After calibration:

```text
PA0 = 3.245 V
ADC_RAW ≈ 4093 ~ 4095
```

At GND:

```text
ADC_RAW = 0
```

### Lessons Learned

For STM32F103 ADC measurements, perform ADC calibration during initialization
before relying on measurement accuracy.

## YYYY-MM-DD - BUG-XXX

### Problem

### Expected

### Actual

### Measurement

### Hypothesis

### Investigation

### Root Cause

### Fix

### Verification

### Lessons Learned
