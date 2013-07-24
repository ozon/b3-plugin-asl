# -*- coding: utf-8 -*-

# Weaponlimiter Plugin for BigBrotherBot(B3)
# Copyright (c) 2012 Harry Gabriel <rootdesign@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import b3
import b3.events
import b3.plugin
from ConfigParser import NoOptionError

__version__ = '0.0.1'
__author__ = 'ozon'


class AslPlugin(b3.plugin.Plugin):
    _adminPlugin = None
    requiresConfigFile = False
    _default_messages = {}
    _guids = list()
    _action = 'kick'

    def onLoadConfig(self):
        try:
            self._action = self.config.get('settings', 'action')
        except NoOptionError:
            self.debug('using default setting')
            pass

    def onStartup(self):
        """ Initialize plugin settings """
        # try to load admin plugin
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return False

        self.update_guids()
        self.registerEvent(b3.events.EVT_CLIENT_AUTH)
        self.registerEvent(b3.events.EVT_CLIENT_DISCONNECT)

    def onEvent(self, event):
        """ Handle EVT_CLIENT_CONNECT and EVT_CLIENT_DISCONNECT """
        if event.type == b3.events.EVT_CLIENT_AUTH:
            # do action if check for existing GUID is true
            if event.client.guid in self._guids:
                self.debug('Client GUID: %s is already connected.' % event.client.guid)

                if self._action == 'kick':
                    self.console.kick(event.client, self.getMessage('kick_reason'), None, True)

            else:
                self.update_guids()

        if event.type == b3.events.EVT_CLIENT_DISCONNECT:
            self.update_guids()

    def update_guids(self):
        """ Refresh GUID list """
        self._guids = [c.guid for c in self.console.clients.getList()]


if __name__ == '__main__':
    from b3.fake import fakeConsole, superadmin, joe, simon
    import time

    p = AslPlugin(fakeConsole, 'conf/plugin_asl.ini')

    p.onStartup()
    time.sleep(2)

    superadmin.connects(cid=0)
    # make joe connect to the fake game server on slot 1
    joe.connects(cid=1)
    # make joe connect to the fake game server on slot 2
    simon.connects(cid=2)
    # superadmin put joe in group user
    superadmin.says('!putgroup joe user')
    superadmin.says('!putgroup simon user')

    superadmin.connects(cid=0)
