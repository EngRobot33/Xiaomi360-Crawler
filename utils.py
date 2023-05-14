import json


def convert_to_latin(*, number: str) -> str:
    latin_number = ""
    for char in str(number):
        if char == "۰":
            latin_number += "0"
        elif char == "۱":
            latin_number += "1"
        elif char == "۲":
            latin_number += "2"
        elif char == "۳":
            latin_number += "3"
        elif char == "۴":
            latin_number += "4"
        elif char == "۵":
            latin_number += "5"
        elif char == "۶":
            latin_number += "6"
        elif char == "۷":
            latin_number += "7"
        elif char == "۸":
            latin_number += "8"
        elif char == "۹":
            latin_number += "9"

    return latin_number


def save_json(*, data, file_name):
    file_path = f"{file_name}.json"
    with open(file_path, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)
