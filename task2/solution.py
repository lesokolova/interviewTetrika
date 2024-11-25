from collections import Counter

import requests
from bs4 import BeautifulSoup
import csv


def parser(url: str):
    animal_names = []

    while url:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")

        beasts = soup.find_all("div", class_="mw-category-group")

        for beast in beasts:
            links = beast.find_all("a")
            for link in links:
                name = link.text.strip()

                if (
                    name
                    and "А" <= name[0] <= "Я"
                    and len(name) > 2
                    and not any(
                        phrase in name
                        for phrase in ["Знаменитые", "Породы собак", "по алфавиту"]
                    )
                ):
                    animal_names.append(name)

        next_page = soup.find("a", string="Следующая страница")
        if next_page:
            url = "https://ru.wikipedia.org" + next_page["href"]
        else:
            url = None

    return animal_names


def count_by_letter(animal_names: list):
    counts = Counter(name[0] for name in animal_names)
    return counts


def write_csv(file_name: str, data: dict):
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for letter, count in sorted(data.items()):
            writer.writerow([letter, count])


def data_analysis(file_name: str):
    """
    Функция анализирует данные из CSV-файла, содержащего количество названий животных, начинающихся на каждую букву русского алфавита. Данные сортируются по количеству животных в порядке убывания, после чего выводится рейтинг в консоль.
    :param file_name: Имя CSV-файла с информацией о животных в формате <Буква>, <Количество>
    :return: отсортированный по количеству список
    """

    with open(file_name, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = [(row[0], int(row[1])) for row in reader]

    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)

    print("Рейтинг букв по количеству животных:")
    for letter, count in sorted_data:
        print(f"{letter}: {count} животных")

    return sorted_data


if __name__ == "__main__":
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    animal_names = parser(url)
    letter_counts = count_by_letter(animal_names)
    write_csv("beasts.csv", letter_counts)
    data_analysis("beasts.csv")
