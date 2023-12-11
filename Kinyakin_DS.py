# Произведем необходимые импорты
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")






st.set_page_config(page_title='My webpage', page_icon=':tada:', layout='wide')

st.subheader('Hi? i am Vlad :wave:')
st.title('ABOBA')
st.write('BIMBIMBAMBAM')


st.subheader('Получаем нeобходимые для анализа данные')

#-------------загружаем файл-------
data = st.file_uploader("Pick a file")

data = pd.read_csv(data, encoding='utf-8',sep=';')
st.write('Первые пять строк датасета',data.head())



#-----------------график------------------------
st.write('График Распределения количества больничных дней')
st.bar_chart(data['Количество больничных дней'].value_counts())
st.write('Как мы видим, график небольшое сходство с нормальным распределением. Среднее значение равно 3, Максмимальное равно 8, минимальное равно 9')


st.write('График Распределения количества больничных дней')
st.bar_chart(data['Возраст'].value_counts())
st.write('На данном графике мы видим, что распределение похоже на нормальное распределение, среднее равно примерно 40 лет. минимальное около 23, максимальное около 60.')



#-----------Исследование_гипотез----------------
st.title('Гипотеза №1')
st.subheader('Нулевая гипотеза:')

st.write('Мужчины пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще женщин.')


#------------------alpha--------------
alpha = st.slider("Выберите значение для переменной alpha, оно будет поделено на 100", 1, 10)/100
st.write(f'''Критерий независимости хи-квадрат Пирсона. Проверим наличие ссвязи между болезненностью сотрудника и его полом



Установим уровень статистической значимости а={alpha}''')


data_c = data.copy(deep=True)
# Получаем значение Work days
work_days = st.slider("Выберите значение для переменной work days", 0, 7)
st.write('Значение work days = '+str(work_days))
#Производим все необходимые действия с данными
data_c['target'] = (data_c['Количество больничных дней']>work_days)
data_c['target'] = data_c['target'].astype(int)
data_c['Пол'] = data_c['Пол'].replace('М',1).replace('Ж',0)
st.write(f'Построим таблицу сопряженности, она будет выглядить следующим образом при значении work_days={work_days}:')
t = data_c.groupby('Пол')['target'].value_counts().unstack()
t.index = ['Женщины',"Мужчины"]
t.columns = ['Болеют <=2 дней', "Болеют >2 дней"]
st.write(t)


chi2 = round(stats.chi2_contingency(t, correction=False).pvalue,3)

st.subheader(
    f'''
    В таком случае pvalue равно {chi2}
    '''
)

if chi2 <alpha:

    st.write(f'chi2 = {chi2} <{alpha}. Можем отвергнуть нулевую гипотезу в пользу альтернативной')
else:
    st.write(f'chi2 = {chi2} >{alpha}. Мы не можем отвергнуть нулевую гипотезу в пользу альтернативной')

#------------------------------Гипотеза 2_______________________________
st.title('Гипотеза №2')


alpha_1 = st.slider("Выберите значение для переменной alpha, оно будет поделено на 100", 1, 10, key=1)/100
st.write(f'''Критерий независимости хи-квадрат Пирсона. Проверим наличие ссвязи между болезненностью сотрудника и его возрастом
Установим уровень статистической значимости а={alpha_1}''')

work_days_1 = st.slider("Выберите значение для переменной work days", 0, 7,key=3)
st.write('Значение work days = '+str(work_days_1))
# Получаем значение Age
age = st.slider("Выберите значение для переменной age", 23, 60)
st.write('Значение age = '+str(age))
#Производим все необходимые действия с данными

data_c_2 = data.copy(deep=True)
data_c_2['target'] = (data_c_2['Количество больничных дней']>work_days_1)
data_c_2['target'] = data_c_2['target'].astype(int)
data_c_2['Возраст'] = data_c_2['Возраст'].where(data_c_2['Возраст'] > age, 1).where(data_c_2['Возраст'] <= age, 0)
t_2 = data_c_2.groupby('Возраст')['target'].value_counts().unstack()
t_2.index = ['Младше 35',"Старше 35"]
t_2.columns = ['Болеют <=2 дней', "Болеют >2 дней"]
st.write(t_2)




chi2_1 = round(stats.chi2_contingency(t_2, correction=False).pvalue,3)

st.subheader(
    f'''
    В таком случае pvalue равно {chi2_1}
    '''
)

if chi2_1 <alpha:

    st.write(f'chi2 = {chi2_1} <{alpha_1}. Можем отвергнуть нулевую гипотезу в пользу альтернативной')
else:
    st.write(f'chi2 = {chi2_1} >{alpha_1}. Мы не можем отвергнуть нулевую гипотезу в пользу альтернативной')
