# ЗАДАЧА: Визуализировать импорт/экспорт Россию на примере импорта/экспорта с Турцией
# https://github.com/infoculture/datatasks/issues/54
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import switch as sw

# читаем файл с данными и делаем из него dataframe
dt = pd.read_csv("turkey.csv")


# смотрим года сбора данных и регионы
print(set(dt["PERIOD"]), set(dt["REGION_S"]))

# создаём список лет в dataframe-e
years = []                              # список будет состоять из целочисленных значений

# заполняем список
for i in dt["PERIOD"]:
    if i not in years:
        years = np.append(years, i)

# берём колонки с информацией по депозитам и годами
npdt = dt.values[:, 0:2]
inf = npdt[:, 0]
date = npdt[:, 1]
reg = np.array(dt["REGION_S"])

# создаём переменные для подсчёта импорта и экспорта по годам
exp13 = exp14 = exp15 = exp16 = 0
imp13 = imp14 = imp15 = imp16 = 0

ereg = [0, 0, 0, 0, 0, 0, 0, 0, 0]
ireg = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# заполняем данные по экспорту и импорту
for i in range(len(inf)):
    if inf[i] == "ЭК":                                   # если текущая позиция - экспорт
        for j in range(len(ereg)):
            if int(reg[i][1]) == j+1:
                ereg[j] = ereg[j] + 1
                break

        for case in sw.switch(date[i]):
            if case(2013):
                exp13 += 1
                break
            if case(2014):
                exp14 += 1
                break
            if case(2015):
                exp15 += 1
                break
            if case(2016):
                exp16 += 1
                break
    elif inf[i] == "ИМ":                                 # если текущая позиция - импорт
        for j in range(len(ireg)):
            if int(reg[i][1]) == j+1:
                ireg[j] = ireg[j] + 1
                break

        for case in sw.switch(date[i]):
            if case(2013):
                imp13 += 1
                break
            if case(2014):
                imp14 += 1
                break
            if case(2015):
                imp15 += 1
                break
            if case(2016):
                imp16 += 1
                break

print(ireg, ereg)
# считаем общие импорт и экспорт за 2013-2016 года
texp = exp13 + exp14 + exp15 + exp16
timp = imp13 + imp14 + imp15 + imp16

# создаём график общего импорта и экспорта
plt.title("total export and import for 2013-2016")
plt.bar("export", texp, color="red")
plt.bar("import", timp, color="blue")
# plt.show()
plt.savefig("total_exp_imp.png")    # сохраняем график в виде png

# создаём подграфики импорта и экспорта по годам
plt.suptitle("export and import in years")
plt.subplots_adjust(hspace=0.4)     # вертикальный отступ между графиками
plt.subplots_adjust(wspace=0.3)     # горизонтальный отступ между графиками
plt.subplots_adjust(top=0.86)       # отступ от заголовка
# первый график, все последующие графики имеют одинаковые координатные оси благодаря параметрам sharex и sharey
fsp = plt.subplot(2, 2, 1)
plt.title("2013")
plt.bar("export", exp13, color="red")
plt.bar("import", imp13, color="blue")

# второй график
plt.subplot(2, 2, 2, sharex=fsp, sharey=fsp)
plt.title("2014")
plt.bar("export", exp14, color="red")
plt.bar("import", imp14, color="blue")

# третий график
plt.subplot(2, 2, 3, sharex=fsp, sharey=fsp)
plt.title("2015")
plt.bar("export", exp15, color="red")
plt.bar("import", imp15, color="blue")

# четвёртый график
plt.subplot(2, 2, 4, sharex=fsp, sharey=fsp)
plt.title("2016")
plt.bar("export", exp16, color="red")
plt.bar("import", imp16, color="blue")

plt.savefig("imp_exp_in_years.png")     # сохраняем график в виде png
# plt.show()

fig, ax = plt.subplots()
index = [1, 2, 3, 4, 5, 6, 7, 8, 9]
bar_width = 0.2

rects1 = plt.bar([x + 0.05 for x in index], ireg, bar_width, color="b", label="import")
rects2 = plt.bar([x + bar_width for x in index], ereg, bar_width, color="r", label="export")

plt.show()