import streamlit as st


def main():
    st.title("Описание проекта")

    st.markdown("""
    Это веб-приложение предоставляет несколько функций:

    1. **Регистрация и Авторизация:** Пользователь может зарегистрироваться, войти в систему и переключаться между регистрацией и авторизацией.

    2. **Предсказание категории товара:** Пользователь вводит название товара, выбирает модель из списка и получает предсказание категории товара вместе со списком рекомендованных товаров.

    ## Инструкции по использованию:

    1. **Регистрация и Авторизация:**
        - Нажмите кнопку "Регистрация" или "Авторизация" в верхней части страницы.
        - Введите необходимые данные (имя пользователя, email, пароль) и следуйте инструкциям.

    2. **Предсказание категории товара:**
        - В разделе "Предсказание категории товара" введите название товара.
        - Выберите модель из выпадающего списка.
        - Нажмите кнопку "Определить категорию".
        - Получите результат предсказания.

    ## О проекте:

    Этот проект создан с использованием библиотеки Streamlit с целью предоставить простой интерфейс для регистрации, авторизации и предсказания категории товара на основе ml-моделей.

    Автор: Шухман Арина
    """)


if __name__ == "__main__":
    main()