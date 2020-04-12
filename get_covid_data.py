from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_covid():
    url = "https://www.worldometers.info/coronavirus/"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    table = soup.find("table", id="main_table_countries_today")
    table_data = table.tbody.find_all("tr")

    alldata = {}
    for i in range(len(table_data)):
        try:
            key = (table_data[i].find_all('a', href=True)[0].string)
        except:
            key = (table_data[i].find_all('td')[0].string)

        value = [j.string for j in table_data[i].find_all('td')]
        alldata[key] = value
    csv_data = pd.DataFrame(alldata).drop(0).T
    csv_data.columns = ["Total Cases", "New Cases", "Total Deaths", "New Deaths", "Total Recovered", "Active", "Serious Critical",
                        "Tot Cases/1M pop", "Tot Deaths/1M pop", "Tot tests/1M pop", "Test/1M pop", "Continent"]
    csv_data.index.name = 'Country'
    csv_data.iloc[1:, :7].to_csv("data.csv")


get_covid()
