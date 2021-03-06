"""
This module allows you to interact with my status; do stop in and say "hello"!
Admins can also tell me to "shut down" for repairs or to "update yourself".
"""
import logging
import os
import subprocess
import sys

import jarvis.core.helper as helper
import jarvis.core.messages as messages
import jarvis.core.plugin as plugin
import jarvis.db.channels as channels


logger = logging.getLogger(__name__)


class Status(plugin.Plugin):
    def __init__(self, slack):
        super(Status, self).__init__(slack, 'status')

        for channel in channels.ChannelsDal.read(admin_only=True):
            ch = helper.get_channel_or_fail(logger, self.slack, channel)
            self.send_now(ch, messages.ONLINE())

    def help(self, ch):
        self.send_now(ch, __doc__.replace('\n', ' '))

    @plugin.Plugin.require_auth
    @plugin.Plugin.on_message(r'.*(power|shut) (off|down).*')
    def die(self, ch, _user, _groups):
        self.send_now(ch, messages.ACKNOWLEDGE())
        sys.exit(0)

    @plugin.Plugin.require_auth
    @plugin.Plugin.on_message(r'.*update yourself.*')
    def update(self, ch, _user, _groups):
        if not os.path.isdir('/etc/jarvis'):
            self.send_now(ch, messages.ERROR_NOT_ENABLED('auto-update'))
            return

        self.send_now(ch, messages.UPDATING())
        subprocess.Popen(['/usr/bin/env', 'bash', '/etc/jarvis/bin/update'],
                         cwd='/etc/jarvis')

    @plugin.Plugin.on_message(r".*i'm (back|home).*")
    def home(self, ch, _user, _group):
        self.send(ch, messages.WELCOME_HOME())

    @plugin.Plugin.on_message(r".*hello|(you (there|up)).*")
    def you_there(self, ch, _user, _groups):
        self.send(ch, messages.GREET())
