# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

from abc import ABCMeta, abstractmethod
from xbmcaddon import Addon
from xbmcgui import ACTION_NAV_BACK
import pyxbmct

addon = Addon()


def ui_string(id_):
    """
    Get localized UI string

    :param id_: string ID
    :type id_: int
    :return: localized string
    :rtype: unicode
    """
    return addon.getLocalizedString(id_).encode('utf-8')


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
