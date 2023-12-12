import json
import re
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

# Передаем URL и headers
url = str(os.getenv("URL"))

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.967 YaBrowser/23.9.1.967 Yowser/2.5 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text

with open("index.html", "w", encoding="utf-8") as file:
    file.write(src)

with open("index.html", encoding="utf-8") as file:
    src = file.read()

# Находим ссылки на рецепты по категориям
soup = BeautifulSoup(src, "lxml")
meals_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

# Собираем ссылки на категории рецептов
meals_dict = {}
for item in meals_hrefs:
    item_text = item.text
    item_href = "https://health-diet.ru" + item.get("href")
    meals_dict[item_text] = item_href

with open('meals_dict.json', 'w', encoding="utf-8") as file:
    json.dump(meals_dict, file, indent=4, ensure_ascii=False)

with open('meals_dict.json', encoding="utf-8") as file:
    all_meals = json.load(file)

print(all_meals)

# Перебираем все категории рецептов
for meals_name, meals_hrefs in all_meals.items():
    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in meals_name:
            meals_name = meals_name.replace(item, "_")

    req = requests.get(url=meals_hrefs, headers=headers)
    src = req.text

    # Получаем ссылки на ингредиенты для каждой категории рецептов
    soup = BeautifulSoup(src, "lxml")
    ingridients_hrefs = soup.find_all("table", class_="uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed")

    # Готовим ingridients_dict для каждой категории рецептов
    ingridients_dict = {}
    for ingridients in ingridients_hrefs:
        links = ingridients.find_all('td')
        for link in links:
            spisok = link.find("a")
            if spisok:
                href = spisok.get("href")
                item_text = link.text
                item_href = "https://health-diet.ru" + href
                item_text = re.sub('\n', '', item_text)
                ingridients_dict[item_text] = item_href

        with open(f'meals/{meals_name}_ingridients_dict.json', 'w', encoding="utf-8") as file:
            json.dump(ingridients_dict, file, indent=4, ensure_ascii=False)

        with open(f'meals/{meals_name}_ingridients_dict.json', encoding="utf-8") as file:
            all_ingridients = json.load(file)

        for ingridients_name, ingridients_hrefs in all_ingridients.items():
            rep = [",", " ", "-", "'"]
            for item in rep:
                if item in ingridients_name:
                    ingridients_name = ingridients_name.replace(item, "_")

            req = requests.get(url=ingridients_hrefs, headers=headers)
            src = req.text

            # Здесь обрабатываем ссылку на ингредиенты и получаем данные

            print(ingridients_hrefs)
            next_page_url = ingridients_hrefs
            response = requests.get(next_page_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Ищем таблицу с ингредиентами
            ingredients_table = soup.find('table', class_='mzr-recipe-view-ingredients')
            ingredients_list = {}
            if ingredients_table:
                ingredients_rows = ingredients_table.find_all('tr')
                # Обрабатываем таблицу с ингридиентами
                for row in ingredients_rows[1:]:
                    ingredients_cells = row.find_all('td')
                    if len(ingredients_cells) == 2:
                        ingridients_name = soup.find_all('h2', class_='mzr-block-header-line')
                        for name in ingridients_name:
                            meal_name = re.sub('Ингредиенты ', '', name.text)
                        # noinspection PyUnboundLocalVariable
                        ingridients_name = meal_name
                        ingredient = ingredients_cells[0].text.strip()
                        amount = ingredients_cells[1].text.strip()
                        if meal_name not in ingredients_list:
                            ingredients_list[meal_name] = []
                        ingredients_list[meal_name].append(
                            {
                                "ingredient": ingredient,
                                "quantity": amount
                            }
                        )
                        # Создаем словарь с данными
                        recipe_instruction = soup.find_all('p', class_='mzr-recipe-view-description-tc')
                        for recipe_instruction in soup.find_all(attrs={'itemprop': 'recipeInstructions'}):
                            recipe_manual = recipe_instruction.text.strip()

                        recipe = {"ingredients": []}
                        for dish, ingredients in ingredients_list.items():
                            for ingredient in ingredients:
                                ingredient_name = ingredient["ingredient"]
                                quantity = ingredient["quantity"]
                                dish = dish.replace("\n", '').replace('"', '')
                                recipe["ingredients"].append({
                                    "dish": dish,
                                    "ingredient": ingredient_name,
                                    "quantity": quantity,
                                    "link": ingridients_hrefs,
                                    "key": dish + ' ' + ingridients_hrefs
                                })

                                print(f"# БЛЮДО {dish} Ингредиент: {ingredient_name}.\
                                 Количество: {quantity} записан...")

                        # Записываем данные в JSON файл
                        # noinspection PyUnboundLocalVariable
                        with open(f'recipe/{dish}_ingredients.json', 'w', encoding='utf-8') as file:
                            json.dump(recipe, file, ensure_ascii=False, indent=4)

                        # Создаем recipe_manual
                        recipe_manual_data = {}
                        existing_keys = []

                        for recipe_instruction in soup.find_all(attrs={'itemprop': 'recipeInstructions'}):
                            recipe_manual = recipe_instruction.text.strip()
                            key = dish + ' ' + ingridients_hrefs

                            if key not in existing_keys:
                                recipe_manual_data[key] = recipe_manual
                                existing_keys.append(key)

                        # Записываем данные в JSON файл
                        with open(f'recipe_manual/{dish}_recipe_manual.json', 'w', encoding='utf-8') as file:
                            json.dump(recipe_manual_data, file, ensure_ascii=False, indent=4)
