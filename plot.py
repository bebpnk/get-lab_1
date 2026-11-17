import numpy as np

adc = [p40.mean(), p80.mean(), p120.mean(), p160.mean()]
pressure = [40, 80, 120, 160]

k, b = np.polyfit(adc, pressure, 1)      # P = k·N + b
values = np.polyval([k, b], samples)
coefs, cov = np.polyfit(x, y, 1, cov=True)
errors = np.sqrt(np.diag(cov))
import matplotlib.pyplot as plt

fit_x = np.linspace(min(adc), max(adc), 100)
plt.plot(adc, pressure, "*", label="Измерения")
plt.plot(fit_x, np.polyval([k, b], fit_x), label="P = %.3f·N %+.1f [мм рт. ст.]" % (k, b))
plt.xlabel("Отсчёты АЦП")
plt.ylabel("Давление [мм рт. ст.]")
plt.grid(which="major")
plt.grid(which="minor", linestyle="--")
plt.minorticks_on()
plt.legend()
plt.savefig("pressure-calibration.png", dpi=200)