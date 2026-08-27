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

## 2026-08-27 - CTRL-DBG-001 Closed-loop overshoot caused by slow RC plant and incremental control

### Problem

The closed-loop system converged near the target but showed clear overshoot,
target crossings, and repeated correction.

### Observation

Plant:

```text
R = 10 kOhm
C = 100 uF
RC ≈ 1 s
```

Controller update:

```text
approximately 100 ms
```

Controller action:

```text
±1% duty per update outside a ±20 ADC-count deadband
```

### Analysis

The plant responded much more slowly than the controller update interval. The
incremental controller continued changing duty before the RC output had fully
responded. Delayed plant response was followed by target crossing, overshoot,
and repeated direction reversal.

### Root Cause

Primary contributing factors:

- Large RC time constant.
- Incremental controller behavior.
- Controller update interval relative to plant response.

These are recorded as contributing factors rather than a single proven root
cause.

### Verification

Real UART data showed correct control direction and eventual convergence near
`ADC_RAW = 2048`. Representative near-target readings ranged around 2043 to
2055 in the supplied samples, with duty around 51% to 52% in those samples.

### Lessons Learned

Closed-loop behavior depends not only on control direction, but also on plant
dynamics and controller timing.

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
