import requests
import config as cfg
import datetime
import bs4
import keys


def return_movies(required_date=datetime.date.today()):
    """date = {
        'year': required_date.strftime('%Y'),
        'month': required_date.strftime('%m'),
        'day': required_date.strftime('%d')
    }"""
    params = {'date': required_date}
    classes = {'common': 'film-box-holder actual',
               'personal': 'film-box',
               'title': 'film-title',
               'link': 'btn-buy'}
    board_link = '{}{}'.format(
        cfg.links.get('main'), cfg.links.get('board')
    )

    r = requests.get(url=board_link,
                     params=params,
                     headers=cfg.headers)
    page = bs4.BeautifulSoup(r.text, features='html.parser')
    only_films = page.find('div', classes.get('common')
                           ).find_all('div',
                                      classes.get('personal'))

    answer = dict()

    for i in range(len(only_films)):
        film_name = only_films[i].find('a', classes.get('title')
                                       ).find('span').get_text()
        info_link = '{}{}'.format(
            cfg.links.get('main'),
            only_films[i].find('a', classes.get('link')).get('href'))
        answer[film_name] = info_link

    return answer


def info_about(info_link):
    classes = {
        'description': {'element': 'div', 'class': 'film-description'},
        'title': {'element': 'h3', 'class': 'title'},
        'translation': {'element': 'span', 'class': 'sub-title'},
        'image': {'element': 'div', 'class': 'img-holder'}
    }

    r = requests.get(info_link)
    page = bs4.BeautifulSoup(r.text, features='html.parser')
    film_data = {
        'title':
            page.find(classes.get('description').get('element'),
                      classes.get('description').get('class')
                      ).find('h3', {'class': 'title'}).get_text(),
        'translation':
            page.find(classes.get('description').get('element'),
                      classes.get('description').get('class')
                      ).find(classes.get('translation').get('element'),
                             classes.get('translation').get('class')
                             ).get_text(),
        'img_link':
            page.find(classes.get('description').get('element'),
                      classes.get('description').get('class')).find(
                classes.get('image').get('element'),
                classes.get('image').get(
                    'class')).find(
                'img').get('data-srcset').split(',')[1].split(' ')[1]
    }
    print(film_data)
    return film_data


def get_mdb_info(name):
    if name is None:
        return 'Name is None'
    params = {
        'apikey': keys.mdb_key,
        't': name
    }
    r = requests.get(url=cfg.links.get('omdb'), params=params)
    return r.json()
