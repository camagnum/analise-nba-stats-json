from dataclasses import field
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

# Pegar o conteúdo HTML de uma URL
url = "https://www.nba.com/stats/players/traditional/?PerMode=Totals&sort=PLAYER_NAME&dir=-1"
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'}
}

def buildrank(type):

    field = rankings[type]['field']
    label = rankings[type]['label']

    time.sleep(5)

    driver.find_element_by_xpath(
        f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()

    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    # Parsear o conteúdo HTML - BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Estruturar conteúdo em um DataFrame - Pandas
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    # Transformar os dados num Dicionário de dados próprio
    return df.to_dict('records')

option = Options()
option.headless = True
driver = webdriver.Firefox()

driver.get(url)
time.sleep(8)

# Aceitar cookies
driver.find_element_by_xpath(
    '//*[@id="onetrust-accept-btn-handler"]').click()

# Chamar a função buildrank
for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()

# Converter e salvar em um arquivo JSON
js = json.dumps(top10ranking)
fp = open('ranking.json','w')
fp.write(js)
fp.close()

print('Programa finalizado!')