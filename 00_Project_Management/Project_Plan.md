# Project Plan

No phase may claim completion without linked evidence and a firmware commit.

## Phase 0 — Project Initialization

Repository structure, Git metadata, README, requirements, debug log, issue log, plans and templates. Status: initialized; review pending.

## Phase 1 — ADC

`Potentiometer → ADC → UART`. Test 0.5, 1.0, 1.5, 2.0, 2.5 and 3.0 V. Record DMM value, ADC value, error, VDDA and conditions. Status: Not Tested.

## Phase 2 — PWM

`STM32 → PWM`; verify frequency, duty and stability. Status: Not Tested.

## Phase 3 — PWM to Analog

`PWM → RC filter → analog voltage`; measure ripple, settling time and linearity. Status: Not Tested.

## Phase 4 — Dummy Load

Start with a first-order RC model representing only an intentionally simplified load/polarization response. Values: TBD. Status: Not Tested.

## Phase 5 — P Control

Implement `output = Kp * (target - measured)` with output limits; record Kp, rise time, overshoot and steady-state error. Status: Not Tested.

## Phase 6 — PI Control

Add integral action, output/integral limits and verified anti-windup. Status: Not Tested.

## Phase 7 — Current Sense

**Post-MVP / Future Work.** Evaluate shunt plus INA180/INA181-class solution; range and part are TBD.

## Phase 8 — Voltage Sense

**Post-MVP / Future Work.** Evaluate `Vout → divider → protection → ADC`; values are TBD.

## Phase 9 — Reference Input AFE

**Post-MVP / Future Work.** Evaluate high input impedance, low bias current, filtering, protection, bipolar conditioning and ADC range conversion from real requirements; do not assume industrial parameters.

## Phase 10 — RS485 / Modbus

**Post-MVP / Future Work**, after core low-voltage modules are verified.

## Phase 11 — PCB

**Post-MVP / Future Work**, only after module-level verification.

## MVP Exit Criteria

The Cathodic Protection Control Loop MVP exits only when all criteria below have real, linked test evidence:

- ADC 能稳定采样。
- PWM 可调。
- RC 输出可控。
- 闭环能够跟踪目标值。
- PI 调节有效。
- PC 能显示 Setpoint、Measured 和 Control Output 实时曲线。
- 至少完成一次 `0.8 V → 1.2 V → 1.8 V` 阶跃响应测试。
- 所有结果来自真实测试，不得虚构；未完成项保持 `Not Tested` 或 `TBD`。
