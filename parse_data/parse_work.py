import csv
import requests
import lxml
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
from datetime import datetime

ua = UserAgent()
session = requests.Session()
session.headers = {
    "Accept": "image/avif,image/webp,*/*",
    "User-Agent": ua.random
}

item = "https://layboard.com/vakansii/rabota-v-polshe/rabota-v-krakove"
link_list = [item]  # https://layboard.com/vakansii/rabota-v-polshe/rabota-v-krakove?page=5
vacancy_info_list = []


def make_link_list():
    global link_list
    for n in range(2, 22):
        link = f"https://layboard.com/vakansii/rabota-v-polshe/rabota-v-krakove?page={n}/"
        link_list.append(link)
    return link_list


def get_vacancy(url):
    global vacancy_info_list
    response = session.get(url)
    data = response.text
    print(response.status_code)
    soup = BS(data, "lxml")

    all_vacancy = soup.find_all("div", class_="job-cards")

    for el in all_vacancy:
        link = 'https://layboard.com' + el.find("a", class_="vacancy-body").get("href")
        title = el.find("div", class_="vacancy-card-title").text.strip()
        category = el.find("div", class_="vacancy-card-category").text.strip()
        preview = el.find("div", class_="vacancy-card-preview").text.strip()
        vacancy_info = [category, title, link, preview]
        vacancy_info_list.append(vacancy_info)
        # with open("work_data/vacancy_layboard_com.csv", "a", newline="", encoding="utf-8") as file:
        #     writer = csv.writer(file)
        #     writer.writerow(
        #         (
        #             title,
        #             category,
        #             link,
        #             preview
        #         )
        #     )


def main():
    make_link_list()
    print(len(vacancy_info_list), vacancy_info_list)
    for i in range(len(link_list)):
        for url in link_list:
            get_vacancy(url)
    for itm in vacancy_info_list:
        print(itm)
        with open(f"work_data/all_vacancy{datetime.now()}", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    itm[0],
                    itm[1],
                    itm[2],
                    itm[3],
                )
            )


if __name__ == '__main__':
    main()
