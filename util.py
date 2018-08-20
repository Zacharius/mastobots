#!/usr/bin/python3

import os

def getAbsolutePath(file, relativePath):
   dirname = os.path.dirname(file)
   path = os.path.join(dirname, relativePath)
   return path

if __name__ == '__main__':
    print(getAbsolutePath(__file__, 'secrets/'))
