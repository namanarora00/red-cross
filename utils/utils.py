import csv
import re

regex = re.compile(r"[^\w]", re.IGNORECASE)


def read_csv(file_path=None) -> list:
    if file_path is None:
        file_path = "resources/test.csv"    # test file

    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        data = [dict(row) for row in reader]

        cleaned_data = []

        for row in data:
            new_row = {}
            for key in row:
                new_row[clean(key)] = row[key]          # cleaning column
            cleaned_data.append(new_row)

        return cleaned_data


def clean(column):
    cleaned = re.sub(regex, "", column)

    return cleaned.lower()


if __name__ == "__main__":
    read_csv()
