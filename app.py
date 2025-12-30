import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- ПАРОЛЬ ---
PASSWORD = "admin"

# --- РАБОТА С GOOGLE SHEETS ---
def get_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        # ttl=0 чтобы данные обновлялись мгновенно
        df = conn.read(ttl=0) 
        return df
    except:
        return pd.DataFrame()

def add_entry(item_name, buy_price, sell_price, is_refunded, status, comment):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = get_data()
    
    # Считаем профит
    real_cost = 0 if is_refunded else buy_price
    profit = sell_price - real_cost
    
    # Создаем новую строку
    new_row = pd.DataFrame([{
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "item_name": item_name,
        "buy_price": buy_price,
        "sell_price": sell_price,
        "is_refunded": is_refunded,
        "status": status,
        "comment": comment,
        "profit": profit
    }])
    
    # Добавляем в общую кучу
    updated_df = pd.concat([df, new_row], ignore_index=True)
    # Обновляем Google Таблицу
    conn.update(data=updated_df)

# --- ИНТЕРФЕЙС ---
st.set_page_config(page_title="My Resell CRM", page_icon="💸", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔒 Вход в систему")
    pwd = st.text_input("Пароль", type="password")
    if st.button("Войти"):
        if pwd == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Неверно")

def main_app():
    st.sidebar.title("Меню")
    page = st.sidebar.radio("Перейти:", ["Главная", "Добавить продажу", "Вся база"])
    
    # Кнопка ручного обновления на всякий случай
    if st.sidebar.button("Обновить данные 🔄"):
        st.cache_data.clear()
        st.rerun()

    df = get_data()

    if page == "Главная":
        st.title("📈 Твоя Статистика")
        if not df.empty:
            # Превращаем колонки в цифры, чтобы считать сумму
            df['profit'] = pd.to_numeric(df['profit'], errors='coerce').fillna(0)
            df['sell_price'] = pd.to_numeric(df['sell_price'], errors='coerce').fillna(0)
            
            total_profit = df['profit'].sum()
            total_sales = df['sell_price'].sum()
            
            c1, c2 = st.columns(2)
            c1.metric("💰 Чистый Профит", f"{total_profit:,.0f}")
            c2.metric("💳 Оборот", f"{total_sales:,.0f}")
            
            st.divider()
            st.subheader("Последние записи")
            st.dataframe(df.tail(5))
        else:
            st.info("База пуста. Добавь первую продажу!")

    elif page == "Добавить продажу":
        st.title("➕ Добавить товар")
        with st.form("add"):
            name = st.text_input("Название (Что продал?)")
            c1, c2 = st.columns(2)
            buy = c1.number_input("Купил за", min_value=0.0, step=100.0)
            sell = c2.number_input("Продал за", min_value=0.0, step=100.0)
            status = st.selectbox("Статус", ["В наличии", "Продано", "Возврат"])
            is_ref = st.checkbox("Был Рефанд? (Покупка = 0)")
            comm = st.text_area("Заметка")
            
            if st.form_submit_button("Сохранить"):
                add_entry(name, buy, sell, is_ref, status, comm)
                st.success("Сохранено в Google Таблицу! ✅")

    elif page == "Вся база":
        st.title("📋 Все записи")
        st.dataframe(df)

if __name__ == '__main__':
    if st.session_state.logged_in:
        main_app()
    else:
        login()
