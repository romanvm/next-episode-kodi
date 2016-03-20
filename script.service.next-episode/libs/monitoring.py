# coding: utf-8
# Created on: 17.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import xbmc
from xbmcgui import Dialog
from commands import sync_library, sync_new_items, login, addon
# Here ``addon`` is imported from another module to prevent a bug
# when username and hash are not stored in the addon settings.

dialog = Dialog()


class UpdateMonitor(xbmc.Monitor):
    """
    Monitors updating Kodi library
    """
    def onScanFinished(self, library):
        if library == 'video':
            sync_new_items()
            xbmc.log('next-episode.net: new items updated', xbmc.LOGNOTICE)


def initial_prompt():
    """
    Show login prompt at first start
    """
    if (addon.getSetting('prompt_shown') != 'true' and
            not addon.getSetting('username') and
            dialog.yesno('Login required!',
                         'You need to login to next-episode.net',
                         'to synchronize your video library data.',
                         'Login now?')):
        if login() and dialog.yesno('Library synchronization',
                                    'You need to synchronize your video library with next-episode.net.',
                                    'Synchronize now?'):
            sync_library()
        addon.setSetting('prompt_shown', 'true')
