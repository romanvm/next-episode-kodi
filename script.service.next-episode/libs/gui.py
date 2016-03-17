# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

from abc import ABCMeta, abstractmethod
import xbmc
from xbmcaddon import Addon
from xbmcgui import Dialog, ACTION_NAV_BACK
import pyxbmct
from nextepisode import get_password_hash, prepare_movies_list, prepare_episodes_list, update_data, LoginError
from medialibrary import get_movies, get_tvshows, get_episodes

addon = Addon()
_ui = addon.getLocalizedString
dialog = Dialog()


class NextEpDialog(pyxbmct.AddonDialogWindow):
    """
    Base class for addon dialogs
    """
    __metaclass__ = ABCMeta

    def __init__(self, title=''):
        super(NextEpDialog, self).__init__(title)
        self.setGeometry(420, 210, 3, 2)
        self._set_controls()
        self._set_connections()
        self._set_navigation()

    @abstractmethod
    def _set_controls(self):
        pass

    @abstractmethod
    def _set_connections(self):
        self.connect(ACTION_NAV_BACK, self.close)

    @abstractmethod
    def _set_navigation(self):
        pass

    def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=250'),
                               ('WindowClose', 'effect=fade start=100 end=0 time=250')])


class LoginDialog(NextEpDialog):
    """
    Enter login/password dialog
    """
    def __init__(self, title='', username=''):
        super(LoginDialog, self).__init__(title)
        self.username = username
        self._username_field.setText(username)
        self.password = ''
        self.is_cancelled = True

    def _set_controls(self):
        login_label = pyxbmct.Label('Username:')
        self.placeControl(login_label, 0, 0)
        password_label = pyxbmct.Label('Password:')
        self.placeControl(password_label, 1, 0)
        self._username_field = pyxbmct.Edit('')
        self.placeControl(self._username_field, 0, 1)
        self._password_field = pyxbmct.Edit('', isPassword=True)
        self.placeControl(self._password_field, 1, 1)
        self._ok_btn = pyxbmct.Button('OK')
        self.placeControl(self._ok_btn, 2, 1)
        self._cancel_btn = pyxbmct.Button('Cancel')
        self.placeControl(self._cancel_btn, 2, 0)

    def _set_connections(self):
        super(LoginDialog, self)._set_connections()
        self.connect(self._ok_btn, self._ok)
        self.connect(self._cancel_btn, self.close)

    def _set_navigation(self):
        self._username_field.controlUp(self._ok_btn)
        self._username_field.controlDown(self._password_field)
        self._password_field.controlUp(self._username_field)
        self._password_field.controlDown(self._ok_btn)
        self._ok_btn.setNavigation(self._password_field, self._username_field, self._cancel_btn, self._cancel_btn)
        self._cancel_btn.setNavigation(self._password_field, self._username_field, self._ok_btn, self._ok_btn)
        self.setFocus(self._username_field)

    def _ok(self):
        self.is_cancelled = False
        self.username = self._username_field.getText()
        self.password = self._password_field.getText()
        self.close()

    def close(self):
        if self.is_cancelled:
            self.username = self.password = ''
        super(LoginDialog, self).close()


class MainDialog(NextEpDialog):
    """
    Main UI dialog
    """
    def _set_controls(self):
        self._sync_new_btn = pyxbmct.Button('Synchronize new video items')
        self.placeControl(self._sync_new_btn, 0, 0, columnspan=2)
        self._sync_library_btn = pyxbmct.Button('Synchronize Kodi video library')
        self.placeControl(self._sync_library_btn, 1, 0, columnspan=2)
        self._enter_login_btn = pyxbmct.Button('Enter username and password')
        self.placeControl(self._enter_login_btn, 2, 0, columnspan=2)
        if not addon.getSetting('hash'):
            Dialog().ok('Login required!', 'Select "Enter username and password" menu item',
                        'and enter credentials for next-episode.net.')

    def _set_connections(self):
        super(MainDialog, self)._set_connections()
        self.connect(self._sync_new_btn, self._sync_new_items)
        self.connect(self._sync_library_btn, self._sync_library)
        self.connect(self._enter_login_btn, self._enter_login)

    def _set_navigation(self):
        self._sync_new_btn.controlUp(self._enter_login_btn)
        self._sync_new_btn.controlDown(self._sync_library_btn)
        self._sync_library_btn.controlUp(self._sync_new_btn)
        self._sync_library_btn.controlDown(self._enter_login_btn)
        self._enter_login_btn.controlUp(self._sync_library_btn)
        self._enter_login_btn.controlDown(self._sync_new_btn)
        self.setFocus(self._sync_new_btn)

    def _sync_new_items(self):
        raise NotImplementedError

    def _sync_library(self):
        if dialog.yesno('Warning!', 'Are you sure you want to sync your video library\nwith next-episode.net?'):
            username = addon.getSetting('username')
            hash_ = addon.getSetting('hash')
            movies = prepare_movies_list(get_movies())
            episodes = []
            for show in get_tvshows():
                episodes += prepare_episodes_list(get_episodes(show['tvshowid']), show['imdbnumber'])
            data = {
                'user': {'username': username, 'hash': hash_},
                'movies': movies,
                'tvshows': episodes
            }
            xbmc.log('next-episode: data sent:\n{0}'.format(data), xbmc.LOGNOTICE)
            update_data(data)

    def _enter_login(self):
        self.close()
        login_dialog = LoginDialog('Login to next-episode.net', username=addon.getSetting('username'))
        login_dialog.doModal()
        if not login_dialog.is_cancelled:
            username = login_dialog.username
            password = login_dialog.password
            try:
                hash_ = get_password_hash(username, password)
            except LoginError:
                dialog.ok('Login error!', 'Check login/password and try again.')
            else:
                addon.setSetting('username', username)
                addon.setSetting('hash', hash_)
        self.doModal()
