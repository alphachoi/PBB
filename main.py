#!/usr/bin/env python
#coding=utf-8

import os
import tornado.httpserver
import tornado.ioloop
import tornado.locale
import tornado.options
import tornado.web
from tornado.options import define, options
from init_db import db
import urls

ROOT = os.path.abspath(os.path.dirname(__file__))

define('port', default=8888, help='run on the given port', type=int)
define('settings', default=os.path.join(ROOT, 'settings.py'), help='path to the settings file.', type=str)


class Application(tornado.web.Application):
    def __init__(self):
        settings = {'template_path': os.path.join(ROOT, "templates"),
                    'role': {1: 'Member',
                             2: 'Admin',
                             3: 'SuperAdmin'}}
        execfile(options.settings, {}, settings)

        if 'static_path' not in settings:
            settings['static_path'] = os.path.join(ROOT, "static")

        super(Application, self).__init__(urls.handlers,
            ui_modules=urls.ui_modules, login_url='/account/signin',
            **settings)

        self.db = db

        tornado.locale.load_translations(os.path.join(ROOT, "locale"))
        tornado.locale.set_default_locale('zh_CN')


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
