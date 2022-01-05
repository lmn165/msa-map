from common.models import ValueObject, Reader
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import csv


class CrawlingTest(object):
    def __init__(self):
        pass

    def execute_crawling(self):
        vo = ValueObject()
        vo.context = 'data/'
        vo.url = 'https://www.worldometers.info/coronavirus'
        driver = webdriver.Chrome(f'{vo.context}chromedriver')
        driver.get(vo.url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tables = soup.select('table')
        table = tables[0]
        table_html = str(table)
        table_df_list = pd.read_html(table_html)
        table_df = table_df_list[0]
        # print(table_df)
        table_df = table_df.loc[:, ['Country,Other', 'TotalCases', 'TotalDeaths', 'TotalRecovered', 'Population']]
        table_df = table_df.iloc[1:-1]
        table_df.rename(columns={'Country,Other': 'name', 'TotalCases': 'cases', 'Population': 'population'}, inplace=True)
        table_df.fillna(0, inplace=True)
        table_df.to_csv(vo.context+'new_data/manufactured_corona_cases.csv', index=False)
        # print(table_df)
        driver.close()

    def world_code_labeling(self):
        vo = ValueObject()
        reader = Reader()
        vo.context = 'data/new_data/'
        vo.fname = 'new_iso_countries'
        csvfile = reader.new_file(vo)
        countries_code_df = reader.csv(csvfile)
        vo.fname = 'manufactured_corona_cases'
        csvfile = reader.new_file(vo)
        cases_df = reader.csv(csvfile)
        countries_code_df = countries_code_df.loc[:, ['name', 'alpha-2']]

        cases_df = pd.merge(cases_df, countries_code_df, left_on='name', right_on='name')
        cases_df.dropna(inplace=True)
        cases_df.rename(columns={'alpha-2': 'short_name'}, inplace=True)
        cases_df['population'] = cases_df['population'].astype(int)
        cases_df.to_csv(vo.context+'integrated_cases.csv', index=False)
        # print(cases_df.head(3))


if __name__ == '__main__':
    c = CrawlingTest()
    c.execute_crawling()
    c.world_code_labeling()