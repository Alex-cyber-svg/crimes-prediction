import streamlit as st
import requests

st.title("Предсказание преступления по результатам расследования")

months_list = {
    "Январь": 1,
    "Февраль": 2,
    "Март": 3,
    "Апрель": 4,
    "Май": 5,
    "Июнь": 6,
    "Июль": 7,
    "Август": 8,
    "Сентябрь": 9,
    "Октябрь": 10,
    "Декабрь": 11
}

selected_month = st.selectbox("Месяц", options=list(months_list.keys()))
Month = months_list[selected_month]

Latitude = st.slider("Широта", min_value=51.431743, max_value=51.532684, step=0.001, value=51.450000)
Longitude = st.slider("Долгота", min_value=-0.223697, max_value=-0.145363, step=0.001, value=-0.160000)

status_categories = {
    "Действия предпримет другая организация": 0,
    "Ожидание решения суда": 1,
    "Официальные действия не отвечают общественным интересам": 2,
    "Дальнейшие действия не отвечают общественным интересам": 3,
    "Дальнейшее расследование не отвечает общественным интересам": 4,
    "Локальное разрешение": 5,
    "Нарушителю вынесено предупреждение": 6,
    "Нарушителю вынесено предупреждение за хранение наркотиков": 7,
    "Нарушителю выдано уведомление о штрафе": 8,
    "Подозреваемому предъявлены обвинения в рамках другого дела": 9
}

selected_status = st.selectbox("Результат расследования", options=list(status_categories.keys()))
Status_category = status_categories[selected_status]

if st.button("Получить прогноз"):
    data = {
        'Month': Month,
        'Latitude': Latitude,
        'Longitude': Longitude,
        'Status_category': Status_category
    }

    url = 'https://crimes-prediction.onrender.com/predict'
    response = requests.post(url, json=data)

    if response.status_code == 200:
        try:
            data = response.json()
            prediction = data.get('prediction')
            if prediction is not None:
                st.success(f'Прогнозируемое преступление - {prediction}')
            else:
                st.error("Ошибка! Ответ API не содержит прогноз!")
        except:
            st.error("Ошибка! Ответ API не является валидным json!")
    else:
        st.error("Ошибка! API вернул статус: {response.status_code}")