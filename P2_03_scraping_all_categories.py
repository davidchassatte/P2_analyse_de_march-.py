import requests
from bs4 import BeautifulSoup
import pandas as pd
from math import ceil
import os


def scrape_everything():

    # SCRAPPER LE SITE ENTIER

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

    # ECRIRE LE FICHIER CSV

    with open('scraping_all_categories.csv', 'w', encoding='utf-8-sig') as file:
        file.write("title,upc,price_excluding_tax,price_including_tax,number_available,"
                   "image,category,review_rating,product_description" + '\n')
        for book in all_books_urls:
            url_book2 = book.strip()
            response = requests.get(url_book2)
            soup_2 = BeautifulSoup(response.text, 'html.parser')

            title_bs = soup_2.find_all("h1")
            title = title_bs[0].string.replace(",", "").replace("\"", "")

            product_information = soup_2.find_all("td")
            upc = product_information[0].string
            price_excluding_tax = product_information[2].string.replace('Â', '')
            price_including_tax = product_information[3].string.replace('Â', '')
            number_available = product_information[5].string

            product_description_bs = soup_2.find_all("p")
            product_description = product_description_bs[3].string

            category_bs = soup_2.find_all("a")
            category = category_bs[3].string

            image_bs = soup_2.find_all("img")
            images = image_bs[0]
            image_2 = images.attrs['src']
            image = 'https://books.toscrape.com/' + image_2.replace('../..', '')

            review_rating_bs = soup_2.find("p", class_='star-rating')
            review_rating_classes = review_rating_bs['class']
            star_rating_index = review_rating_classes.index('star-rating')
            review_rating_classes.pop(star_rating_index)
            review_rating = review_rating_classes[0] + ' star(s)'
            file.write(
                str(title) + ',' + str(upc) + ',' + str(price_excluding_tax) + ',' + str(price_including_tax) + ',' +
                str(number_available) + ',' + str(image) + ',' + str(category) + ',' + str(review_rating) + ',' +
                str(product_description).replace(",", "").replace("\"", "") + '\n')

    # TELECHARGER LES IMAGES

    # On crée un path avec plusieurs arguments, notre premier argument est une fonction qui permet de
    # situer où l'on est actuellement et le deuxième argument est le nom de notre dossier
    os.mkdir(os.path.join(os.getcwd(), 'images'))

    # On se place dans le dossier
    os.chdir(os.path.join(os.getcwd(), 'images'))

    for book in all_books_urls:
        url_book2 = book.strip()
        response = requests.get(url_book2)
        soup_2 = BeautifulSoup(response.text, 'html.parser')

        product_information = soup_2.find_all("td")
        upc = product_information[0].string

        image_bs = soup_2.find_all("img")
        images = image_bs[0]
        image_2 = images.attrs['src']
        image = 'https://books.toscrape.com/' + image_2.replace('../..', '')

        with open(upc.replace(' ', '-') + '.jpg', 'wb') as f:
            im = requests.get(image)
            f.write(im.content)

    # CREER UN FICHIER CSV POUR CHAQUE CATEGORIE

    os.mkdir(os.path.join(os.getcwd(), 'catégories_CSV'))
    df = pd.read_csv('scraping_all_categories.csv')
    categories = df.category

    os.chdir(os.path.join(os.getcwd(), 'catégories_CSV'))
    for category3 in categories:
        category2 = df[(df['category'] == str(category3))]
        category2.to_csv(str(category3) + '.csv')
