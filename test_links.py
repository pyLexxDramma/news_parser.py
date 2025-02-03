import unittest
import feedparser
import requests

class TestRSSParser(unittest.TestCase):
    def setUp(self):
        # Список RSS-лент для тестирования
        self.rss_links = {
    "Общие новости": [
        "https://lenta.ru/rss/",
        "https://ria.ru/export/rss2/index.xml",
        "https://tass.ru/rss/v2.xml",
        "https://www.interfax.ru/rss.asp",
        "https://www.kommersant.ru/RSS/main.xml"
    ],
    "Новости (отдельная категория)": [
        "https://lenta.ru/rss/news/",
        "https://www.kommersant.ru/RSS/news.xml"
    ],
    "Статьи": [
        "https://lenta.ru/rss/articles/",
        "https://habr.com/ru/rss/articles/"
    ],
    "Технологии": [
       "https://habr.com/ru/rss/all/",
       "https://habr.com/ru/rss/news/",
        "https://www.opennet.ru/opennews/opennews_all.rss"
    ]
}

    def test_rss_parsing(self):
        successful_links = []

        for source, urls in self.rss_links.items():
            for url in urls:
                with self.subTest(url=url):
                    # Проверка доступности URL
                    try:
                        response = requests.head(url)
                        response.raise_for_status()  # Генерирует исключение для 4xx и 5xx
                    except requests.RequestException as e:
                        print(f"URL не доступен: {url}. Ошибка: {e}")
                        continue

                    # Парсинг RSS-ленты
                    try:
                        feed = feedparser.parse(url)
                        self.assertEqual(feed.bozo, 0, f"Не удалось распарсить RSS-ленту: {url}")
                        successful_links.append((source, url))  # Сохраняем успешные ссылки
                    except Exception as e:
                        print(f"Ошибка при парсинге {url}: {e}")

        # Выводим успешные ссылки
        print("\nУспешно распарсенные ссылки:")
        for source, url in successful_links:
            print(f"{source}: {url}")

if __name__ == "__main__":
    unittest.main()
