## Scraping Horsezone and Horse Deals horse ads

This is just a project I devised mainly to explore the capabilities of scrapy. However, I did find that I had to go back to using Selenium for part of it as one of my websites used Javascript and at the time I couldn't devote the resources to learning scrapy-splash. It consists of four spiders (two for each website - one to scrape the searchpage data and the second to follow the links into the ads themselves), an items file for the scrapy spiders, and various scripts used to clean the data.

The final scrape was able to pull out 2,616 ads from Horse Deals and 494 ads from Horsezone, and included a number of different elements such as the listing price, title or horse name, advert text, what disciplines the horse would be suited for, breed, age and height. The rest of this README contains an overview of the EDA I did, which primarily consisted of a comparison of the data using features common to both websites.

The first chart plotted the ratio of sold to 'not-sold' ads. It indicated that about half of the Horse Deals dataset was made up of adverts marked as sold, whereas the proportion of adverts marked as sold in the Horsezone dataset was far smaller (approximately 20 per cent).

[insert image here]

The second chart looked at the distribution of number of views of adverts across the two websites. The distributions were very similar in shape, but somewhat surprisingly (for me at least), the average (mean) number of views per ad for the Horse Deals website was slightly lower at 877 views compared to 1,139 views for the Horsezone website.

[insert image here]

The third chart examined the breeds most often advertised. On the Horse Deals website, the top spot was taken by Thoroughbreds, with Quarter Horses and Australian Stock Horses making up the top three. However, the Horsezone website was very much dominated by Warmbloods and Thoroughbreds.

[insert image here]

The fourth chart examined the types of rider levels associated with the ads. Most Horse Deals ads didn't mention the level of rider most suited to the horse, but when it did, Intermediate was the most common level. The Horsezone website had a more even distribution across the categories, but many ads also didn't specify or didn't find the rider level feature applicable (presumably because there were some ads for horses too young or too small to ride). However, like the Horse Deals website, the most common level of rider specified was Intermediate.

[insert image here]

Moving on to sex, the distributions were almost identical, with geldings being most-often advertised, followed by mares.

[insert image here]

The advert location was interesting, especially since the distributions for the two websites across the states and territories were again just about identical. One possible explanation for why NSW, QLD and VIC dominated could be that the websites are east-coast specific and that states like South Australia and Western Australia had their own equine advertising websites.

[insert image here]



