#!/usr/bin/env python
#coding=utf-8

from __future__ import print_function
import time
from init_db import db
from handlers.utils import username_validator
import hashlib

username = email = ''

while True:
    username = raw_input('username:')
    if not username_validator.match(username):
        print("Invalid username")
        continue
    if not db.members.find_one({'name_lower': username.lower()}):
        break
    else:
        print("This username is already registered")

while True:
    email = raw_input('email:').lower()
    if not db.members.find_one({'email': email}):
        break
    print("This email is already registered")

password = raw_input('password:')
password = hashlib.sha1(password + username.lower()).hexdigest()

db.members.insert({
'name': username,
'name_lower': username.lower(),
'password': password,
'email': email,
'website': '',
'description': '',
'created': time.time(),
'role': 3,
'block': [],
'like': [],  # topics
'follow': [],  # users
'favorite': []  # nodes
})
