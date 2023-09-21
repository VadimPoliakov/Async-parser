import httpx
import asyncio
import requests
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup
from pandas import DataFrame
from fake_useragent import UserAgent
from itertools import chain

# фейковый юзер агент для имитации посещения страницы человеком
ua = UserAgent()
user_agent = ua.random
headers = {"User-Agent": user_agent}



async def get_links(url: str) -> list:
    """
    Получает ссылки на каждый товар с каждой страницы категории.

    Args:
        url (str): URL категории.

    Returns:
        list: Список ссылок на товары из категории.
    """
    try:
        async with httpx.AsyncClient() as client:
            # обращаемся к категории
            r = await client.get(url + "1", headers=headers, timeout=3)
            await asyncio.sleep(1)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                try:
                    # проверяем на количество страниц в категории
                    pages = soup.findAll("li", class_="pagination-item").text
                    pages = max(i for i in pages if int(i) == i)
                except AttributeError:
                    pages = 1
                # проходимся одновременно по всем страницам категории и собираем ссылки
                links = await asyncio.gather(
                    *(link_parser(url, page) for page in range(1, pages + 1)),
                    return_exceptions=True)
                print("Категория ", url, " готова")
                # возвращаем ссылки на все товары из категории
                return list(chain(*links))
    except ConnectTimeout:
        print('Request has timed out')



async def link_parser(url: str, page: int) -> list:
    """
    Получает ссылки с конкретной страницы.

    Args:
        url (str): URL категории.
        page (int): Номер страницы.

    Returns:
        list: Список ссылок на товары с текущей страницы.
    """

    links_list = []
    async with httpx.AsyncClient() as client:
        r = await client.get(url + str(page))
        await asyncio.sleep(1)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
            links = soup.findAll("div", class_="product-card")
            for link in links:
                links_list.append(link.find("a").get("href"))
            print("Страница ", page, " готова")
            return links_list



async def parser(url: str) -> None:
    """
    Парсит все товары с переданной категории.

    Args:
        url (str): URL категории.

    Returns:
        None
    """

    # получаем ссылки на каждый товар с каждой страницы категории
    links = await get_links(url)
    if len(links) > 0:
        for link in links:
            data = []
            link = "https://www.art-lamps.ru" + link
            # парсим каждый товар из категории ПОСЛЕДОВАТЕЛЬНО и записываем в таблицу
            try:
                """
                async with httpx.AsyncClient() as client:
                    r = await client.get(link, headers=headers, timeout=3)
                    await asyncio.sleep(1)

                Для полной асинхронности и одновременного скачивания всех товаров:
                убрать документацию
                сдвинуть весь код до except на один таб
                удалить/закомментировать отмеченный код

                Сейчас асинхронно работает по категориям, то есть
                каждая категория обрабатывается параллельно, а товары в них последовательно

                Полностью асинхронно делать не рекомендуется из-за нестабильной работы и 
                большой нагрузки на сайт
                """

                # удалить для полной асинхронности
                r = requests.get(link, headers=headers, timeout=3)
                await asyncio.sleep(1)
                # удалить для полной асинхронности

                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, "lxml")
                    name = soup.find("h1", class_="js-product-title").text
                    price = soup.find("div", class_="price js-product-price").text
                    description = soup.find("div", id="product-description") \
                        .find("div", class_="editor").get_text()
                    short_description = soup.find("div", class_="product-introtext") \
                        .get_text()
                    images = []
                    pictures = soup.findAll("div", class_="slide-inner with-object-fit")
                    for picture in pictures:
                        images.append(picture.find("img").get("src"))
                    images = " ".join(images)
                    vendor_code = soup.find("div", class_="article-value cell-xl-9").text
                    data.append([vendor_code, name, price, description, short_description, images])
                    print("Товар ", name, " готов")
                    df = DataFrame(data)
                    df.to_csv("art.csv", mode="a", index=False, sep=";", encoding="utf-8", header=False)
            except ConnectTimeout:
                print('Request has timed out')


async def main() -> None:
    url = "https://www.art-lamps.ru"
    columns = ["Артикул",
               "Имя",
               "Цена",
               "Описание",
               "Краткое описание",
               "Изображения"]
    df = DataFrame(columns=columns)
    df.to_csv("art.csv", index=False, sep=";", encoding="utf8")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    # парсим все категории с сайта
    categories = soup.find("ul", "collection-menu-horizontal list js-edge-calc").findAll("li", "menu-item")

    # одновременно проходимся по всем категориям
    await asyncio.gather(
        *(parser(url + category.find("a").get("href") + "?page=") for category in categories),
        return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
