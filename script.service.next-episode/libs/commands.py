# coding: utf-8
# Created on: 17.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import xbmc
from xbmcaddon import Addon
from xbmcgui import Dialog
from medialibrary import get_movies, get_tvshows, get_episodes, get_recent_movies, get_recent_episodes
from nextepisode import prepare_movies_list, prepare_episodes_list, update_data

addon = Addon()
dialog = Dialog()


def sync_library():
    """
    Syncronize Kodi video library with next-episode.net
    """
    if dialog.yesno('Warning!', 'Are you sure you want to sync your video library\nwith next-episode.net?'):
        episodes = []
        for show in get_tvshows():
            episodes += prepare_episodes_list(get_episodes(show['tvshowid']))
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
