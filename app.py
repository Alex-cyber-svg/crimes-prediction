import streamlit as st
import requests

st.title("Прогноз преступления по результатам расследования")

Month = st.number_input("Месяц (от 1 до 12)", format="%d")
Latitude = st.slider("Широта", min_value=51.431743, max_value=51.532684, value=51.450000)
Longitude = st.slider("Долгота", min_value=-0.223697, max_value=-0.145363, value=-0.160000)
Status_category = st.number_input("Результат расследования", format="%d")

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
                st.subheader('Визуализация прогноза')
                st.bar_chart({"Прогноз":[prediction]})
            else:
                st.error("Ошибка! Ответ API не содержит прогноз!")
        except:
            st.error("Ошибка! Ответ API не является валидным json!")
    else:
        st.error("Ошибка! API вернул статус: {response.status_code}")