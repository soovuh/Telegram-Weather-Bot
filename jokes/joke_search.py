import bs4
import requests


async def joke_search():
    url = 'https://www.anekdotua.com'
    response = requests.get(url)
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    text = soup.select('div[class = "marg5"]')[1].text
    if 'читати повністю' in text:
        elem = soup.select('div[class = "marg5"] > a[class = "menul"]')
        joke_url = elem[0].get('href')
        res = requests.get(joke_url)
        res.raise_for_status()
        sp = bs4.BeautifulSoup(res.text, features='html.parser')
        joke_text = sp.select('div[class = "marg10"]')[0].text
        return joke_text
    else:
        joke_text = ''
        for i in text:
            if i == '\n':
                break
            joke_text += i
        return joke_text
