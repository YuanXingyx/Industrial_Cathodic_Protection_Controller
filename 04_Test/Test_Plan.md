# Test Plan

Every execution must use the record template, identify firmware commit and hardware version, preserve raw data/waveform paths, and report `Not Tested` until performed.

| Test ID | Purpose | Equipment | Setup | Procedure | Expected Result | Measured Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|---|---|
| TEST-001 ADC Basic Acquisition | Verify basic conversion and UART report | STM32 board, potentiometer, DMM, USB-UART, current-limited supply | 0–3.3 V input; exact pins TBD | Apply safe points; record DMM, VDDA, raw and converted values | Valid bounded readings and correctly formatted 2–10 Hz telemetry; numeric tolerance TBD before run | Not Tested | Not Tested | First and only recommended next task |
| TEST-002 ADC Linearity | Characterize conversion across range | Same as TEST-001 | Six specified voltage points | Repeat readings and calculate error against DMM | Acceptance threshold TBD | Not Tested | Not Tested | Preserve CSV |
| TEST-003 ADC Noise | Characterize stationary-input variation | Same plus stable source if available | Fixed points TBD | Capture sample series without hiding raw data | Threshold TBD | Not Tested | Not Tested | Record bandwidth/sample timing |
| TEST-004 PWM Frequency | Verify configured frequency | Oscilloscope/logic analyzer | PWM pin TBD | Measure multiple periods | Matches configured tolerance TBD | Not Tested | Not Tested | |
| TEST-005 PWM Duty | Verify duty command | Oscilloscope/logic analyzer | PWM pin TBD | Sweep selected duty points | Tolerance TBD | Not Tested | Not Tested | |
| TEST-006 PWM RC Filter | Measure ripple, settling, linearity | Oscilloscope, DMM | RC values TBD | Step/sweep duty | Criteria TBD from requirements | Not Tested | Not Tested | |
| TEST-007 Dummy Load | Characterize RC plant | Oscilloscope, DMM | Load revision TBD | Apply bounded steps | Reproducible response matching documented simple model | Not Tested | Not Tested | |
| TEST-008 P Control Step Response | Characterize bounded P loop | Prior validated modules | Kp/sample time TBD | Apply setpoint and disturbance steps | Stable response within TBD criteria | Not Tested | Not Tested | Gated |
| TEST-009 PI Control Step Response | Characterize bounded PI loop | Prior validated modules | Kp/Ki/limits TBD | Apply setpoint and disturbance steps | Stable response and verified limiting | Not Tested | Not Tested | Gated |
