import numpy as np
import pandas as pd
import regex as re

# import and clean searchpage data
def clean_searchpage_data(searchpage_data):
    HZ_search_data['webpage'] = HZ_search_data.webpage.str.replace("<title>", "")
    HZ_search_data.webpage = HZ_search_data.webpage.str.replace("</title>", "")
    HZ_search_data['webpage2'] = HZ_search_data.webpage.apply(lambda x: re.match(r'^(Horses(\s*))', x))
    HZ_search_data.webpage2 = HZ_search_data.apply(lambda x: x.webpage2.group() if x.webpage2 != None else x.webpage, axis=1)

    HZ_search_data['breed'] = HZ_search_data.apply(lambda x: x.hyperlink.split("/")[2], axis=1)
    HZ_search_data.breed = HZ_search_data.breed.str.replace("_", " ", regex=False)

    HZ_search_data['price_conditions'] = HZ_search_data.price.apply(lambda x: "POA" if x.find("POA") > -1 else np.nan)
    HZ_search_data.price_conditions = HZ_search_data.apply(lambda x: "NEG" if x.price.find("NEG") > -1 else x.price_conditions, axis=1)
    HZ_search_data.price_conditions = HZ_search_data.apply(lambda x: "ONO" if x.price.find("ONO") > -1 else x.price_conditions, axis=1)
    HZ_search_data.price_conditions = HZ_search_data.apply(lambda x: "Free" if x.price.find("Free") > -1 else x.price_conditions, axis=1)
    HZ_search_data.price_conditions = HZ_search_data.apply(lambda x: "Make offer" if x.price.find("offer") > -1 else x.price_conditions, axis=1)
    HZ_search_data['price_currency'] = HZ_search_data.price.apply(lambda x: "AUD" if x.find("AUD") > -1 else np.nan)
    HZ_search_data.price_currency = HZ_search_data.apply(lambda x: "NZD" if x.price.find("NZD") > -1 else x.price_currency, axis=1)

    HZ_search_data['price2'] = HZ_search_data.price.apply(lambda x: re.match(r'^(\s*\$)(\d+[,.]\d+)', x))
    HZ_search_data.price2 = HZ_search_data.price2.apply(lambda x: x.group(2) if x != None else "")
    HZ_search_data.price2 = HZ_search_data.price2.str.replace(".00", "", regex=False)
    HZ_search_data.price2 = HZ_search_data.price2.str.replace(",", "", regex=False)
    HZ_search_data.price2 = HZ_search_data.price2.str.strip()
    HZ_search_data.price2 = HZ_search_data.price2.replace("", np.nan)
    HZ_search_data.price2 = HZ_search_data.price2.astype(float)

    HZ_search_data['excerpt'] = HZ_search_data.excerpt.apply(lambda x: re.sub('[\t\r\n\xa0\u200b]', '', x))
    HZ_search_data.excerpt = HZ_search_data.excerpt.apply(lambda x: re.sub('\s+', ' ', x))

    HZ_search_data['location'] = HZ_search_data.location.apply(lambda x: re.sub('[\t\r\n\xa0\u200b]', '', x))
    HZ_search_data['city/town'] = HZ_search_data.location.apply(lambda x: re.match(r'^(.+)(\,)', x))
    HZ_search_data['city/town'] = HZ_search_data['city/town'].apply(lambda x: x.group(1) if x != None else "")
    HZ_search_data['city/town'] = HZ_search_data.apply(lambda x: x['city/town'] if x['city/town'] != "" else x.location, axis=1)
    HZ_search_data['city/town'] = HZ_search_data['city/town'].apply(lambda x: x.title())
    HZ_search_data['city/town'] = HZ_search_data['city/town'].str.strip()
    HZ_search_data['state/territory'] = HZ_search_data.location.apply(lambda x: re.match(r'^(.+\,\s)(.+)', x))
    HZ_search_data['state/territory'] = HZ_search_data['state/territory'].apply(lambda x: x.group(2) if x != None else "")

    HZ_search_data.sold = HZ_search_data.sold.replace(np.nan, '')
    HZ_search_data.sold = HZ_search_data.sold.apply(lambda x: "SOLD" if x != '' else x)

    HZ_search_data['disciplines'] = HZ_search_data.disciplines.apply(lambda x: re.sub('[\t\r\n\xa0\u200b]', '', x))
    all_disciplines = ['Adult riding club', 'Breeding', 'Cutting', 'Driving/Harness', 'Eventing', 'Off the track', 'Polo',
                       'Pony Club', 'Reining', 'School Master', 'Showjumping', 'Western All Rounder', 'Western Show',
                       'All Rounder', 'Campdraft', 'Dressage', 'Endurance', 'Hunter', 'Other', 'Polocrosse', 'Racing',
                       'Rodeo/Barrel racing', 'Show', 'Trail riding/pleasure', 'Western Pleasure']

    for i in all_disciplines:
        HZ_search_data['discipline_' + i] = HZ_search_data.disciplines.apply(lambda x: "1" if x.find(i) > -1 else 0)

    HZ_search_data.replace('', np.nan, inplace=True)

    HZ_search_data.drop(['price', 'disciplines', 'location', 'hyperlink', 'webpage'], axis=1, inplace=True)
    HZ_search_data.rename(columns={'price2': 'price',
                                   'webpage2': 'webpage'}, inplace=True)

    return HZ_search_data

HZ_search_data = pd.read_csv("D:\Libraries\Documents\Data Science\PycharmProjects\horse_ads\HZ_searchpage_data.csv")
clean_HZ_search_data = clean_searchpage_data(HZ_search_data)

# import and clean ad data
def clean_ad_data(ad_data):
    HZ_ad_data = ad_data.copy()
    HZ_ad_data.drop_duplicates(subset='webpage', inplace=True, keep='first')
    HZ_ad_data.reset_index(drop=True, inplace=True)

    HZ_ad_data['extra_response'].fillna('', inplace=True)
    HZ_ad_data.extra_response = HZ_ad_data.extra_response.apply(lambda x: re.sub('[\t\r\n\xa0\u200b]', '', x))

    HZ_ad_data.rename(columns={'info_value1': 'colour'}, inplace=True)
    HZ_ad_data.colour.replace('Select Colour', np.nan, inplace=True)

    HZ_ad_data['sex'] = HZ_ad_data.apply(lambda x: x['info_value2'] if x['info_label2'] == "Sex:" else '', axis=1)

    HZ_ad_data['info_Mature Height'] = HZ_ad_data.apply(lambda x: x.info_value2 if x.info_label2 != "Sex:" else '', axis=1)
    HZ_ad_data['info_Mature Height2'] = HZ_ad_data.apply(lambda x: x.info_value3 if x.info_label3 != "Discipline:" else '', axis=1)
    HZ_ad_data['mature_height'] = HZ_ad_data['info_Mature Height'] + HZ_ad_data['info_Mature Height2']

    HZ_ad_data['info_Age'] = HZ_ad_data.apply(lambda x: x.info_value4 if x.info_label4 != "Discipline:" else '', axis=1)
    HZ_ad_data['info_Age2'] = HZ_ad_data.apply(lambda x: x.info_value5 if (x.info_label5 != "Broken:") & (x.info_label5 != "Age:") else '', axis=1)
    HZ_ad_data['age'] = HZ_ad_data.info_Age + HZ_ad_data.info_Age2

    HZ_ad_data['info_Registrations'] = HZ_ad_data.apply(lambda x: x.info_value5 if x.info_label5 == "Age:" else '', axis=1)
    HZ_ad_data['info_Registrations2'] = HZ_ad_data.apply(lambda x: x.info_value7 if x.info_label7 == "Registrations" else '', axis=1)
    HZ_ad_data['info_Registrations3'] = HZ_ad_data.apply(lambda x: x.info_value8 if x.info_label8 == "Rider Level:" else '', axis=1)
    HZ_ad_data['registrations'] = HZ_ad_data.info_Registrations + HZ_ad_data.info_Registrations2 + HZ_ad_data.info_Registrations3

    HZ_ad_data['info_Broken'] = HZ_ad_data.apply(lambda x: x.info_value5 if x.info_label5 == "Broken:" else '', axis=1)
    HZ_ad_data['info_Broken2'] = HZ_ad_data.apply(lambda x: x.info_value6 if x.info_label6 == "Age:" else '', axis=1)
    HZ_ad_data['broken'] = HZ_ad_data.info_Broken + HZ_ad_data.info_Broken2

    HZ_ad_data['info_Rider Level'] = HZ_ad_data.apply(lambda x: x.info_value6 if x.info_label6 == "Rider Level:" else '', axis=1)
    HZ_ad_data['info_Rider Level2'] = HZ_ad_data.apply(lambda x: x.info_value7 if x.info_label7 == "Broken:" else '', axis=1)
    HZ_ad_data['rider_level'] = HZ_ad_data['info_Rider Level'] + HZ_ad_data['info_Rider Level2']

    HZ_ad_data['listing_id'] = HZ_ad_data.listing_id.apply(lambda x: re.sub('[\t\r\n\xa0\u200b]', '', x))
    HZ_ad_data.listing_id = HZ_ad_data.listing_id.apply(lambda x: re.sub('Listing ID:', '', x))

    HZ_ad_data['num_views2'] = HZ_ad_data.num_views.apply(lambda x: re.match(r'(.+\s)(\d+)', x))
    HZ_ad_data.num_views2 = HZ_ad_data.num_views2.apply(lambda x: x.group(2) if x != None else "")
    HZ_ad_data.num_views2 = HZ_ad_data.num_views2.astype(int)

    HZ_ad_data['stallion_extras'] = HZ_ad_data.stallion_extras.str.replace(",", ", ")

    HZ_ad_data['text'] = HZ_ad_data.text.apply(lambda x: re.sub('[\t\r\n\xa0\u200b]', '', x))
    HZ_ad_data.text = HZ_ad_data.text.apply(lambda x: re.sub('\<[^>]*\>', ' ', x))
    HZ_ad_data.text = HZ_ad_data.text.str.strip()
    HZ_ad_data.text = HZ_ad_data.text.apply(lambda x: re.sub('\s+', ' ', x))

    HZ_ad_data['webpage'] = HZ_ad_data.webpage.apply(lambda x: re.sub('\<[^>]*\>', '', x))
    HZ_ad_data.webpage = HZ_ad_data.webpage.apply(lambda x: re.sub('\s+', ' ', x))

    HZ_ad_data['sex'] = HZ_ad_data.sex.apply(lambda x: 'Stallion' if x == '' else x)

    HZ_ad_data['title'] = HZ_ad_data.title.apply(lambda x: re.sub('[\t\r\n\xa0\u200b]', '', x))

    HZ_ad_data.sold = HZ_ad_data.sold.replace(np.nan, '')
    HZ_ad_data.sold = HZ_ad_data.sold.apply(lambda x: "SOLD" if x != '' else x)

    HZ_ad_data = HZ_ad_data[['extra_question', 'extra_response', 'colour', 'listing_id', 'seller_id', 'stallion_extras',
                             'text', 'title', 'webpage', 'sex', 'mature_height', 'age', 'registrations', 'broken',
                             'rider_level', 'num_views2', 'sold']]

    HZ_ad_data.rename(columns={'num_views2': 'num_views'}, inplace=True)

    HZ_ad_data.replace('', np.nan, inplace=True)
    HZ_ad_data['age'] = HZ_ad_data.age.astype(float)

    HZ_ad_data.sex.replace("Select Sex", np.nan, inplace=True)
    HZ_ad_data.broken.replace("Select Broken in", np.nan, inplace=True)
    HZ_ad_data.rider_level.replace("Select Rider Level", np.nan, inplace=True)

    return HZ_ad_data

HZ_ad_data = pd.read_csv("D:\Libraries\Documents\Data Science\PycharmProjects\horse_ads\HZ_ad_data.csv")
clean_HZ_ad_data = clean_ad_data(HZ_ad_data)

clean_HZ_search_data.sort_values(by='title', inplace=True)
clean_HZ_ad_data.sort_values(by='webpage', inplace=True)
clean_HZ_search_data.reset_index(inplace=True, drop=True)
clean_HZ_ad_data.reset_index(inplace=True, drop=True)

HZ_data = pd.merge(clean_HZ_search_data, clean_HZ_ad_data, left_index=True, right_index=True, how='inner')

HZ_data.drop(['title_y', 'webpage_y', 'sold_y'], axis=1, inplace=True)
HZ_data.rename(columns={'title_x': 'title',
                        'webpage_x': 'webpage',
                        'sold_x': 'sold'}, inplace=True)

HZ_data.to_csv("clean_HZ_data.csv")
