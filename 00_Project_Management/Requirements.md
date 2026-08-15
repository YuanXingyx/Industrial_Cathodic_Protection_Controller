# System Requirements — Revision 0

Status: Draft. Verification status for every requirement: `Not Tested`.

## SYS

| ID | Requirement | Planned verification |
|---|---|---|
| SYS-001 | The system shall use STM32F103 for V0/V1. | Inspection |
| SYS-002 | V0/V1 experiment supply shall not exceed 24 V DC. | Inspection and measurement |
| SYS-003 | The system shall provide a target-potential setting. | Functional test |
| SYS-004 | The system shall acquire the simulated actual potential. | TEST-001/002 |
| SYS-005 | The system shall provide closed-loop control in a later validated phase. | TEST-008/009 |

## ADC

| ID | Requirement |
|---|---|
| ADC-001 | V0 shall initially use the STM32 internal 12-bit ADC. |
| ADC-002 | Phase 1 input test range shall be 0–3.3 V. |
| ADC-003 | Records shall include ADC RAW, measured VDDA, and converted voltage. |

## PWM

| ID | Requirement |
|---|---|
| PWM-001 | An STM32 timer shall generate PWM. |
| PWM-002 | Firmware shall permit PWM duty adjustment. |
| PWM-003 | A later phase may use PWM to command a low-voltage power stage. |

## Control

| ID | Requirement |
|---|---|
| CTRL-001 | The first closed-loop phase shall implement P control. |
| CTRL-002 | The next closed-loop phase shall implement PI control. |
| CTRL-003 | Control output shall be limited. |
| CTRL-004 | PI design shall include integral limiting/anti-windup. |

## Communication

| ID | Requirement |
|---|---|
| COMM-001 | V0 shall use UART for debug telemetry at approximately 2–10 Hz. |
| COMM-002 | V1 shall add RS485 after earlier modules are verified. |
| COMM-003 | A later phase shall add Modbus RTU. |
