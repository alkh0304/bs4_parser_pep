import argparse
import logging

from logging.handlers import RotatingFileHandler

from constants import (
    PRETTY, FILE, LOGS_DIR, LOGS_FILE, TEXT_LOGS_FORMAT, DT_LOGS_FORMAT
)


def configure_argument_parser(available_modes):
    parser = argparse.ArgumentParser(description='Парсер документации Python')
    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=(PRETTY, FILE),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging():
    log_dir = LOGS_DIR
    log_dir.mkdir(exist_ok=True)
    log_file = LOGS_FILE
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_LOGS_FORMAT,
        format=TEXT_LOGS_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
