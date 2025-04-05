from collections import defaultdict
from typing import List
from pathlib import Path
import re


LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def generate_handlers_report(log_paths: List[Path]) -> None:
    stats = defaultdict(lambda: defaultdict(int))
    total_requests = 0

    pattern = re.compile(
        r'(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL).*?'
        r'(GET|POST|PUT|DELETE|PATCH)?\s*(?P<path>/[^\s]+)'
    )

    for path in log_paths:
        with path.open(encoding='utf-8', errors='ignore') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    level = match.group('level')
                    endpoint = match.group('path')
                    stats[endpoint][level] += 1
                    total_requests += 1

    print(f'Total requests: {total_requests}\n')
    print(f'{'HANDLER':<24}' + ''.join(f'{lvl:<8}' for lvl in LOG_LEVELS))

    endpoints = sorted(stats.keys())
    col_totals = {lvl: 0 for lvl in LOG_LEVELS}

    for ep in endpoints:
        print(f'{ep:<24}', end='')
        for lvl in LOG_LEVELS:
            count = stats[ep].get(lvl, 0)
            col_totals[lvl] += count
            print(f'{count:<8}', end='')
        print()

    print(f'{'':<24}', end='')
    for lvl in LOG_LEVELS:
        print(f'{col_totals[lvl]:<8}', end='')
    print()


def generate_report(log_paths: List[Path], report_name: str) -> None:
    if report_name == 'handlers':
        generate_handlers_report(log_paths)
