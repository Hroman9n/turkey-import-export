# ЗАДАЧА: Визуализировать импорт/экспорт Россию на примере импорта/экспорта с Турцией
# https://github.com/infoculture/datatasks/issues/54
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import switch as sw


# функция для показа значений столбцов
def autolabel(rects, labels=None, height_factor=0.994):
    for i, rect in enumerate(rects):
        height = rect.get_height()
        if labels is not None:
            try:
                label = labels[i]
            except (TypeError, KeyError):
                label = ' '
        else:
            label = '%d' % int(height)
        ax.text(rect.get_x() + rect.get_width()/2., height_factor*height,
                '{}'.format(label),
                ha='center', va='bottom')


# читаем файл с данными и делаем из него dataframe
dt = pd.read_csv("turkey.csv")


# смотрим года сбора данных и регионы
print(set(dt["PERIOD"]), set(dt["REGION_S"]))

# создаём список лет в dataframe-e
years = []                              # список будет состоять из целочисленных значений
# список с регионами, где ["01-центральный фед. округ", "02-северо-западный фед. округ", "03-южный фед. округ",
#            "04-приволжский фед. округ", "05-уральский фед. округ", "06-сибирский фед. округ",
#            "07-дальневосточ. фед. округ", "08-северо-кавказский фед. округ", "09-крымский фед. округ"]
regions = ["01-ЦФО", "02-СЗФО", "03-ЮФО", "04-ПФО", "05-УФО", "06-СФО", "07-ДФО", "08-СКФО", "09-КФО"]

# заполняем список
for i in dt["PERIOD"]:
    if i not in years:
        years = np.append(years, i)

# берём колонки с информацией по импорту/эспорту и годами
inf = dt.values[:, 0]
date = dt.values[:, 1]
reg = np.array(dt["REGION_S"])

# создаём переменные для подсчёта импорта и экспорта по годам
exp13 = exp14 = exp15 = exp16 = 0
imp13 = imp14 = imp15 = imp16 = 0

# создаем списки для экспорта и импорта по регионам
ereg = [0, 0, 0, 0, 0, 0, 0, 0, 0]
ireg = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# заполняем данные по экспорту и импорту
for i in range(len(inf)):
    if inf[i] == "ЭК":                                   # если текущая позиция - экспорт
        for j in range(len(ereg)):                       # если номер региона равен текущему индексу, увеличиваем
            if int(reg[i][1]) == j + 1:                  # значение на 1
                ereg[j] = ereg[j] + 1
                break

        for case in sw.switch(date[i]):                  # заполняем экспорт по годам
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
        for j in range(len(ireg)):                       # цикл аналогичен циклу в ветви экспорта
            if int(reg[i][1]) == j+1:
                ireg[j] = ireg[j] + 1
                break

        for case in sw.switch(date[i]):                  # заполняем экспорт по годам
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

# считаем общие импорт и экспорт за 2013-2016 года
texp = exp13 + exp14 + exp15 + exp16
timp = imp13 + imp14 + imp15 + imp16

# создаём график общего импорта и экспорта
fig, ax = plt.subplots()
plt.title("total export and import for 2013-2016")
rects1 = plt.bar("export", texp, color="IndianRed")
rects2 = plt.bar("import", timp, color="SkyBlue")

autolabel(rects1)
autolabel(rects2)

plt.savefig("total_exp_imp.png")    # сохраняем график в виде png
plt.show()

# создаём подграфики импорта и экспорта по годам
plt.suptitle("export and import by year")
plt.subplots_adjust(hspace=0.4)     # вертикальный отступ между графиками
plt.subplots_adjust(wspace=0.3)     # горизонтальный отступ между графиками
plt.subplots_adjust(top=0.86)       # отступ от заголовка
# первый график, все последующие графики имеют одинаковые координатные оси благодаря параметрам sharex и sharey
fsp = plt.subplot(2, 2, 1)
plt.ylim(0, 9000)
plt.title("2013")
plt.bar("export", exp13, color="IndianRed")
plt.bar("import", imp13, color="SkyBlue")

# второй график
plt.subplot(2, 2, 2, sharex=fsp, sharey=fsp)
plt.title("2014")
plt.bar("export", exp14, color="IndianRed")
plt.bar("import", imp14, color="SkyBlue")

# третий график
plt.subplot(2, 2, 3, sharex=fsp, sharey=fsp)
plt.title("2015")
plt.bar("export", exp15, color="IndianRed")
plt.bar("import", imp15, color="SkyBlue")

# четвёртый график
plt.subplot(2, 2, 4, sharex=fsp, sharey=fsp)
plt.title("2016")
plt.bar("export", exp16, color="IndianRed")
plt.bar("import", imp16, color="SkyBlue")


plt.savefig("imp_exp_in_years.png")     # сохраняем график в виде png
plt.show()

# создаем график импорта и экспорта по регионам
fig, ax = plt.subplots()
plt.title("import and export across regions")

ind = np.array([x*2 for x in range(len(regions))])           # задаём позиции для пар столбцов
width = 0.75                                                 # задаём ширину столбцов

rects1 = ax.bar(ind + width/2, ireg, width, color='SkyBlue', label='import')    # столбы импорта, располагаются справа
rects2 = ax.bar(ind - width/2, ereg, width, color='IndianRed', label='export')  # столбы экспорта, располагаются слева

plt.xticks(ind)                                 # задаём свою ось Х
ax.set_xticklabels(regions, rotation=60)        # с названиями регионов
plt.margins(0.2)        # расширяем область между осью Х и нижней границей окна
plt.subplots_adjust(bottom=0.17)
plt.ylim(0, 9000)       # задаём предел для оси У
plt.xlim(-2, 18)        # и оси Х

autolabel(rects1)
autolabel(rects2)

plt.legend()
plt.savefig("imp_exp_in_regions.png")       # сохраняем график в виде png
plt.show()
