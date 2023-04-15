from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time

firefox_options = Options()
firefox_options.add_argument("--incognito")  # browser operates in private/incognito mode
firefox_options.headless = True  # crawler runs without a visible browser
driver = webdriver.Firefox(options=firefox_options)

url_list = ['https://www.horsedeals.com.au/search/stallion-services-for-sale',
            'https://www.horsedeals.com.au/search/horses-for-sale']


def scrape_searchpage_content(url_list):
    list_pagename = []
    list_title = []
    list_hyperlink = []
    list_breed = []
    list_price = []
    list_location = []
    list_excerpt = []
    list_num_photos = []
    list_discipline = []
    list_height = []
    list_age = []
    list_sex = []
    list_sold = []

    for url in url_list:
        driver.get(url)
        time.sleep(5)

        next_page = driver.find_element_by_css_selector('span.pagination__next').text

        try:
            sold_checkbox = driver.find_element_by_css_selector('input#include_sold')
            sold_checkbox.click()
        except:
            pass

        while next_page == "Next\nPage":
            time.sleep(2)

            current_page = driver.find_element_by_css_selector('p.pagination__current-page').text
            print(current_page + " of " + driver.title)

            ads = driver.find_elements_by_id("results")

            page_name = [driver.title for ad in ads]
            title = [ad.find_element_by_css_selector('span.listing_title').text for ad in ads]
            price = [ad.find_element_by_css_selector('span.listing_price').text for ad in ads]
            location = [ad.find_element_by_css_selector('span.listing_location').text for ad in ads]
            excerpt = [ad.find_element_by_css_selector('div.advert-description').text for ad in ads]
            num_photos = [ad.find_element_by_css_selector('span.product__img-counter').text for ad in ads]
            hyperlink = [ad.find_element_by_css_selector('a.btn.product__action__details').get_attribute('href') for ad in ads]

            for ad in ads:
                try:
                    breed = ad.find_element_by_css_selector('li[ng-if="qualities.breed"] span.disciplines-and-breed').text
                except:
                    breed = ''
                finally:
                    list_breed.append(breed)

            for ad in ads:
                try:
                    discipline = ad.find_element_by_css_selector('li[ng-if="displaySuitableFor()"] span.disciplines-and-breed').text
                except:
                    discipline = ''
                finally:
                    list_discipline.append(discipline)

            for ad in ads:
                try:
                    height = ad.find_element_by_css_selector('li.product__detail__item--height').text
                except:
                    height = ''
                finally:
                    list_height.append(height)

            for ad in ads:
                try:
                    age = ad.find_element_by_css_selector('li.product__detail__item--age').text
                except:
                    age = ''
                finally:
                    list_age.append(age)

            for ad in ads:
                try:
                    sex = ad.find_element_by_css_selector('li[ng-if="qualities.sex"]').text
                except:
                    sex = ''
                finally:
                    list_sex.append(sex)

            for ad in ads:
                try:
                    sold = ad.find_element_by_css_selector('.product__flag.is-sold').text
                except:
                    sold = ''
                finally:
                    list_sold.append(sold)

            list_pagename.extend(page_name)
            list_title.extend(title)
            list_price.extend(price)
            list_location.extend(location)
            list_excerpt.extend(excerpt)
            list_num_photos.extend(num_photos)
            list_hyperlink.extend(hyperlink)

            try:
                next_page = driver.find_element_by_css_selector('span.pagination__next').text
                next_link = driver.find_element_by_css_selector('a[rel="next nofollow"]')
            except:
                print("Done! No more pages.")
                break
            else:
                next_link.click()
                time.sleep(2)

        else:
            print("All done! Proceeding to the next stage.")

    driver.quit()

    series_pagename = pd.Series(list_pagename)
    series_hyperlink = pd.Series(list_hyperlink)
    series_title = pd.Series(list_title)
    series_breed = pd.Series(list_breed)
    series_price = pd.Series(list_price)
    series_location = pd.Series(list_location)
    series_excerpt = pd.Series(list_excerpt)
    series_num_photos = pd.Series(list_num_photos)
    series_discipline = pd.Series(list_discipline)
    series_height = pd.Series(list_height)
    series_age = pd.Series(list_age)
    series_sex = pd.Series(list_sex)
    series_sold = pd.Series(list_sold)


    data_dict = {'page_name': series_pagename,
                 'hyperlink': series_hyperlink,
                 'title': series_title,
                 'breed': series_breed,
                 'price': series_price,
                 'location': series_location,
                 'excerpt': series_excerpt,
                 'num_photos': series_num_photos,
                 'discipline': series_discipline,
                 'height': series_height,
                 'age': series_age,
                 'sex': series_sex,
                 'sold': series_sold}

    searchpage_df = pd.DataFrame(data_dict)

    return searchpage_df


startTime_prelim = time.time()
searchpage_data = scrape_searchpage_content(url_list)
executionTime_prelim = (time.time() - startTime_prelim)
print('Time taken to scrape preliminary content: {} minutes.'.format(str(round(executionTime_prelim, 2) / 60)))

searchpage_data.to_csv("HD_searchpage_data.csv")
url_series = searchpage_data.iloc[:,1]
url_series.to_csv('url_series.csv')
