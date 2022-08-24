from pathlib import Path

BASE_DIR = Path(__file__).parent
WHATS_NEW_URL = 'https://docs.python.org/3/whatsnew/'
MAIN_DOC_URL = 'https://docs.python.org/3/'
DOWNLOADS_URL = 'https://docs.python.org/3/download.html'
PEP_ZERO_URL = 'https://peps.python.org/'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
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
