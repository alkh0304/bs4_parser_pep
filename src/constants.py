from pathlib import Path

PRETTY = 'pretty'
FILE = 'file'

BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / 'logs'
LOGS_FILE = LOGS_DIR / 'parser.log'

TEXT_LOGS_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_LOGS_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

WHATS_NEW_URL = 'https://docs.python.org/3/whatsnew/'
MAIN_DOC_URL = 'https://docs.python.org/3/'
DOWNLOADS_URL = 'https://docs.python.org/3/download.html'
PEP_ZERO_URL = 'https://peps.python.org/'

EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active'],
}
