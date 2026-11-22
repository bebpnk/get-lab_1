import numpy as np
import matplotlib.pyplot as plt
import os

# --- Константы ---
rho = 1.2               # Плотность воздуха [кг/м^3]
calib_slope = 0.0308    # Честный коэффициент с графика калибровки [Па/отсчет]
step_mm = 0.038         # Шаг перемещения [мм]

files = ['00mm.txt', '10mm.txt', '20mm.txt', '30mm.txt', 
         '40mm.txt', '50mm.txt', '60mm.txt', '70mm.txt', '80mm.txt']

plt.figure(figsize=(12, 8))

for filename in files:
    if not os.path.exists(filename):
        continue
        
    data = np.loadtxt(filename, comments='#')
    steps, adc = data[:, 0], data[:, 1]
    
    # 1. Убираем линейный дрейф нуля от начала к концу замера
    zero_line = np.linspace(np.mean(adc[:5]), np.mean(adc[-5:]), len(adc))
    dp = calib_slope * (adc - zero_line)
    dp[dp < 55 * calib_slope] = 0

    
    v = np.sqrt(2 * dp / rho)
    
    # 2. Центрируем по энергетическому центру струи (а не по случайному пику)
    center_step = np.sum(steps * v**2) / np.sum(v**2)
    r_mm = (steps - center_step) * step_mm
    r_m = r_mm * 1e-3
    
    # 3. Расчет расхода Q методом трапеций (левая + правая половины)
    mask_r = r_m >= 0
    mask_l = r_m <= 0
    
    int_r = np.trapezoid(r_m[mask_r] * v[mask_r], r_m[mask_r])
    int_l = np.trapezoid(-r_m[mask_l][::-1] * v[mask_l][::-1], -r_m[mask_l][::-1])
    
    q_avg = 2 * np.pi * rho * (int_r + int_l) / 2 * 1000  # [г/с]
    
    plt.plot(r_mm, v, label=f"Q ({filename[:2]} мм) = {q_avg:.2f} [г/с]", linewidth=2)

# --- Оформление графика ---
plt.title('Скорость потока воздуха в сечении затопленной струи', fontsize=14, fontweight='bold')
plt.xlabel('Положение трубки Пито относительно центра струи [мм]', fontsize=12)
plt.ylabel('Скорость воздуха [м/с]', fontsize=12)

plt.grid(True, which='major', linestyle='-', alpha=0.7)
plt.minorticks_on()
plt.grid(True, which='minor', linestyle='--', alpha=0.4)
plt.legend(loc='upper right', fontsize=11)
plt.tight_layout()
plt.show()