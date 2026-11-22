import numpy as np
import matplotlib.pyplot as plt

# 1. Загрузка данных
# np.loadtxt автоматически пропускает строки с решеткой (# step adc)
data_0 = np.loadtxt('test_00mm.txt', comments='#')
data_77 = np.loadtxt('test_0mm.txt', comments='#')

# Берем второй столбец (индекс 1), там где значения АЦП
adc_0 = data_0[:, 1]
adc_77 = data_77[:, 1]

# 2. Усреднение значений АЦП для калибровочных точек
# Для калибровки берем среднее арифметическое всех замеров
mean_adc_0 = np.mean(adc_0)   # Когда дувка выключена (0 Па)
mean_adc_77 = np.mean(adc_77) # Когда дувка включена (77 Па)

print(f"Средний АЦП при 0 Па: {mean_adc_0:.1f}")
print(f"Средний АЦП при 77 Па: {mean_adc_77:.1f}")

# Наши "идеальные" точки для калибровки (АЦП, Давление)
x_points = np.array([mean_adc_0, mean_adc_77])
y_points = np.array([0, 87])

# 3. Линейная аппроксимация (МНК)
# Находим коэффициенты a и b для уравнения P = a*N + b
a, b = np.polyfit(x_points, y_points, 1)

# 4. Построение графика
plt.figure(figsize=(10, 6))

# Рисуем точки (средние значения)
plt.scatter(x_points, y_points, color='tab:blue', s=80, zorder=5, label='Измерения (среднее)')

# Рисуем линию тренда
# Берем диапазон по X чуть шире наших точек для красоты
x_line = np.linspace(mean_adc_0 - 200, mean_adc_77 + 200, 100)
y_line = a * x_line + b

# Форматируем уравнение для легенды (например: P = 0.0267·N - 5678 [Па])
equation_label = f'P = {a:.4f}·N {b:+.0f} [Па]'
plt.plot(x_line, y_line, color='tab:orange', linewidth=2, label=equation_label)

# Настройка осей и оформления (как на твоем скрине)
plt.title('Калибровка датчика давления', fontsize=14, fontweight='bold')
plt.xlabel('Отсчёт АЦП', fontsize=12)
plt.ylabel('Давление [Па]', fontsize=12)

# Включаем сетку (основную и минорную)
plt.grid(True, which='major', linestyle='--', alpha=0.7)
plt.minorticks_on()
plt.grid(True, which='minor', linestyle='--', alpha=0.4)

# Красивая легенда
plt.legend(loc='upper left', fontsize=12)

# Показываем график
plt.tight_layout()
plt.show()