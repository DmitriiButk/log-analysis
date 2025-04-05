from pathlib import Path
import sys

from report_handlers import generate_report
from utils import check_files_exist, check_report_valid


def main() -> None:
    args = sys.argv[1:]

    report_index = args.index('--report') if '--report' in args else None
    log_files = args[:report_index] if report_index else args
    report_name = args[report_index + 1] if report_index else None

    log_paths = [Path(file) for file in log_files]
    check_files_exist(log_paths)

    if report_name:
        check_report_valid(report_name)

    generate_report(log_paths, report_name)


if __name__ == '__main__':
    main()
