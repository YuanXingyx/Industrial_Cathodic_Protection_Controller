# TEST-010-A Day 7 Host Visualization and Step Response

The `010` directory preserves the repository's existing `007_Current_Sense_Test`
numbering. This record covers Day 7 of the MVP schedule.

## Objective

Verify host-side UART acquisition, parsing, CSV logging, real-time Target/ADC
visualization, and directional closed-loop response to a setpoint step using
the stable PI baseline.

This is a minimum low-voltage closed-loop validation, not a complete industrial
cathodic-protection rectifier/controller.

## Test Setup

```text
ADC feedback → PI controller → TIM3 PWM → RC low-pass
     ↑                                      |
     └──────── PA0 / VOUT feedback ─────────┘

STM32 UART → Python host → live plot + CSV
```

## Hardware Configuration

```text
MCU: STM32F103C8T6
System clock: HSI 8 MHz
ADC: ADC1_IN0 / PA0
PWM: TIM3_CH1 / PA6
TIM3: PSC=7, ARR=999, approximately 1 kHz theoretical
UART: USART1 / 115200 / 8N1
RC: 10 kOhm + 100 uF, approximately 1 s
```

The 100 uF capacitor is a temporary test component. The planned approximately
1 uF replacement remains `Not Tested`.

## Firmware Configuration

```text
Kp: 0.010
Ki: 0.002
dt: approximately 0.1 s
base duty: 50%
integral clamp: -5000 to +5000
output clamp: 0% to 100%
```

UART format:

```text
ADC=...,TARGET=...,INT=...,ERR=...,KP=0.010,KI=0.002,OUT=...,DUTY=...
```

`OUT` is `control_output × 100`; for example, `OUT=5243` represents 52.43%.

## Host Tool Configuration

```text
Script: 03_Firmware/Host_Tools/serial_plot.py
Port: COM7
Baud: 115200
Dependencies: pyserial, matplotlib, Python standard csv/re/time modules
CSV artifact: pi_log.csv
Plot artifact: 05_Data/Figure_1.png
```

The parser accepts optional whitespace between UART fields. The CSV contains:

```text
time_s,adc,target,integral,error,kp,ki,output_x100,duty
```

The captured CSV contains 1401 data rows. This row count describes the checked
artifact and is not a performance metric.

## Step Profile

```text
Initial target: 2048
Step target: 2400
Return target: 2048
```

The firmware schedule uses 2048 for the first 10 s, 2400 until 30 s, and 2048
thereafter. These are command times, not measured settling times.

## Observations

- Python received and parsed the STM32 UART stream.
- Target and ADC were plotted in real time.
- All parsed fields, including `output_x100`, were saved to CSV.
- ADC moved in the commanded direction after the step to 2400.
- After the target returned to 2048, ADC returned toward the target.
- With `Kp=0.010`, `Ki=0.002`, the loop was stable but slow with the temporary
  10 kOhm/100 uF plant.
- A small number of isolated ADC spikes were observed. They did not form
  sustained oscillation; root cause is `TBD / not confirmed`.

Exact settling time: Not Measured.

## Parameter Comparison

| Kp | Ki | Hardware observation | Status |
|---:|---:|---|---|
| 0.010 | 0.002 | Stable baseline; response slow | PASS / retained baseline |
| approximately 0.015 | 0.002 | Sustained oscillation observed | Unstable test condition |
| 0.020 | 0.002 | Stronger sustained oscillation observed | Unstable test condition |

No additional Kp or Ki values are claimed. The formal baseline is restored to
and remains `Kp=0.010`, `Ki=0.002`; gain must not be increased without a new
controlled test.

## Result

Status: **PASS**

- Python serial receive: PASS
- UART parsing: PASS
- CSV logging: PASS
- Real-time TARGET/ADC plotting: PASS
- Step direction tracking: PASS
- Closed-loop returns toward target: PASS
- Stable baseline at Kp=0.010, Ki=0.002: PASS
- Response speed: Slow / improvement needed
- Kp approximately 0.015: Sustained oscillation observed
- Kp=0.020: Stronger sustained oscillation observed
- Isolated ADC spikes: Observed; root cause TBD
- Exact settling time: Not Measured
- 1 uF RC test: Not Tested

## Limitations / Open Issues

- The 100 uF capacitor is temporary and makes the plant slow.
- The approximately 1 uF replacement is not tested.
- Isolated ADC spike root cause is not confirmed.
- No formal settling-time calculation has been performed from the CSV.
- No true reference-electrode AFE, industrial power stage, output current/voltage
  sensing, RS485/Modbus, full protection, industrial supply, or EMC validation
  is implemented.
