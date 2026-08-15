# Industrial Cathodic Protection Controller

工业阴极保护恒电位控制器原型。该仓库面向真实工程学习与求职作品集，保存需求、设计、固件、测试、问题、波形和面试材料；当前只完成项目初始化，所有实验结果均为 `Not Tested`。

## 1. Project Overview

恒电位控制器测量 `Pipe Potential - Reference Electrode Potential`，并根据设定保护电位调节外部电流输出，使 `V_measured → V_set`。V0/V1 仅在不超过 24 V DC 的安全低压模型上验证弱电控制链路，不构成可连接工业强电的设备。

## 2. Project Goals

- Embedded system
- Analog front end
- ADC and PWM
- P/PI control
- Current and voltage sensing
- RS485 and Modbus RTU
- Fault diagnostics
- PCB design

## 3. Hardware Platform

| Item | Selection |
|---|---|
| MCU | STM32F103 |
| Board | STM32F103 Development Board |
| Experiment voltage | <= 24 V DC |
| Debug | SWD |
| Current communication | UART |

Planned peripherals: `ADC1_IN0` for simulated potential, `ADC1_IN1` for future current sensing, `ADC1_IN2` for future voltage sensing, `TIMx_CHx` for PWM, `USART1` for USB-UART debug, and `USART2` for future RS485.

> TODO: assign pins based on actual STM32F103 board schematic.

## 4. Project Stages

- **V0 — Principle verification:** development board, ADC/UART, PWM/RC output, dummy load, then P/PI verification.
- **V1 — Low-voltage industrial-control prototype:** reference AFE, sensing, low-voltage power stage, protection, RS485/Modbus; still <=24 V DC.
- **V2 — Standalone controller board:** minimum MCU system and validated modules integrated on PCB after module tests.

## 5. Safety Boundary

The current project must not directly connect to 220 VAC, 380 VAC, a high-voltage DC bus, or mains-derived/high-power stages. Any >24 V DC or mains concept is documentation-only Future Work.

## 6. Development Status

| Module | Status |
|---|---|
| Project structure | Initialized |
| ADC acquisition | Planned / Not Tested |
| UART debug | Planned / Not Tested |
| PWM output | Planned / Not Tested |
| Dummy load | Planned / Not Tested |
| P controller | Planned / Not Tested |
| PI controller | Interface only / Not Tested |
| Current sensing | Planned / Not Tested |
| Voltage sensing | Planned / Not Tested |
| RS485 | Planned / Not Tested |
| Modbus | Planned / Not Tested |
| PCB | Future |

## Engineering Rules

Unknown values are `TBD`; unperformed verification is `Not Tested`. GPIO assignments are not guessed. Tests must identify firmware commit and hardware version. Significant choices, problems, and pending work belong in the decision, debug, and issue logs respectively.

## Next Task

Only: **TEST-001 / Phase 1 — STM32F103 ADC voltage acquisition verification** (`potentiometer → 0–3.3 V → ADC → UART → PC`).
