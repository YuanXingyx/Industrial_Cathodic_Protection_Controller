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
