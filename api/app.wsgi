import sys
sys.path.insert(0, "/home/smartroom/api")
sys.path.insert(1, "/home/smartroom/plugins")

import bottle
import api
application = bottle.default_app()
