import requests
from bs4 import BeautifulSoup


def get_metacritic_score(name, platform='pc'):
    '''
        Scrape metacritic for user score and critic score
        Returns dict:
            {
                'user score': <user score>,
                'user count': <user count>,
                'critic score': <critic score>,
                'critic count': <critic count>
            }
    '''

    name = name.replace(' ', '-').lower()
    url = f'https://www.metacritic.com/game/{platform}/{name}'
    hdr = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=hdr)
        soup = BeautifulSoup(response.text, 'html.parser')

        critic_raiting = soup.find("span", itemprop="ratingValue").text

        user_raiting = soup.find_all(
            "div", class_='userscore_wrap feature_userscore')
        user_raiting = user_raiting[0].find('div', class_='metascore_w').text

        summary = soup.find_all('div', class_='summary')

        critic_count = summary[0].find('span', class_='').text.strip()

        user_count = summary[1].find('a').text.strip().split()[0]

        # Get game genres
        ar = soup.find('li', class_='summary_detail product_genre').find_all(
            'span', class_='data')
        genres = []
        for x in ar:
            genres.append(x.text)
        genres = ', '.join(genres)

        result = {
            'user score': user_raiting,
            'user count': user_count,
            'critic score': critic_raiting,
            'critic count': critic_count,
            'genres': genres
        }

        return result
    except Exception:
        print('Cant find game on metacritic')
        return None


get_metacritic_score('borderlands 3', platform='pc')
