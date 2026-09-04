import serial
import re
import csv
import time
import matplotlib.pyplot as plt

PORT = "COM7"
BAUD = 115200

pattern = re.compile(
    r"TICK=(\d+),\s*"
    r"ADC=(\d+),\s*"
    r"TARGET=(\d+),\s*"
    r"INT=(-?\d+),\s*"
    r"ERR=(-?\d+),\s*"
    r"KP=([\d.]+),\s*"
    r"KI=([\d.]+),\s*"
    r"OUT=(\d+),\s*"
    r"DUTY=(\d+)"
)

ser = serial.Serial(PORT, BAUD, timeout=1)

times = []
adc_values = []
target_values = []

plt.ion()

fig, ax = plt.subplots()

adc_line, = ax.plot([], [], label="ADC")
target_line, = ax.plot([], [], label="Target")

ax.set_xlabel("Time (s)")
ax.set_ylabel("ADC Raw")
ax.set_title("PI Closed-Loop Response")
ax.legend()
ax.grid(True)

with open("pi_log.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
    "time_s",
    "mcu_tick_ms",
    "adc",
    "target",
    "integral",
    "error",
    "kp",
    "ki",
    "output_x100",
    "duty"
    ])

    t0 = time.time()

    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()

            match = pattern.search(line)

            if not match:
                continue

            mcu_tick_ms = int(match.group(1))
            adc = int(match.group(2))
            target = int(match.group(3))
            integral = int(match.group(4))
            error = int(match.group(5))
            kp = float(match.group(6))
            ki = float(match.group(7))
            output_x100 = int(match.group(8))
            duty = int(match.group(9))

            t = time.time() - t0

            writer.writerow([
                t,
                mcu_tick_ms,
                adc,
                target,
                integral,
                error,
                kp,
                ki,
                output_x100,
                duty
            ])

            f.flush()

            times.append(t)
            adc_values.append(adc)
            target_values.append(target)

            print(
                f"{t:.2f}s "
                f"TICK={mcu_tick_ms} "
                f"ADC={adc} "
                f"TARGET={target} "
                f"ERR={error} "
                f"INT={integral} "
                f"OUT={output_x100 / 100.0:.2f}% "
                f"DUTY={duty}"
            )

            adc_line.set_data(times, adc_values)
            target_line.set_data(times, target_values)

            ax.relim()
            ax.autoscale_view()

            plt.pause(0.01)

    except KeyboardInterrupt:
        print("\nLogging stopped by user.")

    finally:
        ser.close()
        plt.ioff()
        plt.show()
