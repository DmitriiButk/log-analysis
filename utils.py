import sys
from pathlib import Path
from typing import List


VALID_REPORTS = ['handlers']


def check_files_exist(log_paths: List[Path]) -> None:
    for path in log_paths:
        if not path.exists():
            print(f'Error: файл не существует: {path}')
            sys.exit(1)


def check_report_valid(report_name: str) -> None:
    if report_name not in VALID_REPORTS:
        print(f'Error: Некорректное имя отчёта: {report_name}')
        print(f'Доступные отчёты: {', '.join(VALID_REPORTS)}')
        sys.exit(1)
