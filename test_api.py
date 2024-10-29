import requests
import pytest
import allure
from config import API_BASE_URL, API_TOKEN, HEADERS

@allure.feature("API Тесты")
@allure.story("Поиск фильма по ID")
def test_get_movie_by_id():
    movie_id = 456
    response = requests.get(f"{API_BASE_URL}/movie/{movie_id}", headers=HEADERS)
    with allure.step("Проверка, что код ответа 200"):
        assert response.status_code == 200
    with allure.step("Проверка структуры данных"):
        assert "id" in response.json()

@allure.feature("API Тесты")
@allure.story("Поиск фильма по названию")
def test_search_movie_by_title():
    movie_title = "The Matrix" 
    params = {"name": movie_title}
    
    response = requests.get(f"{API_BASE_URL}/movie/search", params=params, headers=HEADERS)

    with allure.step("Проверка, что код ответа 200"):
        assert response.status_code == 200, f"Ошибка: {response.status_code}, Ответ: {response.text}"

    with allure.step("Проверка структуры данных"):
        response_data = response.json()
        assert "docs" in response_data, "Ответ не содержит список фильмов"
        assert isinstance(response_data["docs"], list), "Фильмы должны быть в виде списка"


@allure.feature("API Тесты")
@allure.story("Поиск актера по ID")
def test_get_actor_by_id():
    actor_id = 5661548
    response = requests.get(f"{API_BASE_URL}/person/{actor_id}", headers=HEADERS)
    with allure.step("Проверка, что код ответа 200"):
        assert response.status_code == 200
    with allure.step("Проверка структуры данных"):
        assert "id" in response.json()

@allure.feature("API Тесты")
@allure.story("Поиск фильма по параметрам")
def test_search_movie_by_year_genre_country():
    params = {
        "year": 1934,
        "genres.name": "ужасы",
        "countries.name": "Мексика"
    }
    response = requests.get(f"{API_BASE_URL}/movie", params=params, headers=HEADERS)
    with allure.step("Проверка, что код ответа 200"):
        assert response.status_code == 200
    with allure.step("Проверка структуры данных"):
        assert "docs" in response.json()

@allure.feature("API Тесты")
@allure.story("Поиск отзывов")
def test_get_reviews():
    params = {
        "page": 1,
        "limit": 3,
        "createdAt": "27.05.2024-27.06.2024"
    }
    response = requests.get(f"{API_BASE_URL}/review", params=params, headers=HEADERS)
    with allure.step("Проверка, что код ответа 200"):
        assert response.status_code == 200
    with allure.step("Проверка структуры данных"):
        assert "docs" in response.json()
