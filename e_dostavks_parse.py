import requests
import bs4
from urllib.parse import urljoin


class EDostavkaParseBase:
    headers = {
        'Accept-Language': 'ru',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    def __init__(self, start_url: str, params: dict) -> None:
        self.start_url = start_url
        self.params = params

    def _get_response(self, url):
        response = requests.get(url, headers=self.headers, params=self.params)
        return response

    def _get_soup(self, url):
        soup = bs4.BeautifulSoup(self._get_response(url).text, "lxml")
        return soup

    def get_task(self, url, callback):
        def task():
            soup = self._get_soup(url)
            return callback(url, soup)

        return task


class CategoryParse(EDostavkaParseBase):
    def __init__(self, start_url: str, search_item: str) -> None:
        super().__init__(start_url=start_url,
                         params={'searchtext': search_item})

        self.tasks = [
            self.get_task(self.start_url, self.rubric_parse)
        ]

    def run(self) -> dict:
        return self.tasks[0]()

    def rubric_parse(self, url, soup):
        raw_data = soup.find(
            'div', {'class': 'item filter_rubric'}).find_all('label')

        return {
            'title': [label.text.strip() for label in raw_data],
            'name': [lable.find('input').get('name') for lable in raw_data],
            'value': [lable.find('input').get('value') for lable in raw_data]
        }


class ItemsParse(EDostavkaParseBase):
    def __init__(self, start_url: str, search_item: str, rubric_name: str, rubric_value: str) -> None:
        super().__init__(start_url=start_url,
                         params={
                             'searchtext': search_item,
                             rubric_name: rubric_value
                         })

        self.tasks = [
            self.get_task(self.start_url, self.items_parse)
        ]

    def run(self) -> dict:
        return self.tasks[0]()

    def __item_parse(self, item: bs4.element.Tag) -> dict:
        return {
            'title': item.find('div', {'class': 'title'}).find('a').text.split(',')[0],
            'price': item.find('div', {'class': 'price'}).text.strip(),
            'image': item.find('div', {'class': 'img'}).find('img').get('src')
        }

    def items_parse(self, url, soup):
        products = soup.find_all('div', {'class': 'products_card'})
        return [self.__item_parse(product) for product in products]


if __name__ == "__main__":
    ItemsParse(
        start_url='https://e-dostavka.by/search',
        search_item='яблоко',
        rubric_name='rubric_filter[7998]',
        rubric_value='7998'
    ).run()
