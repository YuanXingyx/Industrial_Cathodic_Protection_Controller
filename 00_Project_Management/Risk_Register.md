# Risk Register

| ID | Risk | Probability | Impact | Mitigation | Status |
|---|---|---|---|---|---|
| RISK-001 | ADC accuracy insufficient | Medium | High | Measure VDDA; characterize gain/offset and repeatability before architecture changes | Open |
| RISK-002 | Analog input noise | High | Medium | Short wiring, grounding review, sampling statistics, then justified filtering | Open |
| RISK-003 | PI controller instability | Medium | High | Plant characterization, bounded output/integral, staged tuning | Open |
| RISK-004 | PWM ripple too large | Medium | Medium | Characterize ripple/settling before selecting filter | Open |
| RISK-005 | Breadboard parasitics affect analog tests | High | Medium | Document layout; compare alternate construction when necessary | Open |
| RISK-006 | Reference input loads electrode | Medium | High | Define source impedance and input-bias requirements before AFE selection | Open |
| RISK-007 | Current-sense range incorrect | Medium | High | Establish current range and fault envelope before shunt/amplifier selection | Open |
| RISK-008 | Project scope becomes too large | High | High | Enforce phase gates and one next task | Open |
| RISK-009 | High-voltage work introduced too early | Low | Critical | Hard <=24 V DC boundary; document higher-voltage concepts as Future Work only | Open |
