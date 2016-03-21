# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: romanvm@yandex.ua

import pyxbmct
from libs.gui import NextEpDialog, ui_string
from libs.commands import sync_library, sync_new_items, login


class MainDialog(NextEpDialog):
    """
    Main UI dialog
    """
    def _set_controls(self):
        self._enter_login_btn = pyxbmct.Button(ui_string(32001))
        self.placeControl(self._enter_login_btn, 2, 0, columnspan=2)
        self._sync_library_btn = pyxbmct.Button(ui_string(32002))
        self.placeControl(self._sync_library_btn, 1, 0, columnspan=2)
        self._sync_new_btn = pyxbmct.Button('Synchronize new video items')
        self.placeControl(self._sync_new_btn, 0, 0, columnspan=2)

    def _set_connections(self):
        super(MainDialog, self)._set_connections()
        self.connect(self._sync_new_btn, sync_new_items)
        self.connect(self._sync_library_btn, sync_library)
        self.connect(self._enter_login_btn, self._enter_login)

    def _set_navigation(self):
        self._sync_new_btn.controlUp(self._enter_login_btn)
        self._sync_new_btn.controlDown(self._sync_library_btn)
        self._sync_library_btn.controlUp(self._sync_new_btn)
        self._sync_library_btn.controlDown(self._enter_login_btn)
        self._enter_login_btn.controlUp(self._sync_library_btn)
        self._enter_login_btn.controlDown(self._sync_new_btn)
        self.setFocus(self._sync_new_btn)

    def _enter_login(self):
        self.close()
        login()
        self.doModal()


if __name__ == '__main__':
    main_dialog = MainDialog('next-episode.net')
    main_dialog.doModal()
    del main_dialog
