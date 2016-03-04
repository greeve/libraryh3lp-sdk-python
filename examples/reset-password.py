#!/usr/bin/env python

# reset-password.py
# -----------------
# Assign a new password to a user.

from xkcdpass import xkcd_password as xp

import argparse
import getpass
import lh3.api
import pyperclip

parser = argparse.ArgumentParser(description = "Reset a user's password.  Will generate a password if none is provided.")
parser.add_argument('username', help = 'change the password for this user')
parser.add_argument('--password', help = 'assign this password')
parser.add_argument('-p', '--prompt', help = 'prompt for the new password', action = 'store_true')
parser.add_argument('-c', '--clip', help = 'copy the generated password to the clipboard', action = 'store_true')

args = parser.parse_args()

password = args.password

if not password and args.prompt:
    password = getpass.getpass('Enter a new password for the user: ')

if not password:
    wordfile = xp.locate_wordfile()
    wordlist = xp.generate_wordlist(wordfile)
    password = xp.generate_xkcdpassword(wordlist, numwords = 4)

    if args.clip:
        pyperclip.copy(password)
        print('generated password has been copied to clipboard')
    else:
        print(password)

client = lh3.api.Client()
client.set_options(version = 'v1')
client.find_user_by_name(args.username).put({'password': password})
print('password has been changed')
