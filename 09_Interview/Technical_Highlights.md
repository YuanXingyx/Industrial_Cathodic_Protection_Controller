# Technical Highlights

Develop evidence-backed answers for:

- Why STM32F103 was selected
- Why V0 starts with the internal ADC
- ADC error sources
- Why a reference electrode needs high input impedance
- Why industrial environments require filtering
- Why PI may be needed beyond P control
- Integral saturation and anti-windup
- How PWM commands a low-voltage power stage
- How output current can be measured
- Why RS485 is useful
- Why a dummy load is used
- Why the project does not directly implement 220/380 V

Current evidence status: Not Tested. Do not turn planned design rationale into claimed results.

## Day 5 — P Controller Talking Points

- A P controller changes its output in proportion to the current error:
  `error = target - measured`.
- With this loop polarity, a larger positive error produces a larger PWM
  command; a negative error reduces PWM.
- `Kp` sets correction strength. Too small gives weak correction and potentially
  larger offset; too large can cause aggressive response, overshoot, or
  oscillation. Only `Kp = 0.01` has been validated here.
- P-only control can retain steady-state offset when the plant requires a
  nonzero sustained correction. The actual offset also depends on plant gain,
  hardware conditions, and base-duty bias.
- Integral action is the planned next step because accumulated error can supply
  that sustained correction; it also requires integral limits/anti-windup.
- The temporary 10 kOhm/100 uF plant has `RC ≈ 1 s`, so its output lags controller
  changes and experiments need a long settling interval.
- Do not quantize the floating-point P output to integer duty before calculating
  CCR. Direct CCR calculation preserves timer-level resolution; rounded duty is
  suitable only for human-readable telemetry.

Day 4 and Day 5 must be described separately: Day 4 verified a deadband
incremental controller; Day 5 verified a true P controller with 50% base-duty
bias.

## Day 6 — PI Controller Talking Points

- The P term reacts to current error; the I term accumulates error over time and
  supplies the sustained correction that P-only control may lack.
- P-only control can retain offset because a nonzero error may be required to
  produce the needed correction. Integral action can retain that correction
  even after instantaneous error reaches zero.
- `ERR=0` with nonzero `INT` is expected: the integral state represents past
  error and can hold the output away from the 50% base duty.
- This implementation clamps the integral state to ±5000 to prevent unlimited
  accumulation. Clamping is basic protection, not complete anti-windup.
  Conditional integration and back-calculation are not implemented.
- The temporary 10 kOhm/100 uF plant has `RC ≈ 1 s`, so feedback reacts slowly
  and each experiment requires a long observation interval.
- Isolated ADC outliers returned immediately to the target region. They are
  recorded as possible sampling/contact/transient noise with root cause TBD,
  not automatically labeled controller instability.

Controller progression: Day 4 deadband incremental → Day 5 P with base-duty
bias → Day 6 PI with integral clamping.

## Day 7 — Host Validation Talking Points

Built a minimum closed-loop validation on STM32F103 using ADC, PI control,
PWM-based analog output, UART telemetry, Python visualization, and step-response
logging; identified gain-dependent stability trade-offs experimentally.

- The Python tool parses all telemetry fields, plots Target/ADC in real time,
  and preserves raw evidence in CSV, including control output at 0.01% units.
- The `2048 → 2400 → 2048` command verified response direction and return toward
  the baseline target. Exact settling time was not measured.
- Increasing Kp from the stable 0.010 baseline to approximately 0.015 produced
  sustained oscillation; 0.020 produced stronger sustained oscillation. The
  engineering decision was to restore 0.010 rather than keep increasing gain.
- Isolated ADC spikes are tracked separately with root cause TBD; they were not
  misclassified as sustained controller instability.
- This is a low-voltage control-loop MVP. Reference-electrode AFE, industrial
  power conversion, sensing, communications, protection, supply, and EMC work
  remain outside the validated scope.

## Day 8 — ADC Averaging Talking Points

Compared multiple RC time constants and ADC acquisition strategies, then
introduced eight-sample averaging to reduce measurement spikes while preserving
closed-loop stability on the STM32F103 MVP.

- Replacing the temporary 100 uF capacitor with 1 uF reduced the plant time
  constant; static 25%, 50%, and 75% points were verified before closed-loop use.
- Eight valid ADC conversions are averaged per approximately 100 ms PI update.
  Failed conversions are excluded, and the controller is not updated if all
  conversions fail.
- The `2048 -> 2400 -> 2048` hardware run retained correct tracking direction
  and closed-loop stability. The curve was visibly smoother and isolated spikes
  were reduced relative to single-sample acquisition.
- The spike root cause is not fully confirmed, so averaging is described as an
  observed improvement rather than a complete root-cause fix.
- A 20 ms update-period experiment produced more visible variation without a
  clear speed gain. The stable `Kp=0.010`, `Ki=0.002`, approximately 100 ms
  baseline was restored instead of continuing to tune multiple variables.
- Response is still slow and exact settling time was not measured.
- This remains a low-voltage minimum constant-potential control validation, not
  a production industrial potentiostat or industrial filtering solution.
