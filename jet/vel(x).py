import numpy as np
import matplotlib.pyplot as plt
import os

# --- Настройки из теории и твоих данных ---
rho = 1.2            # Плотность воздуха [кг/м^3]
calib_slope = 0.0452 # Коэффициент наклона из калибровки (Па/отсчет)
step_mm = 0.038      # Длина одного шага в мм (38/1000)

# Значения Q из твоего эталонного графика (для легенды)
q_values = {
    '00': 6.40, '10': 6.90, '20': 7.28, '30': 9.20, 
    '40': 9.95, '50': 9.03, '60': 11.42, '70': 11.62, 
    '80': 0.00 # Для 80мм нет значения на скрине, можешь поправить
}

files = ['00mm.txt', '10mm.txt', '20mm.txt', '30mm.txt', 
         '40mm.txt', '50mm.txt', '60mm.txt', '70mm.txt', '80mm.txt']

plt.figure(figsize=(12, 8))

for filename in files:
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден, пропускаем...")
        continue
        
    # 1. Загрузка данных
    data = np.loadtxt(filename, comments='#')
    steps = data[:, 0]
    adc = data[:, 1]
    
    # 2. Базовый уровень (когда трубка не в потоке, P0 - P = 0)
    # Берем среднее первых 5 точек, где поток точно отсутствует
    base_adc = np.mean(adc[:5])
    
    # 3. Расчет дельты давления и скорости (строго по формулам из текста)
    # Датчик меряет разность P0 - P. Константа -9406 сокращается при вычитании фона.
    delta_P = calib_slope * (adc - base_adc) 
    
    # Защита от отрицательных значений (шум датчика)
    delta_P[delta_P < 0] = 0
    
    # Формула Бернулли из файла: V = sqrt( 2 * (P0 - P) / rho )
    velocity = np.sqrt(2 * delta_P / rho)
    
    # 4. Расчет координаты X в мм и центрирование
    # Переводим шаги в миллиметры
    x_mm = steps * step_mm
    
    # Находим центр струи (по максимуму скорости), чтобы совместить графики
    center_x = np.average(x_mm, weights=velocity)
    x_centered = x_mm - center_x
    
    # 5. Красивая легенда
    num = filename[:2]
    q_val = q_values.get(num, 0.00)
    label_str = f"Q ({num} мм) = {q_val:.2f} [г/с]"
    
    # 6. Отрисовка
    plt.plot(x_centered, velocity, label=label_str, linewidth=2)

# --- Оформление графика (как на скрине) ---
plt.title('Скорость потока воздуха в сечении затопленной струи', fontsize=14, fontweight='bold')
plt.xlabel('Положение трубки Пито относительно центра струи [мм]', fontsize=12)
plt.ylabel('Скорость воздуха [м/с]', fontsize=12)

# Сетка
plt.grid(True, which='major', linestyle='-', alpha=0.7)
plt.minorticks_on()
plt.grid(True, which='minor', linestyle='--', alpha=0.4)

# Легенда
plt.legend(loc='upper right', fontsize=11)

plt.tight_layout()
plt.show()