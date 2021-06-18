from bs4 import BeautifulSoup
import requests
from re import sub


# Return the paradigm and the translations of a word
def outcome(soup):
    result = ', '.join(sub(r'\(.*\) ', '', span.text) for span in soup.find_all('span', class_='italiano')).split(', ')
    paradigm = soup.find('div', id='myth').findAll('span')[1].text
    return paradigm, result


# Make a request to an Online Dictionary
def latin(word):

    # Search translation on Dizionario Olivetti
    soup = BeautifulSoup(
        requests.get(f'https://www.dizionario-latino.com/dizionario-latino-italiano.php?parola={word}').text, 'lxml'
    )

    # If there's only one definition
    find = soup.find_all('span', class_='italiano')
    if find:
        result = ', '.join(sub(r'\(.*\) ', '', span.text) for span in find).split(', ')
        paradigm = soup.find('div', id='myth').findAll('span')[1].text
        return [(paradigm, result)]

    # If there are multiple definitions
    hrefs = soup.find_all('td', {'width': '80%', 'align': 'left'})
    if hrefs:
        links = set(href.a['href'] for href in hrefs)
        return [outcome(BeautifulSoup(requests.get(f'https://www.dizionario-latino.com/{link}').text, 'lxml')) for link in links]

    # If there are None
    return []


# Search for latin texts
def search(s):
    source = requests.get(f'http://www.latin.it/search.htm?q={s}').text
    soup = BeautifulSoup(source, 'lxml')
    texts = soup.find_all('td', class_='hr')
    frasi, versioni = [], []

    # Separate what found by category
    for text in texts:
        href = text.a
        group = href['href'].split('/')[3]

        if group == 'frase':
            frasi.append((href['href'], href.text))
        elif group == 'versione':
            versioni.append((href['href'], href.text, text.find('div', class_='sep').next_sibling))

    return frasi, versioni


def text_info(link):
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    title = soup.find("span", class_="titolo").text
    if link.split("/")[3] == "frase":
        text = soup.find("td", style="color:#5c0082;font-size:22px; text-align:justify;").text
    else:
        text = soup.find("span", class_="notranslate").text
    return title, text
