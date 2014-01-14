# -*- coding: utf-8 -*-

import tornado.escape
import tornado.ioloop
import tornado.web

import model

_streams = model.Streams()
_files = model.Files('files', _streams)

class StreamsHandler(tornado.web.RequestHandler):
    def get(self, index = None):  
        if index == None:
            json = tornado.escape.json_encode(_streams.data)
        else:
            json = tornado.escape.json_encode(_streams[index].data)
        self.write(json) 
    
    def put(self, index):
        data = tornado.escape.json_decode(self.request.body)
        stream = _streams.put(index, data)
        json = tornado.escape.json_encode(stream)
        self.write(json)  
  
class FilesHandler(tornado.web.RequestHandler):
    def get(self, index = None):  
        if index == None:
            json = tornado.escape.json_encode(_files.data)
        else:
            json = tornado.escape.json_encode(_files[index].data)
        self.write(json)
    
    def delete(self, index):
        _files.delete(index)
        self.write("null")
        
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        f = _files.post(data)
        json = tornado.escape.json_encode(f)
        self.write(json)   
    
    def put(self, index):
        data = tornado.escape.json_decode(self.request.body)
        f = _files.put(index, data)
        json = tornado.escape.json_encode(f)
        self.write(json)   

if __name__ == "__main__":
    application = tornado.web.Application(
        [
            (r"/", tornado.web.RedirectHandler, {"url": "/static/index.html"}),
            (r"/files", FilesHandler),
            (r"/files/([0-9]+)", FilesHandler),
            (r"/streams", StreamsHandler),
            (r"/streams/([0-9]+)", StreamsHandler)
        ],
        static_path="static"
    )
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()