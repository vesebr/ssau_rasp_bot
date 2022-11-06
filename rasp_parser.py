from bs4 import BeautifulSoup
import requests
import json
import datetime


def get_rasp(week):
    # current_date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=4)))
    # week = int(current_date.strftime('%W')) - 34
    url = f"https://ssau.ru/rasp?groupId=530994177&selectedWeek={week}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    all_cards = soup.findAll("div", class_="schedule__item")
    cards = all_cards[7::]
    lessons = []

    for i in range(len(cards)):
        num_lessons = len(cards[i].findAll('div', class_="schedule__lesson"))
        if num_lessons == 1:
            try:
                lesson_info = {
                    "name": cards[i].find('div', class_="schedule__discipline").text.strip(),
                    "place": cards[i].find('div', class_="schedule__place").text.strip(),
                    "teacher": cards[i].find('div', class_="schedule__teacher").text.strip(),
                    "group": cards[i].find('div', class_="schedule__groups").text.strip(),
                    "type": str(cards[i])[int(str(cards[i]).find('lesson-border-type-')) + 19]
                }
            except AttributeError:
                lesson_info = {
                    "name": cards[i].find('div', class_="schedule__discipline").text.strip(),
                    "place": '',
                    "teacher": '',
                    "group": '',
                    "type": str(cards[i])[int(str(cards[i]).find('lesson-border-type-')) + 19]
                }
            lessons.append(lesson_info)

        elif num_lessons == 2:
            double_lesson = []
            for j in range(2):
                try:
                    lesson_info = {
                        "name": cards[i].findAll('div', class_='schedule__discipline')[j].text.strip(),
                        "place": cards[i].findAll('div', class_='schedule__place')[j].text.strip(),
                        "teacher": cards[i].findAll('div', class_='schedule__teacher')[j].text.strip(),
                        "group": cards[i].findAll('div', class_='schedule__groups')[j].text.strip(),
                        "type": str(cards[i])[int(str(cards[i]).find('lesson-border-type-')) + 19]
                    }

                except AttributeError:
                    lesson_info = {
                        "name": cards[i].findAll('div', class_='schedule__discipline')[j].text.strip(),
                        "place": '',
                        "teacher": '',
                        "group": '',
                        "type": str(cards[i])[int(str(cards[i]).find('lesson-border-type-')) + 19]
                    }

                double_lesson.append(lesson_info)
            lessons.append(double_lesson)

        else:
            lesson_info = {
                "name": '',
                "place": '',
                "teacher": '',
                "group": '',
                "type": 0

            }
            lessons.append(lesson_info)

    with open("lessons.json", 'w', encoding="utf8") as file:
        json.dump(lessons, file, sort_keys=False, indent=4, ensure_ascii=False)


