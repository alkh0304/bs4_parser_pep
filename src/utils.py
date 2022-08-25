import logging

from exceptions import ParserFindTagException, NullResponseException
from requests import RequestException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException as error:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )
        raise NullResponseException(f'Отсутствует ответ от страницы {url}'
                                    f'Ошибка соединения {error}')


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(f'Не найден тег {tag} {attrs}')
    return searched_tag
