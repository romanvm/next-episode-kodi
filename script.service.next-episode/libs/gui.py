# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

from abc import ABCMeta, abstractmethod
from xbmcaddon import Addon
import pyxbmct

addon = Addon()
ui = addon.getLocalizedString


class NextEpDialog(pyxbmct.AddonDialogWindow):
    """
    Base class for addon dialogs
    """
    __metaclass__ = ABCMeta

    def __init__(self, title=''):
        super(NextEpDialog, self).__init__(title)
        self.setGeometry(400, 210, 3, 2)
        self._set_controls()
        self._set_connections()
        self._set_navigation()

    @abstractmethod
    def _set_controls(self):
        pass

    @abstractmethod
    def _set_connections(self):
        pass

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
    pass


class MainDialog(NextEpDialog):
    """
    Main UI dialog
    """
    def _set_controls(self):
        self._sync_new_btn = pyxbmct.Button('Synchronize new video items')
        self.placeControl(self._sync_new_btn, 0, 0, columnspan=2)
        self._sync_library_btn = pyxbmct.Button('Synchronize Kodi video library')
        self.placeControl(self._sync_library_btn, 1, 0, columnspan=2)
        self._enter_login_btn = pyxbmct.Button('Enter login and password')
        self.placeControl(self._enter_login_btn, 2, 0, columnspan=2)

    def _set_connections(self):
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def _set_navigation(self):
        self._sync_new_btn.controlUp(self._enter_login_btn)
        self._sync_new_btn.controlDown(self._sync_library_btn)
        self._sync_library_btn.controlUp(self._sync_new_btn)
        self._sync_library_btn.controlDown(self._enter_login_btn)
        self._enter_login_btn.controlUp(self._sync_library_btn)
        self._enter_login_btn.controlDown(self._sync_new_btn)
        self.setFocus(self._sync_new_btn)

    def _sync_library(self):
        pass

    def _sync_new_items(self):
        pass

    def _enter_login(self):
        pass
