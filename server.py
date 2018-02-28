#!/usr/bin/env python3
import tornado.ioloop
import tornado.web
import json
import logging
from uf.wrapper.swift_api import SwiftAPI


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, swift):
        self.swift = swift

    def post(self):
        data = json.loads(self.request.body.decode())
        logging.info(repr(data))
        func = getattr(self.swift, data['action'])
        results = func(**data['kwargs'])
        self.write(json.dumps(dict(results=results)))


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    swift = SwiftAPI()
    app = tornado.web.Application([('/', MainHandler, dict(swift=swift))])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
