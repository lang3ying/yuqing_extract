# coding=utf-8
from gne import GeneralNewsExtractor
from sanic import Sanic
from sanic.response import json,text
from sanic.views import HTTPMethodView
from gerapy_auto_extractor import is_detail, is_list
import requests

app = Sanic(__name__)
app.config.RESPONSE_TIMEOUT=10
app.config.KEEP_ALIVE=True
app.config.KEEP_ALIVE_TIMEOUT=20


def content_extract(htmlStr, noiseNodeList):
    try:
        extractor = GeneralNewsExtractor()
        result = extractor.extract(htmlStr, noise_node_list=noiseNodeList)
    except Exception as e:
        return e
    else:
        return result


class DataParser(HTTPMethodView):
    async def post(self,request):
        try:
            htmlStr = request.form['content'][0]
            noiseNodeList = request.form['noiseNodeList'] if request.form['noiseNodeList'][0] else []
            # print({'noiseNodeList':noiseNodeList})
        except Exception as e:
            return text(e)
        else:
            if htmlStr:
                result = content_extract(htmlStr,noiseNodeList)
                return json({"data": result})
            return json({"data": None})


    async def get(self,request):
        try:
            link = request.args.get("link")
        except Exception as e:
            return text(e)
        else:
            if link:
                try:
                    response = requests.get(link)
                except Exception as e:
                    return text(e)
                else:
                    return text(response.text)


class ListOrDetail(HTTPMethodView):

    def page_what_is(self, htmlStr:str, url:str):   # 判断页面是详情页 还是 导航页[列表页]
        try:
            is_detailpage = is_detail(htmlStr)
            is_listpage = is_list(htmlStr)
        except Exception as e:
            return text(e)
        else:
            result = None
            if is_detailpage:
                result = {'is': 'detail', 'link': url}
            if is_listpage:
                result = {'is': 'list', 'link': url}
            return result


    async def post(self,request):
        try:
            htmlStr = request.form['content'][0]
            link = request.form['link'][0]
        except Exception as e:
            return text(e)
        else:
            if htmlStr:
                result = self.page_what_is(htmlStr,link)
                return json({"data": result})
            return json({"data": None})


app.add_route(DataParser.as_view(), '/getData')
app.add_route(ListOrDetail.as_view(), '/getResult')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, workers=8)