import pytest
from pathlib import Path
from io import StringIO
from unittest.mock import patch

from utils import check_files_exist
from report_handlers import generate_handlers_report


def test_check_files_exist_existing_file():
    valid_path = Path('valid_file.log')
    valid_path.touch()
    try:
        check_files_exist([valid_path])
    finally:
        valid_path.unlink()


def test_check_files_exist_non_existing_file():
    invalid_path = Path('non_valid_file.log')
    with pytest.raises(SystemExit):
        check_files_exist([invalid_path])


@patch('sys.stdout', new_callable=StringIO)
def test_generate_handlers_report(mock_stdout):
    log_content = '''
2025-03-28 12:09:06,000 ERROR django.request: Internal Server Error: /api/v1/support/ [192.168.1.84] - DatabaseError: Deadlock detected
2025-03-28 12:10:06,000 INFO django.request: GET /api/v1/users/ [192.168.1.85]
'''
    log_path = Path('test_log.log')
    log_path.write_text(log_content)

    try:
        generate_handlers_report([log_path])
        output = mock_stdout.getvalue()
        assert 'Total requests: 2' in output
        assert '/api/v1/support/' in output
        assert '/api/v1/users/' in output
    finally:
        log_path.unlink()
