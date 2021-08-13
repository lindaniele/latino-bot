from bs4 import BeautifulSoup
import requests
from re import sub


def outcome(soup) -> tuple[str, list[str]]:
    """
    Get paradigm/grammar and translations from latin word.

    :param soup: soup from Beautiful Soup
    :return: paradigm/grammar and translations of a word
    """
    result = ', '.join(sub(r'\(.*\) ', '', span.text) for span in soup.find_all('span', class_='italiano')).split(', ')
    paradigm = soup.find('div', id='myth').findAll('span')[1].text
    return paradigm, result


async def latin(word: str) -> list[tuple[str, list[str], str]]:
    """
    Translates word from Latin to Italian.

    :param word: latin word to be translated
    :return: a list of possible meanings; per each: paradigm/grammar (str), translations (list) and link
    """

    # Request and search translation on online dictionary Olivetti
    link = f'https://www.dizionario-latino.com/dizionario-latino-italiano.php?parola={word}'
    soup = BeautifulSoup(requests.get(link).text, 'lxml')

    # If there's only one definition
    find = soup.find_all('span', class_='italiano')
    if find:
        result = ', '.join(sub(r'\(.*\) ', '', span.text) for span in find).split(', ')
        paradigm = soup.find('div', id='myth').findAll('span')[1].text
        return [(paradigm, result, link)]

    # If there are multiple definitions
    hrefs = soup.find_all('td', {'width': '80%', 'align': 'left'})
    if hrefs:
        links = set(f"https://www.dizionario-latino.com/{href.a['href']}" for href in hrefs)
        return [outcome(BeautifulSoup(requests.get(link).text, 'lxml'))+(link,) for link in links]

    # If there are None
    return []


def search(s: str) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
    """
    Search for texts in latin or italian.

    :param s: text to be searched
    :return: results categorized into "frasi" and "versioni"; each: link and text(s)
    """
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


def text_info(link: str) -> tuple[str, str]:
    """
    Drops info of selected text

    :param link: link of the text
    :return: text info, unfortunately without translation, which can be accessed via link
    """
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    title = soup.find("span", class_="titolo").text
    if link.split("/")[3] == "frase":
        text = soup.find("td", style="color:#5c0082;font-size:22px; text-align:justify;").text
    else:
        text = soup.find("span", class_="notranslate").text
    return title, text


def mouseover(word: str) -> str:
    """
    Searches word information on William Whitaker's WORDS.

    :param word: word to be searched
    :return: info of latin word
    """
    request = requests.get(f'https://archives.nd.edu/cgi-bin/wordz.pl?keyword={word}')
    return BeautifulSoup(request.text, 'lxml').find('pre').text
