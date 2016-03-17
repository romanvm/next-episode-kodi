# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import xbmc
from libs.monitoring import UpdateMonitor

update_monitor = UpdateMonitor()
service_started = False
while not xbmc.abortRequested:
    if not service_started:
        xbmc.log('next-episode.net: service started', xbmc.LOGNOTICE)
        service_started = True
    xbmc.sleep(200)
