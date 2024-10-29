import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
from config import BASE_URL, REGISTER_URL

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.feature("Модуль поиска.")
@allure.title("Тест на поиск фильма или сериала.")
@allure.description("Выполняем поиск фильма или сериала согласно полученным данным.")
@allure.id(2)
@allure.severity("Blocker")
def test_search_film_tv_series(driver):
    film_tv_series = "Интерстеллар"
    
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='kp_query']"))
    )
    search_input.clear()
    search_input.send_keys(film_tv_series)
    search_input.submit()

    with allure.step("Проверяем, что название фильма совпадает с результатами поиска."):
        try:
            film_name_search_list = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#block_left_pad > div > div:nth-child(3) > div > div.info > p > a"))
            )
            all_films = [film.text for film in film_name_search_list]
            print("Результаты поиска:", all_films)

            film_name_result_search = film_name_search_list[0].text
            assert film_tv_series in film_name_result_search, f"Ошибка: '{film_tv_series}' не найдено в '{film_name_result_search}'"
            film_name_search_list[0].click()

            film_name_personal_page = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-tid='75209b22']"))
            ).text

            assert film_name_personal_page.startswith(film_tv_series), f"Ошибка: '{film_name_personal_page}' не начинается с '{film_tv_series}'"

        except TimeoutException as e:
            pytest.fail(f"Не удалось найти результаты поиска: {e}")

@allure.feature("UI Тесты")
@allure.story("Проверка поля ввода логина/email")
def test_login_email_field(driver):
    with allure.step("Открыть страницу входа"):
        driver.get(REGISTER_URL)

    test_emails = [
        ("12345@mail.ru", True),
        ("abb1234@mail.ru", True),
        (".qwerty@mail.ru", False),
        ("qwerty.@mail.ru", False),
    ]

    for email, expected in test_emails:
        with allure.step(f"Ввод логина/email: {email}"):
            login_field = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "passp-field-login"))
            )
            login_field.clear()
            login_field.send_keys(email)

            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "passp:sign-in"))
            )
            submit_button.click()

            if expected:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.ID, "passp-field-passwd"))
                    )
                    back_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div/div/a"))
                    )
                    back_button.click()

                except Exception as e:
                    print(f"Ошибка при проверке корректного email {email}: {e}")

            else:
                try:
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.ID, "passp-field-login"))
                    )
                    assert login_field.get_attribute("aria-invalid") == "true"
                    assert "Некорректный логин или email" in driver.page_source

                except Exception as e:
                    print(f"Ошибка при проверке некорректного email {email}: {e}")

        driver.get(REGISTER_URL)

@allure.feature("UI Тесты")
@allure.story("Проверка поля 'телефон'")
def test_phone_field(driver):
    with allure.step("Открыть страницу регистрации"):
        print(f"Opening URL: {REGISTER_URL}")
        driver.get(REGISTER_URL)

    with allure.step("Выбрать метод ввода 'Телефон'"):
        phone_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div/form/div/div[2]/div[1]/div[2]/button'))
        )
        phone_button.click()

    test_cases = [
        ("", False),
        ("9135135391", True),
        ("25229559999", True),
        ("8976543235", False),
        ("8984894984912", False),
        ("qwertygcvm", False),
        ("!!!!!!!!!!@@@@@", False)
    ]

    for phone, expected in test_cases:
        with allure.step(f"Ввод номера телефона: {phone}"):
            try:
                phone_field = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "passp-field-phone"))
                )
            except TimeoutException:
                print(driver.page_source)
                raise

            phone_field.clear()
            phone_field.send_keys(phone)

            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "passp:sign-in"))
            )
            submit_button.click()

            if not expected:
                error_message = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "field:input-phone:hint"))
                ).text
                assert error_message == "Недопустимый формат номера"

        driver.get(REGISTER_URL)

        with allure.step("Снова выбрать метод ввода 'Телефон'"):
            phone_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div/form/div/div[2]/div[1]/div[2]/button'))
            )
            phone_button.click()

@allure.feature("Модуль поиска.")
@allure.title("Тест на поиск персоны.")
@allure.description("Выполняем поиск персоны согласно полученным данным.")
@allure.id(3)
@allure.severity("Blocker")
def test_search_person(driver):
    person_info = "Николай Караченцов"
    search_person(driver, person_info)
    check_person_info(driver, person_info)

def search_person(driver, person_info):
    search_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='kp_query']"))
    )
    search_input.clear()
    search_input.send_keys(person_info)
    search_input.submit()

def check_person_info(driver, person_info):
    with allure.step("Проверяем, что фамилия и имя персоны совпадают с результатом поиска."):
        try:
            result_text = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.styles_primaryName__2Zu1T"))
            ).text

            assert person_info in result_text, f"Ошибка: '{person_info}' не найден в '{result_text}'"
        except TimeoutException as e:
            pytest.fail(f"Не удалось найти результат поиска: {e}")

@allure.feature("Модуль поиска.")
@allure.title("Тест поиск по несуществующему названию.")
@allure.description("Выполняем поиск по несуществующему названию, проверяем корректность выдачи информационного сообщения.")
@allure.id(4)
@allure.severity("Normal")
def test_empty_search_info_message(driver):
    search_info = "no book such term"
    expected_message = "К сожалению, по вашему запросу ничего не найдено..."

    search_empty_term(driver, search_info)

    get_message = get_empty_search_message(driver)

    print(f"Полученное сообщение: '{get_message}'")

    with allure.step("Проверяем, что считанное информационное сообщение идентично шаблону."):
        assert get_message == expected_message, f"Ошибка: ожидаемое сообщение '{expected_message}', получено '{get_message}'"

def search_empty_term(driver, search_info):
    search_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='kp_query']"))
    )
    search_input.clear()
    search_input.send_keys(search_info)
    search_input.submit()

def get_empty_search_message(driver):
    try:
        message_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.textorangebig"))
        )
        return message_element.text
    except TimeoutException:
        print("Сообщение об ошибке не найдено на странице.")
        return None
