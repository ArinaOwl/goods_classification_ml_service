import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

def is_user_logged_in():
    return "logged_in" in st.session_state and st.session_state.logged_in

def clear_session_state():
    st.session_state.logged_in = False
    st.session_state.access_token = None

def get_access_token():
    return st.session_state.access_token

def registration_form_callback():
    email = st.session_state.email
    password = st.session_state.password
    confirm_password = st.session_state.confirm_password

    if password != confirm_password:
        st.error(f"Ошибка при регистрации: Введенные пароли не совпадают")
    else:
        # Отправляем запрос на регистрацию
        data = {"email": email, "password": password, "credits": 1000}
        response = requests.post(f"{API_BASE_URL}/auth/register", json=data)

        if response.status_code == 201:
            st.success("Регистрация успешна!")
        else:
            st.error(f"Ошибка при регистрации: {response.text}")

def registration_form():
    st.subheader("Регистрация")
    with st.form("registration_form"):
        st.text_input("Email", key='email')
        st.text_input("Пароль", type="password", key='password')
        st.text_input("Подтвердите пароль", type="password", key='confirm_password')
        st.form_submit_button("Зарегистрироваться", on_click=registration_form_callback)

def login_form_callback():
    email = st.session_state.email
    password = st.session_state.password

    # Отправляем запрос на авторизацию
    data = {"username": email, "password": password}
    response = requests.post(f"{API_BASE_URL}/auth/jwt/login", data=data)

    if response.status_code == 200:
        st.session_state["logged_in"] = True
        st.session_state["access_token"] = response.json()["access_token"]
        st.success("Вход выполнен успешно!")
    else:
        st.error(f"Ошибка при входе: {response.text}")

def login_form():
    st.subheader("Авторизация")
    with st.form("login_form"):
        st.text_input("Email", key='email')
        st.text_input("Пароль", type="password", key='password')
        st.form_submit_button("Войти", on_click=login_form_callback)

def get_balance():
    # Получаем баланс пользователя
    access_token = get_access_token()
    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_BASE_URL}/balance", headers=headers)

        if response.status_code == 200:
            return response.json()["balance"]
        else:
            st.error(f"Ошибка при получении баланса: {response.text}")
            return None
    else:
        st.error("Ошибка: Пользователь не аутентифицирован")
        return None

def show_user_dashboard():
    user_balance = get_balance()
    if user_balance is not None:
        st.write(f"Баланс кредитов: {user_balance}")
        if st.button("Выйти"):
            # Выход пользователя
            access_token = get_access_token()
            if access_token:
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.post(f"{API_BASE_URL}/auth/jwt/logout", headers=headers)
                if response.status_code == 204:
                    clear_session_state()
                    st.success("Выход выполнен успешно!")
                else:
                    st.error(f"Ошибка при выходе: {response.text}")
            else:
                st.error("Ошибка: Пользователь не аутентифицирован")

def show_auth_form():
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        reg_button = st.button("Регистрация")

    with col2:
        auth_button = st.button("Авторизация")

    if reg_button:
        registration_form()
    if auth_button:
        login_form()

def main():
    st.subheader("Личный кабинет")

    # Инициализация состояния сессии
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["access_token"] = None

    # Отображение контента в зависимости от статуса входа
    if is_user_logged_in():
        show_user_dashboard()

    else:
        show_auth_form()


if __name__ == "__main__":
    main()
