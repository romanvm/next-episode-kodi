# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import json
import requests

API = 'http://next-episode.net/api/kodi/v1/update_data'


def send_data(data):
    """
    Send data to next-episode.net

    :param data: data to be sent
    :type data: dict
    """
    resp = requests.get(API, params={'data': json.dumps(data)}, headers={'Content-Type': 'application/json'})
    return resp.text


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
    print send_data(data)
