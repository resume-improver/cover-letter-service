import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def get_letter(resume, vacancy):
    # Собираем запрос
    data = {}
    # Указываем тип модели
    data["modelUri"] = f"gpt://{os.getenv('FOLDER_ID')}/yandexgpt"
    # Настраиваем опции
    data["completionOptions"] = {"temperature": 0.5, "maxTokens": 3000}
    # Указываем контекст для модели
    data["messages"] = [
        {"role": "system",
         "text": "Ты помощник, который пишет профессиональные сопроводительные письма. "
         "Напиши персонализированное сопроводительное письмо. Используй информацию из резюме и вакансии."
            "Всегда заполняй информацию, если она есть в резюме или вакансии"
             "Обращайся к компании, а не к HR-специалисту"
             "Возьми имя из резюме"
              "Нельзя использовать слова коллеги" },
        {"role": "user", 
         "text": f"Это резюме \n \n{resume} \n \nЭто описание вакансии {vacancy}"},
    ]
    
    # Отправляем запрос
    response = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers={
            "Accept": "application/json",
            "Authorization": f"Api-Key {os.getenv('API_KEY')}"
        },
        json=data,
    ).json()

    letter = ""
    # Извлекаем текст из первого альтернативного ответа
    if response.get("result") and len(response["result"]["alternatives"]) > 0:
        letter = response["result"]["alternatives"][0]["message"]["text"]
    else:
        print("❌ Не удалось найти сгенерированный текст в ответе.")
    return letter

def parse_json(name):
    # Чтение JSON-файла
    with open(name, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Собираем все пары "ключ: значение" в список строк
    lines = []

    for key, value in data.items():
        # Если значение список — объединяем элементы через пробел
        if isinstance(value, list):
            lines.append(f"{key}: {' '.join(value)}")
        else:
            lines.append(f"{key}: {value}")

    # Объединяем строки в одну, с переносами или через пробел
    line = "\n".join(lines)  # можно использовать " " вместо "\n"
    return line
