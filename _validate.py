import csv
import re
import sys
from pathlib import Path

EXPECTED_HEADERS = ["name", "path", "arguments", "file_types", "os", "group_name"]
VALID_FILE_TYPES = {"TEXT", "IMAGE", "TEXT_AND_IMAGE"}
VALID_OS = {"Mac", "Windows", "Linux"}
SCREAMING_SNAKE_RE = re.compile(r"^[A-Z][A-Z0-9]*(_[A-Z0-9]+)*$")

def main():
    errors = []

    with Path("diff_reporters.csv").open(newline="") as f:
        reader = csv.reader(f, strict=True)
        headers = next(reader)

        if headers != EXPECTED_HEADERS:
            errors.append(f"Header mismatch: expected {EXPECTED_HEADERS}, got {headers}")

        seen = set()
        for line_num, row in enumerate(reader, start=2):
            if all(cell == "" for cell in row):
                continue

            if len(row) != len(EXPECTED_HEADERS):
                errors.append(f"Line {line_num}: expected {len(EXPECTED_HEADERS)} columns, got {len(row)}")
                continue

            name, path, arguments, file_types, os_, group_name = row

            if not name:
                errors.append(f"Line {line_num}: name is empty")
            elif not SCREAMING_SNAKE_RE.match(name):
                errors.append(f"Line {line_num}: name '{name}' is not SCREAMING_SNAKE_CASE")

            if not path:
                errors.append(f"Line {line_num}: path is empty")

            if not file_types:
                errors.append(f"Line {line_num}: file_types is empty")
            elif file_types not in VALID_FILE_TYPES:
                errors.append(f"Line {line_num}: file_types '{file_types}' not in {VALID_FILE_TYPES}")

            if not os_:
                errors.append(f"Line {line_num}: os is empty")
            elif os_ not in VALID_OS:
                errors.append(f"Line {line_num}: os '{os_}' not in {VALID_OS}")

            key = (name, os_)
            if key in seen:
                errors.append(f"Line {line_num}: duplicate name+os pair ('{name}', '{os_}')")
            seen.add(key)

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)
    else:
        print("diff_reporters.csv is valid.")


if __name__ == "__main__":
    main()
