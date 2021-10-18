import requests
from bs4 import BeautifulSoup
import csv

"""
links = []

for i in range(51):
    url = 'https://books.toscrape.com/catalogue/' + 'page-' + str(i) + '.html'
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        tds = soup.findAll('h3')

        for h3 in tds:
            a = h3.find('a')
            link = a['href']
            links.append('https://books.toscrape.com/' + link)

print(links)
"""

"""
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

upc_bs = soup.find_all("td")
print(upc_bs[0].string)
"""

"""
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

product_information = soup.find_all("td")
upc = product_information[0].string
price_excluding_tax = product_information[2].string
price_including_tax = product_information[3].string
number_available = product_information[5].string
review_rating = product_information[6].string

product_description_bs = soup.find_all("p")
product_description = product_description_bs[3]

category_bs = soup.find_all("a")
category = category_bs[3].string

image_bs = soup.find_all("img")
images = image_bs[0]
image = images.attrs['src']

product_page_url = page.url

title_bs = soup.find_all("h1")
title = title_bs[0].string
"""

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

product_page_url = page.url

title_bs = soup.find_all("h1")
title = title_bs[0].string

product_information = soup.find_all("td")
upc = product_information[0].string
price_excluding_tax = product_information[2].string
price_including_tax = product_information[3].string
number_available = product_information[5].string
review_rating = product_information[6].string

product_description_bs = soup.find_all("p")
product_description = product_description_bs[3].string

category_bs = soup.find_all("a")
category = category_bs[3].string

image_bs = soup.find_all("img")
images = image_bs[0]
image = images.attrs['src']

book_information = [product_page_url, upc, title, price_including_tax, price_excluding_tax,
                    number_available, product_description, category, review_rating, image]
