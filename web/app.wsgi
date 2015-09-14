import sys
sys.path.insert(0, "/home/smartroom/web")
sys.path.insert(0, "/home/smartroom/plugins/beaker")

import bottle
import web
#application = bottle.default_app()

import beaker.middleware

session_opts = {
    "session.type": "file",
    "session.cookie_expires": 300,
    "session.data_dir": "./data",
    "session.auto": True
}
application = beaker.middleware.SessionMiddleware(bottle.default_app(), session_opts)

#from web import app
#application = app

