# System Block Diagram

```text
Setpoint ───────────────────────┐
                               v
Simulated electrode -> AFE -> ADC -> STM32F103 -> PWM -> RC filter/load
                         ^          controller              |
                         └──────── measured potential <──────┘

Future monitored inputs: Vout, Iout, temperature and fault signals
```

Blocks beyond the ADC/UART Phase 1 path are conceptual and `Not Tested`.
