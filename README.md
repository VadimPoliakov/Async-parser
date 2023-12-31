# Скрипт для веб-скрапинга

Этот скрипт на Python разработан для сбора данных с веб-сайта. Он использует различные библиотеки и методики для извлечения информации с конкретного сайта и сохранения ее в CSV-файл.

## Особенности

- Асинхронно получает ссылки на продукты из разных категорий на веб-сайте.
- Парсит детали продуктов, включая название, цену, описание и изображения.
- Сохраняет собранные данные в CSV-файле.

## Предварительные требования

Перед использованием этого скрипта убедитесь, что у вас установлены следующие предварительные требования:

- Python
- Необходимые библиотеки Python (установите с помощью `pip install -r requirements.txt`):
  - httpx
  - requests
  - beautifulsoup4
  - pandas
  - fake_useragent

## Использование

1. Клонируйте этот репозиторий на свой локальный компьютер.


git clone https://github.com/VadimPoliakov/Async-parser.git


2. Установите необходимые библиотеки Python с помощью pip.


pip install -r requirements.txt


3. Отредактируйте скрипт по мере необходимости под вашу конкретную задачу.

4. Запустите скрипт:


python main.py


Скрипт начнет сбор данных с указанного веб-сайта и сохранит их в CSV-файл с именем "art.csv" в той же папке.

## Примечания

- Этот скрипт использует асинхронное программирование для повышения производительности. Вы можете настроить уровень параллелизма, изменив код.

- Обязательно соблюдайте условия использования и политику скрапинга веб-сайта при использовании этого скрипта.
