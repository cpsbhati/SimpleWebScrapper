from bs4 import BeautifulSoup
import requests

def scrape_web_page(URL):
    # make a get request
    response = requests.get(URL)
    response.raise_for_status() # raise HTTP errors

    soup = BeautifulSoup(response.content, 'html.parser')

    # find elements 
    heading = soup.find('h1')
    details = soup.find_all(class_ = "page-hero-list")

    # print elements
    # print heading
    print(heading.get_text(strip=True))
    # print details
    for element in details:
        print(element.get_text(strip=True))

URL = "https://www.learningtree.com/courses/cissp-training/"
scrape_web_page(URL)