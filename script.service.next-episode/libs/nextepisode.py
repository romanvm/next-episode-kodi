# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import json
import urllib2
from contextlib import closing
import xbmc
from medialibrary import get_tvdb_id

UPDATE_DATA = 'https://next-episode.net/api/kodi/v1/update_data'
LOGIN = 'https://next-episode.net/api/kodi/v1/login'


class LoginError(Exception):
    pass


def web_client(url, data=None):
    """
    Send/receive data to/from next-episode.net

    :param url: url to open
    :type url: str
    :param data: data to be sent in a POST request
    :type data: dict
    """
    if data is not None:
        data = json.dumps(data)
    request = urllib2.Request(url, data, headers={'Content-Type': 'application/json'})
    with closing(urllib2.urlopen(request)) as response:
        result = response.read()
        xbmc.log('next-episode reply:\n{0}'.format(result), xbmc.LOGNOTICE)
        return result


def update_data(data):
    """
    Update movies/tvshows data

    :param data: data to be send to next-episode.net
    :type data: dict
    :return: next-episode.net response
    """
    return web_client(UPDATE_DATA, data)


def get_password_hash(username, password):
    """
    Get password hash from next-episode.net

    :param username: next-episode username
    :type username: str
    :param password: next-episode password
    :type password: str
    :return: password hash
    :rtype: str
    :raises: LoginError if login fails
    """
    response = json.loads(web_client(LOGIN, {'username': username, 'password': password}))
    if 'error' in response:
        raise LoginError
    return response['hash']


def prepare_movies_list(raw_movies):
    """
    Prepare the list of movies to be sent to next-episodes.net

    :param raw_movies: raw movie list from Kodi
    :type raw_movies: list
    :return: prepared list
    :rtype: list
    """
    listing = []
    for movie in raw_movies:
        imdb_id = movie['imdbnumber']
        watched = '1' if int(movie['playcount']) else '0'
        listing.append({'imdb_id': imdb_id, 'watched': watched})
    return listing


def prepare_episodes_list(raw_episodes):
    """
    Prepare the list of TV episodes to be sent to next-episode.net

    :param raw_episodes: raw episode list for a TV show from Kodi
    :type raw_episodes: list
    :return: prepared list
    :rtype: list
    """
    listing = []
    thetvdb_id_map = {}
    for episode in raw_episodes:
        season_n = str(episode['season'])
        episode_n = str(episode['episode'])
        watched = '1' if int(episode['playcount']) else '0'
        if not thetvdb_id_map.get(episode['tvshowid']):
            thetvdb_id_map[episode['tvshowid']] = get_tvdb_id(episode['tvshowid'])
        listing.append({'thetvdb_id': thetvdb_id_map[episode['tvshowid']], 'season': season_n, 'episode': episode_n,
                        'watched': watched})
    return listing


if __name__ == '__main__':
    data = {
        'user': {'username': 'foo',
                 'hash': 'bar'},
        'tvshows': [
            {'thetvdb_id': '76290', 'season': '1', 'episode': '1', 'watched': '1'},
            {'thetvdb_id': '76290', 'season': '1', 'episode': '2', 'watched': '0'}
        ],
        'movies': [
            {'imdb_id': 'tt1431045', 'watched': '1'},
        ]}

    login = {'username': 'test','password': 'test123'}
    print update_data(data)
    print get_password_hash(login['username'], login['password'])
