# Design Decisions

## DD-001 Use STM32F103 for V0

### Context
The project targets analog measurement, control, debugging and industrial communication rather than MCU migration.
### Decision
Use STM32F103 for V0 and V1.
### Consequence
Revisit MCU selection only for V2; exact board and pins remain TBD.

## DD-002 Use internal ADC in V0

Use the internal 12-bit ADC for initial characterization. An external precision ADC requires evidence from V0 measurements.

## DD-003 Use PWM instead of external DAC initially

Characterize timer PWM and an RC reconstruction filter before considering a DAC. Ripple and settling constraints remain TBD.

## DD-004 Limit experiment voltage to <=24 V DC

All V0/V1 implementation is low voltage. Mains and >24 V DC work is documentation-only Future Work.

## DD-005 Validate modules before PCB

ADC, PWM, filter, dummy load and controls must have reproducible tests before PCB integration, reducing coupled unknowns and preserving evidence.
