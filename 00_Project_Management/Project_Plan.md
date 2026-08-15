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

Evaluate shunt plus INA180/INA181-class solution; range and part are TBD.

## Phase 8 — Voltage Sense

Evaluate `Vout → divider → protection → ADC`; values are TBD.

## Phase 9 — Reference Input AFE

Evaluate high input impedance, low bias current, filtering, protection, bipolar conditioning and ADC range conversion from real requirements; do not assume industrial parameters.

## Phase 10 — RS485 / Modbus

Future, after core low-voltage modules are verified.

## Phase 11 — PCB

Future, only after module-level verification.
