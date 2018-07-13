#!/usr/bin/python3

from mastodon import Mastodon
#Register Stallminator app, should only need to be executed once

def main():
    print("Enter App Name: ")
    appName = input()

    print("Enter name of credential file: ")
    credentialFile = input()

    print("Enter name of instance URL: ")
    url = input()

    register_app(appName, credentialFile, url)

    print(appName, " has been succesfully registered");




def register_app(appName, credentialFile, url):

    SECRET_DIR = '/home/z/prj/mastobots/secrets/'

    Mastodon.create_app(
        appName,
        api_base_url = url,
        to_file = SECRET_DIR + credentialFile)


if __name__ == '__main__':
    main()
