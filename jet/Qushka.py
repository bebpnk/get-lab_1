import numpy as np
import matplotlib.pyplot as plt
import os

# --- Константы ---
rho = 1.2               # Плотность воздуха [кг/м^3]
calib_slope = 0.0308    # Ваш коэффициент калибровки [Па/отсчет]
step_m = 0.038 * 1e-3   # Шаг перемещения в метрах [м]

# Берем функцию трапеций, которая точно есть в установленном NumPy
integrate = getattr(np, 'trapezoid', getattr(np, 'trapz', None))

def calculateOutgo(x, u):
    # радиус — расстояние до оси без знака [м]
    r = np.abs(x)
    # подынтегральная функция: ρ·2π·r·u, кг/(м·с)
    f = rho * 2 * np.pi * r * u
    # сумма трапеций по всему профилю, делённая на два — среднее двух половин
    q = integrate(f, x) / 2.0
    # вернуть массовый расход в кг/с
    return q

distances = [0, 10, 20, 30, 40, 50, 60, 70, 80]
q_values_gs = []  # Сюда сложим расходы в г/с для второго графика
valid_d = []      # Расстояния для файлов, которые реально нашлись

# === ГРАФИК 1: Профили скорости ===
plt.figure(1, figsize=(11, 7))

print("--- Результаты расчёта расхода ---")
for d in distances:
    filename = f"{d:02d}mm.txt"
    if not os.path.exists(filename):
        continue
        
    data = np.loadtxt(filename, comments='#')
    steps, adc = data[:, 0], data[:, 1]
    
    # 1. Убираем дрейф нуля по краям прохода и отсекаем шум АЦП
    zero_line = np.linspace(np.mean(adc[:5]), np.mean(adc[-5:]), len(adc))
    dp = calib_slope * (adc - zero_line)
    dp[dp < 55 * calib_slope] = 0
    
    u = np.sqrt(2 * dp / rho)  # Скорость [м/с]
    
    # 2. Центрируем профиль по энергетическому центру (центру масс u^2)
    center_step = np.sum(steps * u**2) / np.sum(u**2)
    x = (steps - center_step) * step_m  # Координата от оси [м]
    
    # 3. Считаем расход через функцию из методички
    q = calculateOutgo(x, u)  # [кг/с]
    q_gs = q * 1000           # [г/с]
    
    valid_d.append(d)
    q_values_gs.append(q_gs)
    print(f"x = {d:02d} мм  ->  Q = {q_gs:.2f} г/с")
    
    plt.plot(x * 1000, u, label="Q (%02d мм) = %.2f [г/с]" % (d, q_gs), linewidth=2)

plt.title('Скорость потока воздуха в сечении затопленной струи', fontsize=14, fontweight='bold')
plt.xlabel('Положение трубки Пито относительно центра струи [мм]', fontsize=12)
plt.ylabel('Скорость воздуха [м/с]', fontsize=12)
plt.grid(True, which='major', linestyle='-', alpha=0.7)
plt.minorticks_on()
plt.grid(True, which='minor', linestyle='--', alpha=0.4)
plt.legend(loc='upper right', fontsize=10)
plt.tight_layout()

# === ГРАФИК 2: Расход от расстояния ===
plt.figure(2, figsize=(10, 6))

valid_d = np.array(valid_d)
q_values_gs = np.array(q_values_gs)

# Аппроксимация прямой (y = k*x + b)
k, b = np.polyfit(valid_d, q_values_gs, 1)
x_line = np.linspace(min(valid_d), max(valid_d), 100)
y_line = k * x_line + b

plt.scatter(valid_d, q_values_gs, label='Измерения', s=50, zorder=3)
plt.plot(x_line, y_line, color='tab:orange', linewidth=2,
         label=f'Q = {k:.3f}·x +{b:.2f} [г/с]')

plt.title('Расход затопленной струи', fontsize=14, fontweight='bold')
plt.xlabel('Расстояние от среза сопла [мм]', fontsize=12)
plt.ylabel('Массовый расход [г/с]', fontsize=12)
plt.grid(True, which='major', linestyle='-', alpha=0.7)
plt.minorticks_on()
plt.grid(True, which='minor', linestyle='--', alpha=0.4)
plt.legend(loc='upper left', fontsize=11)
plt.tight_layout()

plt.show()
