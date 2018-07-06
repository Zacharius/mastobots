#!/usr/bin/python3

from mastodon import Mastodon
#Register Stallminator app, should only need to be executed once

Mastodon.create_app(
    'stallminator',
    to_file = 'stallminator_clientcred.secret')
