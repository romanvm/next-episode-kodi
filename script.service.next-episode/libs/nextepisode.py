# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import json
import urllib2
from contextlib import closing

UPDATE_DATA = 'https://next-episode.net/api/kodi/v1/update_data'
LOGIN = 'https://next-episode.net/api/kodi/v1/login'


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
        return response.read()


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
    """
    return json.loads(web_client(LOGIN, {'username': username, 'password': password}))['hash']


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
