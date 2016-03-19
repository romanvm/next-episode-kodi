# coding: utf-8
# Created on: 17.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import sys
import xbmc
from xbmcaddon import Addon
from xbmcgui import Dialog
from medialibrary import (get_movies, get_tvshows, get_episodes, get_recent_movies,
                          get_recent_episodes, get_tvdb_id, NoDataError)
from nextepisode import prepare_movies_list, prepare_episodes_list, update_data, get_password_hash, LoginError
from gui import LoginDialog

addon = Addon('script.service.next-episode')
dialog = Dialog()


def sync_library():
    """
    Syncronize Kodi video library with next-episode.net
    """
    if dialog.yesno('Warning!', 'Are you sure you want to sync your video library\nwith next-episode.net?'):
        episodes = []
        for show in get_tvshows():
            try:
                episodes += prepare_episodes_list(get_episodes(show['tvshowid']))
            except NoDataError:
                continue
        data = {
            'user': {
                'username': addon.getSetting('username'),
                'hash': addon.getSetting('hash')
            },
            'movies': prepare_movies_list(get_movies()),
            'tvshows': episodes
        }
        xbmc.log('next-episode: data sent:\n{0}'.format(data), xbmc.LOGNOTICE)
        update_data(data)


def sync_new_items():
    """
    Syncronize new video items with next-episode.net
    """
    data = {
        'user': {
            'username': addon.getSetting('username'),
            'hash': addon.getSetting('hash')
        },
        'movies': prepare_movies_list(get_recent_movies()),
        'tvshows': prepare_episodes_list(get_recent_episodes())
    }
    xbmc.log('next-episode: data sent:\n{0}'.format(data), xbmc.LOGNOTICE)
    update_data(data)


def update_single_item(item):
    """
    Syncronize single item (movie or episode) with next-episode-net

    :param item: video item
    :type item: dict
    """
    data = {
        'user': {
            'username': addon.getSetting('username'),
            'hash': addon.getSetting('hash')
        }}
    if item['type'] == 'episode':
        data['tvshows'] = [{
            'thetvdb_id': get_tvdb_id(item['tvshowid']),
            'season': str(item['season']),
            'episode': str(item['episode']),
            'watched': '1' if item['playcount'] else '0'
            }]
    elif item['type'] == 'movie':
        data['movies'] = [{
            'imdb_id': item['imdbnumber'],
            'watched': '1' if item['playcount'] else '0'
        }]
    xbmc.log('next-episode: data sent:\n{0}'.format(data), xbmc.LOGNOTICE)
    update_data(data)


def login():
    """
    Login to next-episode.net

    :return: ``True`` on successful login
    :rtype: bool
    """
    login_dialog = LoginDialog('Login to next-episode.net', username=addon.getSetting('username'))
    login_dialog.doModal()
    if not login_dialog.is_cancelled:
        username = login_dialog.username
        password = login_dialog.password
        try:
            hash_ = get_password_hash(username, password)
        except LoginError:
            dialog.ok('Login error!', 'Check login/password and try again.')
            xbmc.log('next-episode.net: login failed!', xbmc.LOGERROR)
            return False
        else:
            addon.setSetting('username', username)
            addon.setSetting('hash', hash_)
            xbmc.log('next-episode.net: successful login', xbmc.LOGNOTICE)
            dialog.notification('next-episode.net', 'Successful login', time=3000, sound=False)
            return True


if __name__ == '__main__':
    if sys.argv[1] == 'sync_library':
        sync_library()
    elif sys.argv[1] == 'sync_new_items':
        sync_new_items()
    elif sys.argv[1] == 'login':
        login()
