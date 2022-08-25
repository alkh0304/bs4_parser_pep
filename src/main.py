import logging
import re
import requests_cache

from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_ZERO_URL,
    WHATS_NEW_URL, DOWNLOADS_URL
)
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_response


def make_soup(session, url):
    response = session.get(url)
    response.encoding = 'utf-8'
    response = get_response(session, url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    return soup


def whats_new(session):
    soup = make_soup(session, WHATS_NEW_URL)
    sections_by_python = soup.select(
        'what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(WHATS_NEW_URL, href)
        soup = make_soup(session, version_link)
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    soup = make_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        error_message = 'Ничего не нашлось'
        logging.error(error_message)
        raise ParserFindTagException(error_message)
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    soup = make_soup(session, DOWNLOADS_URL)
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(DOWNLOADS_URL, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    soup = make_soup(session, PEP_ZERO_URL)
    numerical_index = find_tag(soup, 'section', {'id': 'numerical-index'})
    tbody = find_tag(numerical_index, 'tbody')
    tr = tbody.find_all('tr')
    pep_count = 0
    status_count = {}
    results = [('Статус', 'Количество')]
    for pep in tqdm(tr):
        pep_count += 1
        status_short = pep.find('td').text[1:]
        if status_short in EXPECTED_STATUS:
            status_long = EXPECTED_STATUS[status_short]
        else:
            status_long = []
            logging.info(
                f'В списке есть неверно указанный статус: {status_short}'
                f'В строке: {pep}'
            )
        pep_link_short = pep.find('a')['href']
        pep_link_full = urljoin(PEP_ZERO_URL, pep_link_short)
        soup = make_soup(session, pep_link_full)
        dl_table = find_tag(soup, 'dl', {'class': 'rfc2822 field-list simple'})
        status_line = dl_table.find(string='Status')
        if status_line:
            status_parent = status_line.find_parent()
            status_page = status_parent.next_sibling.next_sibling.string
            if status_page not in status_long:
                logging.info(
                    f'Несовпали статусы PEP: {pep_link_full}'
                    f'Статус на странице - {status_page}'
                    f'Статус в списке - {status_long}'
                )
            if status_page in status_count:
                status_count[status_page] += 1
            else:
                status_count[status_page] = 1
        else:
            logging.error(
                f'На странице PEP {pep_link_full}'
                'В таблице нет строки статуса.'
            )
            continue
    results.extend(status_count.items())
    results.append(('Total', pep_count))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception:
        logging.exception(
            'Возникла ошибка в ходе работы парсера.', stack_info=True)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
