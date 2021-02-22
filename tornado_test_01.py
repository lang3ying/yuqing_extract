import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.httpclient
import platform
from tornado import gen
from gne import GeneralNewsExtractor



from tornado.options import define, options
define("port", default=9998, help="run on the given port", type=int)

if platform.system() == "Windows":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

extractor = GeneralNewsExtractor()

class IndexHandler(tornado.web.RequestHandler):
    # TODO 通过post请求传过来的htmlStr 网页源码,运用gne工具包进行字段内容的自动提取,并返回json字符串
    @gen.coroutine
    def post(self):
        htmlStr = self.request.body_arguments['content'][0].decode()
        result = self.content_extract(htmlStr)
        self.write({"data":result})

    def content_extract(self,htmlStr):
        result = extractor.extract(htmlStr)
        # print(result)
        return result


class GetHtmlStr(tornado.web.RequestHandler):
    # TODO 通过请求url获取响应response.body.然后返回响应
    #@gen.coroutine
    async def get(self):
        try:
            url = self.request.arguments['link'][0].decode()
        except Exception as e:
            url = self.request.arguments['link'][0].decode('gbk')
        finally:
            #print(url)
            client = tornado.httpclient.AsyncHTTPClient()
            response = await client.fetch(url)
            # print(response.body)
            self.write(response.body)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/getData", IndexHandler),
            (r"/htmlParser", GetHtmlStr)
        ],
        debug=True,

    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
