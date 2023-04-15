import pandas as pd
import regex as re

data = pd.read_csv("E:\\Data_Files_Scripts\\PycharmProjects\\webscraping\\CRAN_packages\\CRAN_package_data.csv")

data['name'] = data.package_title.apply(lambda x: x.split(':')[0])
data['title'] = data.package_title.apply(lambda x: x.split(':')[1])
data.title = data.title.apply(lambda x: x.replace('\n', ' '))
data.title = data['title'].str.strip()
data.description = data.description.apply(lambda x: re.sub(r'[\n\t]', ' ', x))
data.description = data.description.apply(lambda x: re.sub(r'\s+', ' ', x))
data.description = data.description.apply(lambda x: x.replace(",Please use the canonical form , to link to this page.", ''))
data.description = data.description.apply(lambda x: x.replace('<,>', '<URL>'))

data['name_cf'] = data.name.apply(lambda x: x.casefold())
data.sort_values(by=['name_cf'], inplace=True)

data.drop_duplicates(subset='name_cf', inplace=True)

data = data.iloc[:, [0,2,3,4]]



