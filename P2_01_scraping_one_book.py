import requests
from bs4 import BeautifulSoup


def scrape_book_information():

    # SCRAPPER LES INFORMATIONS D'UN LIVRE
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

        product_description_bs = soup.find_all("p")
        product_description = product_description_bs[3].string

        category_bs = soup.find_all("a")
        category = category_bs[3].string

        image_bs = soup.find_all("img")
        images = image_bs[0]
        image_2 = images.attrs['src']
        image = 'https://books.toscrape.com/' + image_2.replace('../..', '')

        # récupération du paragraphe star-rating
        review_rating_bs = soup.find("p", class_='star-rating')
        # paragraphe star-rating récuperé: review_rating_bs

        # récupération de la liste des classes du paragraphe
        review_rating_classes = review_rating_bs['class']
        # liste des classes du paragraphe récupérées: review_rating_classes

        # récupération de la position de star-rating dans le tableau review_rating_class
        star_rating_index = review_rating_classes.index('star-rating')
        # position de star_rating récupéré: star_rating_index

        # enlèvement de l'index star_rating_index
        review_rating_classes.pop(star_rating_index)
        # afficher ce qui reste dans review_rating_classes: review_rating_classes

        # récupération de ce qui reste dans review_rating_classes
        review_rating = review_rating_classes[0] + ' star(s)'
        # ce qui est resté dans review_rating_classes: review_rating
        csv.write(
            title + ',' + upc + ',' + price_including_tax + ',' + price_excluding_tax + ',' + number_available + ',' +
            image + ',' + category + ',' + review_rating + ',' + product_description.replace(',', ''))
