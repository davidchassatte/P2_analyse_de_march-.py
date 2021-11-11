from P2_01_scraping_one_book import scrape_book_information
from P2_02_scraping_one_category import scrape_one_category
from P2_03_scraping_all_categories import scrape_everything


def menu():
    print('Appuyez sur [1] pour: scrapper les informations d\'un livre.')
    print('Appuyez sur [2] pour: scrapper tous les livres d\'une catégorie.')
    print('Appuyez sur [3] pour: scrapper tous les livres du site.')
    print('[0] Exit')
    print()


menu()
option = int(input('Veuillez entrer votre option: '))

while option != 0:
    if option == 1:
        scrape_book_information()
        print('Vous avez scrappé toutes les informations d\'un livre!')
    elif option == 2:
        scrape_one_category()
        print('Vous avez scrappé tous les livres appartenant à une même catégorie!')
    elif option == 3:
        scrape_everything()
        print('Vous avez scrappé tous les livres du site!')
    else:
        print('Option invalide')

    print()
    menu()
    option = int(input('Veuillez entrer votre option: '))

print('Merci d\'avoir utilisé ce programme.')
print('Au revoir!')
