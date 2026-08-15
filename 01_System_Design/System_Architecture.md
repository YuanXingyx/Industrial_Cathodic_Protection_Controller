# System Architecture

The product concept measures the pipe-to-reference potential and commands an external current so measured potential approaches its setpoint. V0 replaces the electrode, plant and power stage with safe low-voltage sources and an RC dummy load.

`simulated reference/pipe potential → protected analog input → ADC → STM32F103 → P/PI (future) → PWM/DAC concept → low-voltage stage → RC dummy load → feedback`

Measured channels planned: `Vref_actual`, `Vout`, `Iout`. Temperature and fault diagnostics are future work. UART is first; RS485 and Modbus RTU are later phase-gated work.
