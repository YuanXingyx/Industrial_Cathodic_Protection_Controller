# TEST-001-A — UART Basic Output

## Purpose

在开始 ADC 采样验证前，确认 STM32F103 能通过现有 USART1 周期性输出基础测试字符串。

## Configuration

- MCU: STM32F103C8T6
- UART instance: USART1 (`huart1`)
- TX: PA9
- RX: PA10
- Baud rate: 115200
- Data bits: 8
- Parity: None
- Stop bits: 1
- Flow control: None
- Transmission method: polling `HAL_UART_Transmit`
- Period: approximately 500 ms after each transmit call
- HAL timeout: 100 ms

## Expected

USART1 outputs the following text every 500 ms:

```text
TEST-001 UART OK
```

The transmitted byte sequence includes `\r\n` and excludes the terminating `\0`.

## Firmware

TBD current commit

## Build Result

Local compile and link completed with no compiler or linker diagnostics, and
`Industrial_Potentiostat_F103.elf` was generated successfully.

The generated CubeIDE `make all` wrapper returned `Error -1` during its
secondary-output recipe after `arm-none-eabi-size` had completed. Building the
ELF target directly then returned exit code 0 (`up to date`). This is recorded
as a local command-line build-tool behavior, not as hardware verification.

## Hardware Result

PASS

Observed:
`TEST-001 UART OK` was received continuously at approximately 500 ms intervals.

Serial Configuration:

- 115200 baud
- 8 data bits
- No parity
- 1 stop bit
- No flow control

Note:

A short burst of invalid characters was observed during initial serial
connection/reset. Normal UART output was stable afterward.

## Evidence

- Serial log: TBD
- Firmware binary/commit: TBD
- Hardware wiring/photo: TBD
- Operator/date: TBD
