#!/usr/bin/python3

from mastodon import Mastodon
from parser import getNewPosts
import os

def main():

    stallminator = login()
    entries = getNewPosts()
    long = 1
    short = 1000

    for entry in entries:
        entry
    
def login():
    access = Mastodon(
        client_id = "stallminator_clientcred.secret")

    access.log_in(
        'zach.faddis@gmail.com',
        os.environ['STALLMINATOR_PASSWORD'],
        to_file = 'stallminator_usercred.secret')

    stallminator = Mastodon(
        access_token = 'stallminator_usercred.secret')

    return stallminator

if __name__ == '__main__':
    main()
