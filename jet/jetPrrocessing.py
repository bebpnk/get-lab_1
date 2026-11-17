import time
import numpy as np
import jetFunctions as j

count = 50
stepsBetween = 30
samples = 10
filename = "80mm.txt"

try:
    steps = 0

    j.initSpiAdc()
    j.initStepMotorGpio()

    rows = []

    for i in range(count):
        values = []
        for k in range(samples):
            values.append(j.getAdc())
            time.sleep(0.05)

        rows.append((i * stepsBetween, np.median(values)))

        j.stepForward(stepsBetween)
        time.sleep(0.2)

    j.stepBackward(count * stepsBetween)

    np.savetxt(filename, np.array(rows), fmt=["%d", "%.1f"], header="step adc")
    print(f"Измерения завершены. Данные сохранены в {filename}")

finally:
    j.deinitSpiAdc()
    j.deinitStepMotorGpio()