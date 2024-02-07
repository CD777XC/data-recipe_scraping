# pylint: disable=missing-docstring, line-too-long, missing-timeout
import sys
import requests
import csv
from os import path
from bs4 import BeautifulSoup as bs

def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    recipes = []
    for _, page in enumerate(html):
        soup = bs(page, 'html.parser')
        name_divs = soup.find_all('p', class_="recipe-name")
        difficulty_divs = soup.find_all('span', class_="recipe-difficulty")
        prep_time_divs = soup.find_all('span', class_="recipe-cooktime")
        count = len(recipes)
        for name, difficulty, prep_time in zip(name_divs, difficulty_divs, prep_time_divs):
            recipes.append({})
            recipes[count]['name'] = name.get_text()
            recipes[count]['difficulty'] = difficulty.get_text()
            recipes[count]['prep_time'] = prep_time.get_text()
            count+=1
    # soup = bs(html, 'html.parser')
    # name_divs = soup.find_all('p', class_="recipe-name")
    # difficulty_divs = soup.find_all('span', class_="recipe-difficulty")
    # prep_time_divs = soup.find_all('span', class_="recipe-cooktime")
    # count = len(recipes)
    # for name, difficulty, prep_time in zip(name_divs, difficulty_divs, prep_time_divs):
    #     recipes.append({})
    #     recipes[count]['name'] = name.get_text()
    #     recipes[count]['difficulty'] = difficulty.get_text()
    #     recipes[count]['prep_time'] = prep_time.get_text()
    #     count+=1
    return recipes

def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modeling a recipe'''
    article_name = article.replace(' ', '+')
    url = f'https://recipes.lewagon.com/?search[query]={article_name}&button='
    response = requests.get(url)
    recipes = {
        'name': [],
        'difficulty': [],
        'prep_time': []
    }
    if response.status_code == 200 and response.history == []:
        soup = bs(response.text, 'html.parser')
        name_divs = soup.find_all('p', class_="recipe-name")
        difficulty_divs = soup.find_all('span', class_="recipe-difficulty")
        prep_time_divs = soup.find_all('span', class_="recipe-cooktime")
        for name, difficulty, prep_time in zip(name_divs, difficulty_divs, prep_time_divs):
            if name.get_text() == article:
                recipes['name'] = name.get_text()
                recipes['difficulty'] = difficulty.get_text()
                recipes['prep_time'] = prep_time.get_text()
        return recipes
    else:
        print(f"Error {response.status_code}")

def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    with open(f'recipes/{ingredient}', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=recipes[0].keys())
        writer.writeheader()
        for recipe in recipes:
            writer.writerow(recipe)

def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    url = f'https://recipes.lewagon.com/?search[query]={ingredient}&button='
    response = requests.get(url)
    responses = []
    if response.status_code == 200:
        for i in range(3):
            response = requests.get(f"{url}&page={i+start}")
            if response.history == []:
                responses.append(response.text)
    return responses

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"

    if path.exists(file):
        return open(file, encoding='utf-8')

    print("Please, run the following command first:")
    print(f'curl -g "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')

    sys.exit(1)

def main():
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]

        # TODO: Replace scrape_from_file with scrape_from_internet and implement pagination (more than 2 pages needed)
        recipes = parse(scrape_from_internet(ingredient, start=1))
        # recipes = parse(scrape_from_file(ingredient))
        write_csv(ingredient, recipes)
        print(f"Wrote recipes to recipes/{ingredient}.csv")
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
