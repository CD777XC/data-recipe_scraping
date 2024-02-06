import sys
from os import path
from bs4 import BeautifulSoup as bs
import requests

def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modeling a recipe'''
    url = f'https://recipes.lewagon.com/?search[query]={article}&button='
    response = requests.get(url)
    recipes = {
        'name': [],
        'difficulty': [],
        'prep_time': []
    }
    if response.status_code == 200:
        for i in range(3):
            response = requests.get(f"{url}&page={i+1}")
            if response.history == []:
                soup = bs(response.text, 'html.parser')
                name_divs = soup.find_all('p', class_="recipe-name")
                difficulty_divs = soup.find_all('span', class_="recipe-difficulty")
                prep_time_divs = soup.find_all('span', class_="recipe-cooktime")
                for name, difficulty, prep_time in zip(name_divs, difficulty_divs, prep_time_divs):
                    recipes['name'].append(name.get_text())
                    recipes['difficulty'].append(difficulty.get_text())
                    recipes['prep_time'].append(prep_time.get_text())

        return recipes

    else:
        print(f"Error {response.status_code}")




    # recipes = {
    #     'name': [],
    #     'difficulty': [],
    #     'prep_time': []
    # }
    # for time in link.find_all('span', class_="recipe-cooktime"):
    #     recipes['prep_time'] += time.text
    # return recipes['prep_time']

print(parse_recipe('mint'))
