#!/usr/bin/python3

import sys
import time
from subprocess import Popen

print('First initialization...')
p = Popen(['python', 'compchembiobot.py'])

while True:

    if p.poll() is None:
        print('Process is already running...')
    else:
        print('Process is not active. Initiating...')
        p = Popen(['python', 'compchembiobot.py'])
    time.sleep(120)