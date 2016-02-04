#!/usr/bin/env python
"""Send a direct message as Jarvis to a specified user.

Usage:
  send.py --user=<name> <message>...
  send.py (-h | --help)

Options:
  -u --user=<name>  Full name of user to send to
  -h --help         Show this screen.
"""
import json
import os

import docopt
import slackclient


USER = 'Jarvis'


args = docopt.docopt(__doc__)


token = os.environ['SLACK_TOKEN']
slack = slackclient.SlackClient(token)


users = json.loads(slack.api_call('users.list'))
uuids = {u['profile']['real_name']: u['id'] for u in users['members']}
icons = {u['profile']['real_name']: u['profile']['image_48']
         for u in users['members']}

channel = json.loads(
    slack.api_call('im.open', user=uuids[args.get('--user')]))['channel']['id']


slack.api_call('chat.postMessage', channel=channel,
               text=' '.join(args.get('<message>')), username=USER,
               icon_url=icons[USER])
