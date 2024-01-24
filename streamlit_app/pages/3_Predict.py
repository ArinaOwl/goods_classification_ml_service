import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"


# Функция для предсказания категории
def predict_category(product_name, selected_model):
    # Ваш код для предсказания категории на основе выбранной модели
    # Здесь вам нужно вставить соответствующий код для ваших ml-моделей
    # Возвращаемые данные: категория и список товаров в этой категории
    category = "Некоторая категория"
    return category


def get_access_token():
    return st.session_state.access_token


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


def decrease_user_credits(user_balance, access_token):
    if user_balance > 0:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_BASE_URL}/users/me", headers=headers)
        if response.status_code == 200:
            data = response.json()
            data["credits"] = user_balance - 1
            response = requests.patch(f"{API_BASE_URL}/users/me", headers=headers, json=data)
            if response.status_code != 200:
                st.error(response.json()["detail"])
        else:
            st.error(response.json()["detail"])
    else:
        raise ValueError("Недостаточно кредитов")


def main():
    st.title("Предсказание категории товара")

    st.subheader("Стоимость:")
    st.markdown("**Classifier implementing the k-nearest neighbors vote** (k_neighbors): 1 кредит")
    st.markdown("**Multi-layer Perceptron classifier** (mlp): 10 кредитов")

    # Получаем название товара от пользователя
    product_name = st.text_input("Введите название товара:")

    # Выбираем модель для предсказания
    selected_model = st.selectbox("Выберите модель:", ["k_neighbors", "mlp"])

    # Кнопка для выполнения предсказания
    if st.button("Определить категорию"):
        if product_name:
            user_balance = get_balance()
            access_token = get_access_token()
            if user_balance and access_token:
                headers = {"Authorization": f"Bearer {access_token}"}
                data = {"product_name": product_name, "classifier_name": selected_model, "user_balance": user_balance}
                response = requests.get(f"{API_BASE_URL}/predict", headers=headers, json=data)

                if response.status_code == 200:
                    category = response.json()['category']
                    balance = response.json()['balance']
                    data = {"credits": balance}
                    response = requests.patch(f"{API_BASE_URL}/users/me", headers=headers, json=data)
                    if response.status_code != 200:
                        st.error(response.json()["detail"])
                    else:
                        st.subheader("Результат предсказания:")
                        st.write(f"Категория товара: {category}")
                        st.subheader(f"Баланс кредитов: {balance}")
                else:
                    st.error(f"Ошибка при предсказании категории товара: {response.text}")
            else:
                st.error("Ошибка: Пользователь не аутентифицирован")
        else:
            st.warning("Пожалуйста, введите название товара.")


if __name__ == "__main__":
    main()
