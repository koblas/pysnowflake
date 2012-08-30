#!/usr/bin/env python

# tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import idhandler
from tornado.options import define, options, parse_command_line

################################################################################

define("debug", default=False, help="run in debug mode", type=bool)
define("port", default=9000, help="run on the given port", type=int)
define("prefork", default=False, help="pre-fork across all CPUs", type=bool)
define("datacenter", default=0, help="Datacenter Identifier", type=int)
define("worker", default=0, help="Worker Identifier", type=int)

class Application(tornado.web.Application):
    def __init__(self, xsrf_cookies=True):
        handlers = [
            (r'/id/(.*)', idhandler.IdHandler),
            (r'/timestamp/', idhandler.TimestampHandler),
            (r'/worker/', idhandler.WorkerHandler),
            (r'/datacenter/', idhandler.DatacenterHandler),
        ]

        app_settings = {
            'debug': options.debug,
        }

        self.idworker = idhandler.IdWorker(data_center_id=options.datacenter, worker_id=options.worker)

        super(Application, self).__init__(handlers, **app_settings)

def main(): # pragma: no cover
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())

    print "Starting tornado on port", options.port
    if options.prefork:
        print "\tpre-forking"
        http_server.bind(options.port)
        http_server.start()
    else:
        http_server.listen(options.port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
