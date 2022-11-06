import openpyxl
import datetime
import json


def read_excel(week):
    list_lessons = {
        "Общие сведения об аддитивном производстве-Агапровичев А. В. (7 нед.);Материалы и оборудование для аддитивных технологий-Агапровичев А. В. (9 нед.); 3D печать технологиями SLS, SLM, EBM- Ивченко А. В. (15 нед.);3D печать технологиями SLS, SLM, EBM- Агаповичев А. В. (17 нед.) On-line": {
            "name": "3D печать технологиями SLS, SLM, EBM",
            "place": "On-line",
            "teacher": "Ивченко А. В.",
            "group": "15, 17 нед.",
            "type": "4",
            "time": ''},
        "3D печать технологиями FDM, SLA и MJM- Балякин А. В. (11-15 нед.) On-line": {
            "name": "3D печать технологиями FDM, SLA и MJM",
            "place": "On-line",
            "teacher": "Балякин А. В.",
            "group": "11-15 нед.",
            "type": "4"},
        "Изготовление малых партий изделий литьём в силикон- Мешков А. А. 104, 108-18 (12, 14 нед.); Литьё в разрушаемые формы- Мешков А. А. 104, 108-18 (16 нед.)": {
            "name": "Изготовление малых партий изделий литьём в силикон/ Литьё в разрушаемые формы",
            "place": "104, 108-18",
            "teacher": "Мешков А. А.",
            "group": "12, 14 нед./ 16 нед.",
            "type": "4"},

        "Аддитивное производство (3D печать)- Кокарева В. В. 236-5 (10-16 нед.)": {
            "name": "Аддитивное производство (3D печать)",
            "place": "236-5",
            "teacher": "Кокарева В. В.",
            "group": "10-16 нед.",
            "type": "4"},
        "3D печать технологиями FDM, SLA и MJM- Гончаров Е. С. 104, 108-18 (9-15 нед.)": {
            "name": "3D печать технологиями FDM, SLA и MJM",
            "place": "104, 108-18",
            "teacher": "Гончаров Е. С.",
            "group": "9-15 нед.",
            "type": "4"},
        "Материалы и оборудование для аддитивных технологий-Агапровичев А. В. (7 нед.); Возможности и ограничения CAD программ и их место в аддитивном производстве- Щемелев В. И. (9 нед.);3D печать технологиями SLS, SLM, EBM- Ивченко А. В. (15 нед.) On-line": {
            "name": "3D печать технологиями SLS, SLM, EBM",
            "place": "On-line",
            "teacher": "Ивченко А. В.",
            "group": "15 нед.",
            "type": "4"},
        "Создание и подготовка 3D моделей для аддитивного производства- Щемелев В. И. 209-14 (8-12 нед.)": {
            "name": "Создание и подготовка 3D моделей для аддитивного производства",
            "place": "209-14",
            "teacher": "Щемелев В. И.",
            "group": "8-12 нед.",
            "type": "4"},
        "Создание и подготовка 3D моделей для аддитивного производства- Щемелев В. И. 209-14  (9-17 нед.)": {
            "name": "Создание и подготовка 3D моделей для аддитивного производства",
            "place": "209-14",
            "teacher": "Щемелев В. И.",
            "group": "9-17 нед.",
            "type": "4"}
    }

    for j in range(1, 3):
        lessons = []
        book = openpyxl.load_workbook(f'{j}.xlsx', read_only=True)
        sheet = book.active
        for i in range(1, 49):
            if sheet[f'C{i}'].value is not None:
                lessons_info = {
                    "name": list_lessons[sheet[f'C{i}'].value]["name"],
                    "place": list_lessons[sheet[f'C{i}'].value]["place"],
                    "teacher": list_lessons[sheet[f'C{i}'].value]["teacher"],
                    "group": list_lessons[sheet[f'C{i}'].value]["group"],
                    "type": "4",
                    "time": sheet[f'B{i}'].value,
                    "day": sheet[f'A{i}'].value
                }
                lessons.append(lessons_info)
            else:
                continue

        with open(f"dop_lessons{j}.json", "w", encoding="utf8") as file:
            json.dump(lessons, file, sort_keys=False, indent=4, ensure_ascii=False)
