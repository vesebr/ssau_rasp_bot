import json
import datetime


def make_rasp_json(week):
    with open("lessons.json", "r", encoding="utf8") as file:
        data = json.load(file)

    # current_date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=4)))
    # week = int(current_date.strftime('%W')) - 34

    days = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота"
    ]

    time = [
        "8.00-9.35",
        "9.45-11.20",
        "11.30-13.05",
        "13.30-15.05"
    ]

    day_lessons_list = {}
    for i in range(6):
        day_lessons = []
        for j in range(i, len(data), 6):
            day_lessons.append(data[j])
        day_lessons_list[days[i]] = day_lessons

    for day in day_lessons_list:
        time_counter = 0
        for lesson in day_lessons_list[day]:
            if len(lesson) == 2:
                for i in range(2):
                    lesson[i]['time'] = time[time_counter]
            else:
                lesson['time'] = time[time_counter]
            time_counter += 1

    with open(f"dop_lessons{2 if week % 2 == 0 else 1}.json", "r", encoding="utf8") as file:
        dop_data = json.load(file)
    for item in dop_data:
        day_lessons_list[item["day"]].append(item)

    with open("rasp.json", "w", encoding="utf8") as file:
        json.dump(day_lessons_list, file, sort_keys=False, indent=4, ensure_ascii=False)
