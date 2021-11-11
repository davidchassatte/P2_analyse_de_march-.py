import requests
from bs4 import BeautifulSoup
import time


def scrape_one_category():

    # SCRAPPER LES INFORMATIONS DE TOUS LES LIVRES D'UNE MEME CATEGORIE
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

            product_description_bs = soup_2.find_all("p")
            product_description = product_description_bs[3].string.replace("\"", "")

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
                title + ', ' + upc + ', ' + price_including_tax + ', ' + price_excluding_tax + ', ' +
                number_available + ', ' + image + ', ' + category + ', ' +
                review_rating + ', ' + product_description.replace(',', '') + '\n')
