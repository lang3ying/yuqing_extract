import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.httpclient
import platform
from tornado import gen
from gne import GeneralNewsExtractor



from tornado.options import define, options
define("port", default=9999, help="run on the given port", type=int)

if platform.system() == "Windows":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

extractor = GeneralNewsExtractor()

class IndexHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield client.fetch("https://www.baidu.com")
        self.write('response')

    @gen.coroutine
    def post(self):
        htmlStr = self.request.body_arguments['content'][0].decode()
        result = self.content_extract(htmlStr)
        self.write({"data":result})

    def content_extract(self,htmlStr):
        result = extractor.extract(htmlStr)
        # print(result)
        return result

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/getData", IndexHandler)
        ],
        debug=True,

    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
