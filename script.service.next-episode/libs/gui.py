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
        self.setGeometry(420, 210, 3, 2)
        self._set_controls()
        self._set_connections()
        self._set_navigation()

    @abstractmethod
    def _set_controls(self):
        pass

    @abstractmethod
    def _set_connections(self):
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

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
    def __init__(self, title='', parent=None, login=''):
        super(LoginDialog, self).__init__(title)
        self._parent = parent
        self.login = login
        self._login_field.setText(login)
        self.password = ''

    def _set_controls(self):
        login_label = pyxbmct.Label('Login:')
        self.placeControl(login_label, 0, 0)
        password_label = pyxbmct.Label('Password:')
        self.placeControl(password_label, 1, 0)
        self._login_field = pyxbmct.Edit('')
        self.placeControl(self._login_field, 0, 1)
        self._password_field = pyxbmct.Edit('', isPassword=True)
        self.placeControl(self._password_field, 1, 1)
        self._ok_btn = pyxbmct.Button('OK')
        self.placeControl(self._ok_btn, 2, 1)
        self._cancel_btn = pyxbmct.Button('Cancel')
        self.placeControl(self._cancel_btn, 2, 0)

    def _set_connections(self):
        super(LoginDialog, self)._set_connections()
        self.connect(self._ok_btn, self._ok)
        self.connect(self._cancel_btn, self._cancel)

    def _set_navigation(self):
        self._login_field.controlUp(self._ok_btn)
        self._login_field.controlDown(self._password_field)
        self._password_field.controlUp(self._login_field)
        self._password_field.controlDown(self._ok_btn)
        self._ok_btn.setNavigation(self._password_field, self._login_field, self._cancel_btn, self._cancel_btn)
        self._cancel_btn.setNavigation(self._password_field, self._login_field, self._ok_btn, self._ok_btn)
        self.setFocus(self._login_field)

    def doModal(self):
        self._parent.close()
        super(LoginDialog, self).doModal()

    def _ok(self):
        self.login = self._login_field.getText()
        self.password = self._password_field.getText()
        self.close()

    def _cancel(self):
        self.login = self.password = ''
        self.close()

    def close(self):
        super(LoginDialog, self).close()
        self._parent.doModal()


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
        pass

    def _sync_library(self):
        pass

    def _enter_login(self):
        login_dialog = LoginDialog('Login to next-episode.net', parent=self, login=addon.getSetting('login'))
        login_dialog.doModal()
        del login_dialog
