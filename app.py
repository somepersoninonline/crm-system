import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- 1. Настройка страницы ---
st.set_page_config(page_title="My Resell CRM", page_icon="💸", layout="wide")

# --- 2. Твой Ключ (Вшит здесь) ---
creds_dict = {
  "type": "service_account",
  "project_id": "skilled-booking-482818-h2",
  "private_key_id": "94bd30329bbf5dc487f6a49908d41f9b7c7e58c9",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCMzu3O5/acTOL7\nQHLf5+eMuYvlE/5CHV7rSn4zNOw+/ldlnA9yeXQw9U0IUauCNwVu/uJqb/WzPrBG\nqTs3sUujs7bD9uNAbgT4nWMCDRjAooAX3iTjK1eaUPfd9DJ6S0IzoBba2suHOkft\n1JqJD8wNRiyHpdYkM/QtCA54RfNMMHa1roipgOIxucCnCRCUtENZuLkjXr716qDF\nk+u57XWemvrLWH9nDnDuuzEleAPr2CEmOmXMF9R7j/oje2C4+SvJGcOYEZJR2pYt\nXNEd3lLOV7Xyj+RSzwDzLpV+PV4t0ESYSntb3X/7giM36a3Dj12BC2zZra+vTu0C\nqQd/UG5LAgMBAAECggEAM15AQkW8YVvpSHjED6wV/HAqOXl4Pd1iJdtIu9yYPQjj\nkFWFCyGEwmGS5zCILZpt+IayydqrW2dIvpZ5XIFpE0D6MXZthDE+zgX4uyRU/d2q\ndkqb0WYb8NeN/WJbUeMHtTa3b8L3Eg+wcvKnJ85kBgmuMBRPUWjEsPLp+HWoYwgW\neg4QVk2eOgsV5DwSMP4z1zC4g2VUDegcc0lcxvVAUpJvXtCu4ROxWK9IY4uXIsiy\nhtRFPX3zsCGHyYkwp9Tt9aNPoJc70wqE0F7Rb3+bW/ZGfSA9iqSjEsiGJU29ffqg\ncF0pDpfH9RbMkasNxT1gsd/S30C8yvo2iDyly3OTIQKBgQDFv01jY+AeSfzcSvzi\nPvVHVMEExwSXT2OtdNTus0/ncN9kLfFradR0j6IL+S2ARqs5RplzWyVhbQpPACIi\nF+sDTUSI8QlcMs2qAy7G6lhielhQ4iLfUHe0qKWvxAcJZfWOAIce3xquQHQoTLdR\nU3rmc8rPaisrqk32ttz4veKUawKBgQC2SbGqxN70O1PwG4vLLBWWoZ9zg9O3sMMB\nQ1ThwByXZPLS02Ok7aV2i5TDK1EhKLlboGc0xtGuvqcTpddNRtgDOe5II70DfOy6\nBdT0o2p/PCETYhWFgs67fUFNcSVCoQ9R7Sz7FX6O+IuDV9xAiqpAuCINnJ0r58L0\nddUw14EFoQKBgEyc/G+ob1ls0vHKf8VsHP2A4bNnI+k3kefPHvxILon9mh8nCaTT\nAMQULfUzmiRbvNTY/HTL+GSRqW/IHnFVEPFbi1T/BeBZsoLO7t2UR6AHxJW5t0cL\n1wUAXgkGCq/id8uHetJEIAMo55gBePiiPjhw3j+T45vsRH50hJI+hz13AoGAZuh3\nmpaF349Wtah3ZP3AOkeIAuibL4pkrGPcmY2hFn7w7sBT8poO3TuzgfMEXBnneqi1\nWwAbA/Gx1M+9Gm0yKbAcqzEx1bRC2EnOjUVsK+RAL/chezv7hbESmquTg2f1hCTH\nTgA2cHQ0HrQNLYqazuqkntaZjF3Mm8Gh127x8cECgYAFx9vuhs4y1a/DBPRVI6aU\nVO2npQS+L67JE0hBW6HxFVFcP6Cr6I4JG5wXvInjTR4XNEJhxKzqKuWH8d7NW7Xh\n4XugHniqV6qmMhi02GR6XasVX9roRpTOYkNpJLERAqXlWYh8yQddAUwUgE51g7Sx\nfTzyCXRu0L5wO2SBorHWBw==\n-----END PRIVATE KEY-----\n",
  "client_email": "bot-191@skilled-booking-482818-h2.iam.gserviceaccount.com",
  "client_id": "116070386511267179413",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-191%40skilled-booking-482818-h2.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Ссылка на таблицу
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BT8z-LaDTUe8RzKwfJYafXteDjFeUKgz6U6N-EB9PTw/edit?gid=0#gid=0"

# --- 3. Функция Подключения (Напрямую к Google) ---
def get_google_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    # Открываем таблицу и берем первый лист
    return client.open_by_url(SHEET_URL).get_worksheet(0)

# --- Приложение ---
def main_app():
    with st.sidebar:
        st.title("Меню")
        page = st.radio("Навигация", ["Главная", "Добавить продажу", "Вся база"])
        if st.button("Обновить 🔄"):
            st.cache_data.clear()
            st.rerun()

    # Загрузка данных
    try:
        ws = get_google_sheet()
        data = ws.get_all_records()
        df = pd.DataFrame(data)
    except Exception as e:
        st.error(f"Ошибка подключения: {e}")
        df = pd.DataFrame()

    if page == "Главная":
        st.title("📊 Статистика")
        if not df.empty:
            # Превращаем числа из текста в цифры (на всякий случай)
            df['profit'] = pd.to_numeric(df['profit'], errors='coerce').fillna(0)
            df['sell_price'] = pd.to_numeric(df['sell_price'], errors='coerce').fillna(0)
            
            c1, c2 = st.columns(2)
            c1.metric("Прибыль", f"{df['profit'].sum():,.0f}")
            c2.metric("Оборот", f"{df['sell_price'].sum():,.0f}")
            st.dataframe(df.tail(5))
        else:
            st.info("База пуста. Добавь первую запись!")

    elif page == "Добавить продажу":
        st.title("➕ Новая запись")
        with st.form("add"):
            name = st.text_input("Товар")
            c1, c2 = st.columns(2)
            buy = c1.number_input("Закуп", step=100.0)
            sell = c2.number_input("Продажа", step=100.0)
            status = st.selectbox("Статус", ["В наличии", "Продано", "Возврат"])
            is_ref = st.checkbox("Рефанд?")
            comm = st.text_area("Инфо")
            
            if st.form_submit_button("Сохранить"):
                profit = sell - buy if not is_ref else sell
                
                # Подготовка строки для Google Sheets (список значений)
                new_row = [name, buy, sell, str(is_ref), status, comm, profit]
                
                # Пишем напрямую в таблицу
                ws = get_google_sheet()
                ws.append_row(new_row)
                
                st.success("Готово! Записано напрямую в Google! ✅")

    elif page == "Вся база":
        st.title("🗄 База данных")
        st.dataframe(df)

def login():
    st.title("🔒 Вход")
    if st.button("Войти как Админ"):
        st.session_state.logged_in = True
        st.rerun()

if __name__ == '__main__':
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    if st.session_state.logged_in: main_app()
    else: login()
