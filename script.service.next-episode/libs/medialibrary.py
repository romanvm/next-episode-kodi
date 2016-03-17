# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import json
import xbmc


def json_request(method, params):
    """
    Send JSON-RPC to Kodi

    :param method: Kodi JSON-RPC method
    :type method: str
    :param params: method parameters
    :type params: dict
    :return: JSON-RPC response
    :rtype: dict
    """
    result = xbmc.executeJSONRPC(json.dumps({
        'jsonrpc': '2.0', 'method': method, 'params': params, 'id': '1'
    }))
    xbmc.log('JSON-RPC reply: {0}'.format(result), xbmc.LOGNOTICE)
    return json.loads(result)


def get_movies():
    """
    Get the list of movies from the Kodi database

    :return: the list of movie data as Python dicts like this:
        ``{u'imdbnumber': u'tt1267297', u'playcount': 0, u'movieid': 2, u'label': u'Hercules'}``
    :rtype: list
    """
    params = {'properties': ['imdbnumber', 'playcount'], 'sort': {'order': 'ascending', 'method': 'label'}}
    return json_request('VideoLibrary.GetMovies', params)['result']['movies']


def get_tvshows():
    """
    Get te list of TV shows from the Kodi database

    :return: the list of TV show data as Python dicts like this:
        {u'imdbnumber': u'247897', u'tvshowid': 3, u'label': u'Homeland'}
    :rtype: list
    """
    params = {'properties': ['imdbnumber'], 'sort': {'order': 'ascending', 'method': 'label'}}
    return json_request('VideoLibrary.GetTVShows', params)['result']['tvshows']


def get_episodes(tvshowid):
    """
    Get the list of episodes from a specific TV show

    :param tvshowid: internal Kodi database ID for a TV show
    :type tvshowid: str
    :return: the liso of episode data as Python dicts like this:
        ``{u'season': 4, u'playcount': 0, u'episode': 1, u'episodeid': 5, u'label': u'4x01. The Drone Queen'}``
    :rtype: list
    """
    params = {'tvshowid': tvshowid, 'properties': ['season', 'episode', 'playcount', 'tvshowid']}
    return json_request('VideoLibrary.GetEpisodes', params)['result']['episodes']


def get_tvdb_id(tvshowid):
    """
    Get TheTVDB ID for a TV show

    :param tvshowid: internal Kodi database ID for a TV show
    :type tvshowid: str
    :return: TheTVDB ID
    :rtype: str
    """
    params = {'tvshowid': tvshowid, 'properties': ['imdbnumber']}
    return json_request('VideoLibrary.GetTVShowDetails', params)['result']['tvshowdetails']['imdbnumber']


def get_recent_movies():
    """
    Get the list of recently added movies

    :return: the list of recent movies
    :rtype: list
    """
    params = {'properties': ['imdbnumber', 'playcount']}
    return json_request('VideoLibrary.GetRecentlyAddedMovies', params)['result']['movies']


def get_recent_episodes():
    """
    Get the list of recently added episodes

    :return: the list of recent episodes
    :rtype: list
    """
    params = {'properties': ['playcount', 'tvshowid', 'season', 'episode']}
    return json_request('VideoLibrary.GetRecentlyAddedEpisodes', params)['result']['episodes']
