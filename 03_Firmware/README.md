# Firmware

Target: STM32F103 development board. Phase 1 is only `potentiometer → ADC → UART → PC`, with telemetry at approximately 2–10 Hz:

```text
ADC_RAW = xxxx
VDDA = x.xxx V
VIN = x.xxx V
```

Planned module APIs include `adc_measurement_init`, `adc_measurement_read_raw`, `adc_measurement_get_voltage`, `uart_debug_init`, and `uart_debug_printf`. Hardware/HAL binding is intentionally absent until the actual board, clock and project generator setup are confirmed.

TODO: assign pins based on actual STM32F103 board schematic.

The PI interface is an inactive skeleton. It must not be enabled until ADC, PWM, filter and dummy-load characterization are complete.
