# coding: utf-8
# Created on: 17.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import xbmc
from commands import sync_new_items


class UpdateMonitor(xbmc.Monitor):
    """
    Monitors updating Kodi library
    """
    def onScanFinished(self, library):
        if library == 'video':
            sync_new_items()
            xbmc.log('next-episode.net: new items updated', xbmc.LOGNOTICE)
