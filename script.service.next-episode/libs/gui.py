# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

from xbmcgui import ACTION_NAV_BACK
import pyxbmct


class LoginDialog(pyxbmct.AddonDialogWindow):
    """
    Enter login/password dialog
    """
    def __init__(self, title='', username=''):
        super(LoginDialog, self).__init__(title)
        self.setGeometry(400, 200, 3, 2)
        self._set_controls()
        self._set_connections()
        self._set_navigation()
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
        self.connect(ACTION_NAV_BACK, self.close)
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
