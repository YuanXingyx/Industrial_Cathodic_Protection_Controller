# Signal Definition

| Signal | Meaning | V0 range/interface | Status |
|---|---|---|---|
| V_SET | Requested protection potential | TBD | Planned |
| VREF_ACTUAL | Simulated reference/pipe potential | 0–3.3 V at ADC for Phase 1 | Not Tested |
| VOUT | Low-voltage stage output feedback | TBD | Future |
| IOUT | Output current feedback | TBD | Future |
| PWM_CMD | Control output | TIMx_CHx, frequency TBD | Future |
| UART_DEBUG | Human-readable telemetry | USART1 logical assignment | Planned |

Electrical polarity, scaling, acceptable accuracy and connector assignments remain `TBD` until hardware is confirmed.
