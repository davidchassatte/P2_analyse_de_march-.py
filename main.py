import requests
from bs4 import BeautifulSoup
import random
import numpy
import urllib.request
import pandas as pd
import time
import re
from math import ceil
import csv

'''
def scrape_book_information():

    # Scrapper les informations d'un livre et enregistrer sous format csv
    url = "https://books.toscrape.com/index.html"
    page = requests.get(url)
    soup_page = BeautifulSoup(page.text, 'html.parser')
    link_book = soup_page.find('div', class_="image_container").find('a')['href']
    url_book = "https://books.toscrape.com/" + link_book
    page_book = requests.get(url_book)
    soup = BeautifulSoup(page_book.text, 'html.parser')
    
    with open('scraping_single_book.csv', 'w', encoding="utf-8-sig") as csv:
        csv.write(
            "title,upc,price_including_tax,price_excluding_tax,number_available,"
            "image,category,review_rating,product_description" + '\n')
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
        image_2 = images.attrs['src']
        image = 'https://books.toscrape.com/' + image_2.replace('../..', '')
        csv.write(
            title + ',' + upc + ',' + price_including_tax + ',' + price_excluding_tax + ',' + number_available + ',' +
            image + ',' + category + ',' + review_rating + ',' + product_description.replace(',', ''))    
'''

'''


def scrape_one_category():

    # Scrapper toutes les urls de livres appartenant à une catégorie
    hrefs = []
    url = "https://books.toscrape.com/"
    page = requests.get(url)
    soup_page = BeautifulSoup(page.text, 'html.parser')
    link_category = soup_page.find('ul', class_="nav-list").find('ul').findAll('a')
    for link in link_category:
        href = link['href'].replace('index.html', '')
        hrefs.append(href)
    url_category = url + hrefs[3]

    book_urls = []
    for i in range(9):
        url = url_category + 'page-' + str(i) + '.html'
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            h3s = soup.findAll('h3')

            for h3 in h3s:
                a = h3.find('a')
                link = a['href']
                book_urls.append('https://books.toscrape.com/catalogue' + link.replace('../../..', ''))
            time.sleep(3)
    print(book_urls)

    with open('scraping_one_category.csv', 'w', encoding="utf-8-sig") as file:
        file.write(
            "title,upc,price_including_tax,price_excluding_tax,number_available,"
            "image,category,review_rating,product_description" + '\n')
        for book in book_urls:
            url_book = book.strip()
            response = requests.get(url_book)
            soup_2 = BeautifulSoup(response.text, 'html.parser')

            title_bs = soup_2.find_all("h1")
            title = title_bs[0].string.replace(",", "").replace("\"", "")

            product_information = soup_2.find_all("td")
            upc = product_information[0].string
            price_excluding_tax = product_information[2].string.replace('Â', '')
            price_including_tax = product_information[3].string.replace('Â', '')
            number_available = product_information[5].string
            review_rating = product_information[6].string

            product_description_bs = soup_2.find_all("p")
            product_description = product_description_bs[3].string.replace("\"", "")

            category_bs = soup_2.find_all("a")
            category = category_bs[3].string

            image_bs = soup_2.find_all("img")
            images = image_bs[0]
            image_2 = images.attrs['src']
            image = 'https://books.toscrape.com/' + image_2.replace('../..', '')
            file.write(
                title + ', ' + upc + ', ' + price_including_tax + ', ' + price_excluding_tax + ', ' +
                number_available + ', ' + image + ', ' + category + ', ' +
                review_rating + ', ' + product_description.replace(',', '') + '\n')
'''


# Scrapper toutes les catégories
all_category_urls = []
url = 'https://books.toscrape.com/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
category_url = soup.find('ul', class_='nav nav-list').findAll('a')
for urls in category_url:
    href = urls['href'].replace('index.html', '')
    href_bs = url + href
    all_category_urls.append(href_bs)
del all_category_urls[0]

# Ajouter les pages additionnelles des catégories
full_category_urls = []
for all_category_urls_1 in all_category_urls:
    page_category = requests.get(all_category_urls_1)
    soup_category = BeautifulSoup(page_category.text, "html.parser")
    number_of_books_on_page = soup_category.find('form', class_="form-horizontal").find('strong').text
    if int(number_of_books_on_page) > 20:
        number_of_pages = ceil(int(number_of_books_on_page) / 20)
        for i in range(1, number_of_pages + 1):
            url_page = all_category_urls_1 + 'page-' + str(i) + '.html'
            full_category_urls.append(url_page)
    elif not int(number_of_books_on_page) > 20:
        full_category_urls.append(all_category_urls_1)

# Scrapper les urls des livres
all_books_urls = []
for urls in full_category_urls:
    page_book = requests.get(urls)
    soup_book = BeautifulSoup(page_book.text, 'html.parser')
    books = soup_book.findAll('div', class_="image_container")
    for product in books:
        a = product.find('a')
        url_book = a['href'].replace('../../..', '')
        url_book_bs = 'http://books.toscrape.com/catalogue' + url_book
        all_books_urls.append(url_book_bs)

with open('scraping_all_categories.csv', 'w', encoding="utf-8-sig") as file:
    file.write(
        "title,upc,price_including_tax,price_excluding_tax,number_available,"
        "image,category,review_rating,product_description" + '\n')
    for book in all_books_urls:
        url_book = book.strip()
        response = requests.get(url_book)
        soup_2 = BeautifulSoup(response.text, 'html.parser')

        title_bs = soup_2.find_all("h1")
        title = title_bs[0].string

        product_information = soup_2.find_all("td")
        upc = product_information[0].string
        price_excluding_tax = product_information[2].string
        price_including_tax = product_information[3].string
        number_available = product_information[5].string
        review_rating = product_information[6].string

        product_description_bs = soup_2.find_all("p")
        product_description = product_description_bs[3].string

        category_bs = soup_2.find_all("a")
        category = category_bs[3].string

        image_bs = soup_2.find_all("img")
        images = image_bs[0]
        image_2 = images.attrs['src']
        image = 'https://books.toscrape.com/' + image_2.replace('../..', '')
        file.write(
            title + ',' + upc + ',' + price_including_tax + ',' + price_excluding_tax + ',' +
            number_available + ',' + image + ',' + category + ',' +
            review_rating + ',' + product_description.replace(',', '') + '\n')

