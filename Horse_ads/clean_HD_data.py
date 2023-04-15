import numpy as np
import pandas as pd
import regex as re


# import and clean searchpage data
def clean_searchpage_data(searchpage_data):
    searchpage_data.fillna('', inplace=True)

    searchpage_data['webpage'] = searchpage_data.apply(lambda x: x.page_name.split(" | ")[0], axis=1)
    searchpage_data['website'] = searchpage_data.apply(lambda x: x.page_name.split(" | ")[1], axis=1)

    searchpage_data['price'] = searchpage_data.price.str.replace('Fee: ', '', regex=False)
    searchpage_data.price = searchpage_data.price.str.replace('$', '', regex=False)
    searchpage_data.price = searchpage_data.price.str.replace(',', '', regex=False)

    searchpage_data['price_conditions'] = searchpage_data.price.apply(lambda x: "POA" if x.find("POA") > -1 else np.nan)
    searchpage_data.price_conditions = searchpage_data.apply(lambda x: "Free" if x.price.find("Free") > -1 else x.price_conditions, axis=1)
    searchpage_data.price_conditions = searchpage_data.apply(lambda x: "NEG" if x.price.find("NEG") > -1 else x.price_conditions, axis=1)

    searchpage_data.price = searchpage_data.price.apply(lambda x: re.match(r'^(\d+)', x))
    searchpage_data.price = searchpage_data.price.apply(lambda x: x.group() if x != None else '')
    searchpage_data.price = searchpage_data.price.replace('', np.nan)
    searchpage_data.price = searchpage_data.price.astype(float)

    searchpage_data['city/town'] = searchpage_data.location.apply(lambda x: re.match(r'^(.+)(\,\s)', x))
    searchpage_data['city/town'] = searchpage_data['city/town'].apply(lambda x: x.group(1) if x != None else '')

    searchpage_data['state/territory'] = searchpage_data.apply(lambda x: x['city/town'].split(", "), axis=1)
    searchpage_data['city/town'] = searchpage_data.apply(lambda x: x['state/territory'][0], axis = 1)
    searchpage_data['state/territory'] = searchpage_data.apply(lambda x: x['state/territory'][1] if len(x['state/territory']) > 1 else '', axis=1)

    searchpage_data['country'] = searchpage_data.location.apply(lambda x: re.match(r'^(.+\,\s)(.+)', x))
    searchpage_data.country = searchpage_data.country.apply(lambda x: x.group(2) if x != None else '')
    searchpage_data['state/territory'] = searchpage_data.apply(lambda x: x['state/territory'] if x['state/territory'] != '' else x.country if (x.country != "US" or x.country != "NZ") else '', axis=1)
    searchpage_data.country = searchpage_data.apply(lambda x: x.location if x.location == "US" or x.location == "NZ" else x.country, axis=1)
    searchpage_data.country = searchpage_data.apply(lambda x: x.country if x.country == "US" or x.country == "NZ" or x.country == "" else "", axis=1)
    searchpage_data['state/territory'] = searchpage_data.apply(lambda x: x.location if len(x.location) < 4 and (x.location != "NZ" or x.location != "US") else x['state/territory'], axis=1)
    searchpage_data['state/territory'] = searchpage_data['state/territory'].replace("NZ", '')
    searchpage_data['state/territory'] = searchpage_data['state/territory'].replace("US", '')

    searchpage_data['height2'] = searchpage_data.height.apply(lambda x: re.match(r'(.+\s)(\d+[\.\d+]?.+)', x))
    searchpage_data.height2 = searchpage_data.height2.apply(lambda x: x.group(2) if x != None else '')
    searchpage_data.height2 = searchpage_data.height2.str.replace("hh", '')

    searchpage_data['age'] = searchpage_data.age.str.replace("Age: ", '')
    searchpage_data.age = searchpage_data.age.str.replace("yo", '')

    searchpage_data['sex'] = searchpage_data.sex.str.replace("Sex: ", '')
    searchpage_data.sex = searchpage_data.apply(lambda x: "Stallion" if x.webpage == "Stallion Services" else x.sex, axis=1)

    all_disciplines = ['Adult riding club', 'Allrounders', 'Barrel Racing', 'Beginners', 'Breeding', 'Campdrafting',
                       'Challenge', 'Companion', 'Cutting', 'Dressage', 'Endurance', 'Eventing', 'HRCAV', 'Harness',
                       'Interschool', 'Off The Track', 'Performance', 'Performance Ponies', 'Pleasure', 'Polo',
                       'Polocrosse', 'Pony Club', 'Project', 'Racing', 'Ranch Horse', 'Reining', 'Rodeo', 'Show',
                       'Showjumping', 'Team Penning', 'Trail Riding', 'Western Performance', 'Western Show',
                       'Working Cow Horse']
    for i in all_disciplines:
        searchpage_data['discipline_' + i] = searchpage_data.discipline.apply(lambda x: "1" if x.find(i) > -1 else 0)

    searchpage_data.replace('', np.nan, inplace=True)
    searchpage_data.drop(['page_name', 'location', 'height', 'discipline'], axis=1, inplace=True)

    searchpage_data.rename(columns={'height2': 'height_hh'}, inplace=True)

    return searchpage_data


HD_search_data = pd.read_csv("D:\Libraries\Documents\Data Science\PycharmProjects\horse_ads\HD_searchpage_data.csv", index_col=0)
# only required to generate initial hyperlink list for scrapy spider
# HD_hyperlinks = HD_search_data.hyperlink.drop_duplicates()
# HD_hyperlinks.to_csv("HD_hyperlinks.csv")

searchpage_data = HD_search_data.copy()
clean_HD_search_data = clean_searchpage_data(searchpage_data)


# import and clean ad data
def clean_ad_data(ad_data):
    ad_data.fillna('', inplace=True)
    ad_data['service_options'] = ad_data['age_sex_rider_service'].apply(lambda x: "AI" if (x.find("AI") > -1
                                                                                                 or x.find("AI and Live cover") > -1
                                                                                                 or x.find("Live cover") > -1) else np.nan)

    attributes = ad_data['age_sex_rider_service'].str.split(",", expand = True)
    attributes = attributes.iloc[:,0:4]
    attributes = attributes.replace([None], '')
    attributes.rename(columns={0: 'h', 1: 'a', 2: 's', 3: 'r'}, inplace=True)

    attributes['height'] = attributes.apply(lambda x: x.h if x.h.find("hh") > -1 else '', axis=1)
    attributes['age'] = attributes.apply(lambda x: x.a if (x.a.find("yo") > -1
                                                           or x.a.find("under 12 months") > -1) else '', axis=1)
    attributes['sex'] = attributes.apply(lambda x: x.s if (x.s.find("Gelding") > -1
                                                           or x.s.find("Mare") > -1
                                                           or x.s.find("Filly") > -1
                                                           or x.s.find("Colt") > -1
                                                           or x.s.find("Stallion") > -1) else '', axis=1)

    attributes['rider_level'] = attributes.apply(lambda x: x.r if (x.r.find("Beginner") > -1
                                                                   or x.r.find("Novice") > -1
                                                                   or x.r.find("Intermediate") > -1
                                                                   or x.r.find("Advanced") > -1
                                                                   or x.r.find("Not Specified") > -1) else '', axis=1)

    ad_data = pd.merge(ad_data, attributes[['height', 'age', 'sex', 'rider_level']], how='left', left_index=True, right_index=True)

    ad_data['postcode'] = ad_data['breed_location'].apply(lambda x: re.match(r'(.+?)(\d{4})$', x))
    ad_data.postcode = ad_data.postcode.apply(lambda x: x.group(2) if x != None else '')

    ad_data.hyperlink = ad_data.hyperlink.str.replace("<GET ", "", regex=False)
    ad_data.hyperlink = ad_data.hyperlink.str.replace(">", "", regex=False)

    ad_data.num_views = ad_data.num_views.str.replace(" views", "", regex=False)

    ad_data.price = ad_data.price.str.replace("Fee: ", "", regex=False)
    ad_data.price = ad_data.price.str.replace("$", "", regex=False)
    ad_data.price = ad_data.price.str.replace(",", "", regex=False)

    ad_data['price_conditions'] = ad_data.price.apply(lambda x: re.match(r'([A-Za-z]+)', x))
    ad_data.price_conditions = ad_data.apply(lambda x: x.price_conditions.group() if x.price_conditions != None else '', axis=1)
    ad_data['price_conditions2'] = ad_data.price.apply(lambda x: re.match(r'(.+?\s)([A-Za-z]+)$', x))
    ad_data.price_conditions = ad_data.apply(lambda x: x.price_conditions2.group(2) if x.price_conditions2 != None else x.price_conditions, axis=1)
    ad_data.price_conditions = ad_data.price_conditions.apply(lambda x: x.upper())

    ad_data.price = ad_data.price.apply(lambda x: re.match(r'^(\d+)', x))
    ad_data.price = ad_data.price.apply(lambda x: x.group() if x != None else '')
    ad_data.price = ad_data.price.replace('', np.nan)
    ad_data.price = ad_data.price.astype(float)

    ad_data.text = ad_data.text.apply(lambda x: re.sub('>,<', '><', x))
    ad_data.text = ad_data.text.apply(lambda x: re.sub('<[^>]*>', ' ', x))
    ad_data.text = ad_data.text.apply(lambda x: re.sub('\s+', ' ', x))

    searchpage_data.replace('', np.nan, inplace=True)
    ad_data.drop(['age_sex_rider_service', 'height_y', 'breed_location', 'discipline', 'height_x', 'age', 'sex',
                  'price_conditions2', 'webpage'], inplace=True, axis=1)
    
    return ad_data

HD_ad_data = pd.read_csv("D:\Libraries\Documents\Data Science\PycharmProjects\horse_ads\HD_ad_data.csv")
ad_data = HD_ad_data.copy()
clean_HD_ad_data = clean_ad_data(ad_data)

# combine and final clean
def combine_data(search_data, ad_data):
    clean_data = pd.merge(search_data, ad_data, how='inner', left_on='hyperlink', right_on='hyperlink')

    clean_data.drop(['title_y', 'price_x', 'price_conditions_x', 'num_photos_y', 'sold_y', 'hyperlink'],
                    inplace=True, axis=1)
    
    clean_data = clean_data.replace('', np.nan)
    
    clean_data.rename(columns={'title_x': 'title',
                               'num_photos_x': 'num_photos',
                               'sold_x': 'sold',
                               'price_y': 'price',
                               'price_conditions_y': 'price_conditions'}, inplace=True)

    return clean_data

clean_data = combine_data(clean_HD_search_data, clean_HD_ad_data)
clean_data.to_csv("clean_HD_data.csv")
