# Industrial Cathodic Protection Controller

工业阴极保护恒电位控制器原型。该仓库面向真实工程学习与求职作品集，保存需求、设计、固件、测试、问题、波形和面试材料。当前已完成 Day 1 UART 与 ADC RAW 基础硬件验证；其余实验状态按模块记录。

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

## Current Focus

Current milestone: **3–7 Day Cathodic Protection Control Loop MVP**

完成标准：

```text
Setpoint
   ↓
STM32 Control
   ↓
PWM
   ↓
RC / Dummy Load
   ↓
ADC Feedback
   ↓
PI Controller
   ↓
Measured value converges to setpoint
```

PC 端能够实时显示：

- Setpoint
- Measured
- Control Output

本阶段只包含 ADC/UART、PWM/RC、简单 Dummy Load、P/PI 和 PC 实时曲线。详细执行顺序见 [MVP 7-Day Plan](00_Project_Management/MVP_7Day_Plan.md)。

## 5. Safety Boundary

The current project must not directly connect to 220 VAC, 380 VAC, a high-voltage DC bus, or mains-derived/high-power stages. Any >24 V DC or mains concept is documentation-only Future Work.

## 6. Development Status

| Module | Status |
|---|---|
| Project structure | Initialized |
| UART basic output | PASS — hardware verified |
| ADC GND endpoint | PASS — hardware verified |
| ADC full-scale endpoint | PASS — hardware verified after startup calibration |
| ADC potentiometer sweep | PASS — hardware verified |
| ADC accuracy | Not Tested |
| ADC linearity | Not Tested |
| PWM basic duty output | PASS — 10%, 25%, 50%, 75%, and 90% hardware verified |
| PWM frequency calculation | 1 kHz theoretical |
| PWM frequency hardware measurement | Not Tested |
| PWM RC filter | PASS — 100 kOhm / 100 nF hardware verified |
| PWM analog output | PASS — five DC output points verified with DMM |
| PWM ripple | Not Measured |
| PWM settling time | Not Measured |
| PWM oscilloscope verification | Not Tested |
| PWM RC load drive capability | Not Tested |
| RC feedback plant | PASS — minimum feedback path hardware verified |
| Deadband incremental controller | PASS — direction and convergence verified |
| True P controller | Not Implemented |
| PI controller | Not Implemented |
| Step response characterization | Not Tested |
| Python host plotting | Not Implemented |
| Current sensing | Post-MVP / Future Work |
| Voltage sensing | Post-MVP / Future Work |
| Reference AFE | Post-MVP / Future Work |
| RS485 | Post-MVP / Future Work |
| Modbus | Post-MVP / Future Work |
| Protection | Post-MVP / Future Work |
| PCB | Post-MVP / Future Work |

## Engineering Rules

Unknown values are `TBD`; unperformed verification is `Not Tested`. GPIO assignments are not guessed. Tests must identify firmware commit and hardware version. Significant choices, problems, and pending work belong in the decision, debug, and issue logs respectively.

## Next Task

Only: **Day 5 / True P Controller**. The current verified algorithm is a deadband incremental controller, not a P controller. PI remains `Not Implemented`.
