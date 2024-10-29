Тестирование Кинопоиска
Кинопоиск UI и API тесты - Python
Задача проекта провести проверку модуля поиска (фильм/сериал/персона), возможности авторизации, установки оценки фильму/сериалу. Проект состоит из 5 ui тестов и 5 api тестов.

requirements.txt - файл с используемыми зависимостями в проекте. Установить зависимости на тестовый стенд можно командой pip install -r requirements.txt

config.py- файл с данными, которые используются для авторизации на сайте (логин и пароль), url адреса для ui и api тестов, содержит также информацию о заголовке и токене, передаваемых в api тестах.
gi
test_ui.py - файл с тестами ui. Тесты запускаются командой python -m pytest --alluredir <папка для результатов>. Сформировать отчет allure serve <папка с результатами>.

test_api.py - файл с тестами api. Тесты запускаются командой python -m pytest --alluredir <папка для результатов>. Сформировать отчет allure serve <папка с результатами>.