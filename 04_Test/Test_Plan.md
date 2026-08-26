# Test Plan

Every execution must use the record template, identify firmware commit and hardware version, preserve raw data/waveform paths, and report `Not Tested` until performed.

## MVP Priority

MVP 必须完成：TEST-001、TEST-002、TEST-004、TEST-006、TEST-007、TEST-008、TEST-009。TEST-003 和 TEST-005 保留原编号，作为支持性测试，不破坏现有编号体系。执行顺序仍从 TEST-001 开始，后续测试不得绕过其前置条件。

| Test ID | MVP Priority | Purpose | Equipment | Setup | Procedure | Expected Result | Measured Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|---|---|---|
| TEST-001 ADC Basic Acquisition | MVP Required / First | Verify basic conversion and UART report | STM32 board, potentiometer, DMM, USB-UART, current-limited supply | 0–3.3 V input; exact pins TBD | Apply safe points; record DMM, VDDA, raw and converted values | Valid bounded readings and correctly formatted 2–10 Hz telemetry; numeric tolerance TBD before run | Not Tested | Not Tested | First and only recommended next task |
| TEST-002 ADC Linearity / Stability | MVP Required | Characterize conversion across range and short-term stability | Same as TEST-001 | Six specified voltage points | Repeat readings and calculate error against DMM | Acceptance threshold TBD | Not Tested | Not Tested | Preserve CSV |
| TEST-003 ADC Noise | Supporting | Characterize stationary-input variation | Same plus stable source if available | Fixed points TBD | Capture sample series without hiding raw data | Threshold TBD | Not Tested | Not Tested | Record bandwidth/sample timing |
| TEST-004 PWM Output | MVP Required | Verify configured frequency and basic output | Oscilloscope/logic analyzer | PWM pin TBD | Measure multiple periods and commanded output | Matches configured tolerance TBD | Not Tested | Not Tested | Existing TEST-004 ID retained |
| TEST-005 PWM Duty | Supporting | Verify duty command | Oscilloscope/logic analyzer | PWM pin TBD | Sweep selected duty points | Tolerance TBD | Not Tested | Not Tested | |
| TEST-006 PWM RC Filter | MVP Required | Measure ripple, settling, linearity | Oscilloscope, DMM | RC values TBD | Step/sweep duty | Criteria TBD from requirements | Not Tested | Not Tested | |
| TEST-007 Dummy Load | MVP Required | Characterize RC plant | Oscilloscope, DMM | Load revision TBD | Apply bounded steps | Reproducible response matching documented simple model | Not Tested | Not Tested | |
| TEST-008 P Control | MVP Required | Characterize bounded P loop | Prior validated modules | Kp/sample time TBD | Apply setpoint and disturbance steps | Stable response within TBD criteria | Not Tested | Not Tested | Gated |
| TEST-009 PI Control | MVP Required | Characterize bounded PI loop | Prior validated modules | Kp/Ki/limits TBD | Apply setpoint and disturbance steps | Stable response and verified limiting | Not Tested | Not Tested | Gated |
