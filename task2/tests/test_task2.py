import pytest
import csv
from task2.solution import parser, count_by_letter, write_csv


@pytest.mark.parametrize(
    "url, expected_start",
    [
        ("https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту", "А"),
    ],
)
def test_parser(url, expected_start):
    beasts = parser(url)
    assert len(beasts) > 0
    assert all("А" <= name[0] <= "Я" for name in beasts)
    assert beasts[0].startswith(expected_start)


@pytest.mark.parametrize(
    "animal_names, expected_counts",
    [
        (
            [
                "Абидозавр",
                "Агами",
                "Австралийский питон Рамсея",
                "Бархатистая филепитта",
                "Белка-крошка",
            ],
            {"А": 3, "Б": 2},
        ),
        ([], {}),
        (["Обезьяны", "Обыкновенная слепушонка", "Обыкновенный бобр"], {"О": 3}),
    ],
)
def test_count_by_letter(animal_names, expected_counts):
    result = count_by_letter(animal_names)
    assert result == expected_counts


def test_write_csv(tmp_path):
    output_file = tmp_path / "beasts.csv"

    test_data = {"А": 3, "Б": 2}
    write_csv(output_file, test_data)

    with open(output_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)

    assert ["А", "3"] in rows
    assert ["Б", "2"] in rows
