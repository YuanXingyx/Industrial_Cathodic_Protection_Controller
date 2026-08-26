# TEST-001-B ADC RAW Acquisition

## Purpose

Verify STM32F103 ADC1_IN0 raw acquisition using PA0.

## Firmware Configuration

MCU:
STM32F103C8T6

ADC:
ADC1_IN0 / PA0

Resolution:
12-bit

Trigger:
Software

Conversion:
Single channel / single conversion / polling

UART:
USART1 / 115200 / 8N1 / No Flow Control

Output period:
Approximately 500 ms

Firmware commit:
TBD current commit

## Test Cases

### Case 1 - PA0 to GND

Input:
PA0 -> GND

Expected:
ADC_RAW near 0

Actual:
ADC_RAW = 0. Continuous samples remained at 0.

Result:
PASS

### Case 2 - PA0 to 3.3V

Expected:
ADC_RAW near 4095

Input:
PA0 -> 3.245 V

Multimeter:

- VDD_3V3 = 3.245 V
- V_PA0 = 3.245 V

Before ADC calibration:
ADC_RAW approximately 4030 to 4039

After ADC calibration:
ADC_RAW approximately 4093 to 4095, with most samples at 4095

Actual:
The full-scale endpoint reached the expected near-4095 range after one-time
startup ADC calibration.

Result:
PASS

### Case 3 - Potentiometer Sweep

Setup:
Connect the 10 kOhm potentiometer ends to 3.3 V and GND, and connect the wiper
to PA0.

Expected:
ADC_RAW changes continuously from low to high as input voltage increases.

Actual:
Observed representative values:

```text
2459
2599
2940
3783
4035
```

ADC_RAW changed monotonically with potentiometer adjustment. At a fixed
position, only small LSB-level variation was observed.

Result:
PASS

## Build Result

The existing CubeIDE GNU toolchain compiled `main.c` and linked a new
`Industrial_Potentiostat_F103.elf` with no compiler or linker warnings or
errors. The ELF target recheck returned exit code 0, and `arm-none-eabi-size`
completed successfully.

The generated `make all` wrapper again returned `Error -1` in the
`default.size.stdout` secondary-output recipe after displaying the valid size
report. No firmware compile or link error was reported.

## Hardware Result

PASS

Basic ADC raw acquisition verified. Accuracy and linearity characterization
are deferred to the next ADC test and remain `Not Tested`.

## Evidence

- Raw UART log: TBD
- Hardware wiring/photo: TBD
- Firmware binary/commit: TBD
- Operator/date: TBD
