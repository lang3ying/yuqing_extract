from gne import GeneralNewsExtractor
from sanic import Sanic
from sanic.response import json,text
from sanic.views import HTTPMethodView
import requests

app = Sanic(__name__)
app.config.RESPONSE_TIMEOUT=10


class DataParser(HTTPMethodView):

    def content_extract(self, htmlStr, noiseNodeList=[]):
        try:
            extractor = GeneralNewsExtractor()
            result = extractor.extract(htmlStr, noise_node_list=noiseNodeList)
        except Exception as e:
            return e
        else:
            return result


    async def post(self,request):
        htmlStr = request.form['content'][0]
        if htmlStr:
            noiseNodeList = request.form['noiseNodeList'] if request.form['noiseNodeList'] else []
            result = self.content_extract(htmlStr,noiseNodeList)
            return json({"data": result})
        return json({"data": None})


    async def get(self,request):
        link = request.args.get("link")
        if link:
            try:
                response = requests.get(link)
            except Exception as e:
                return text(e)
            else:
                return text(response.text)


app.add_route(DataParser.as_view(), '/getData')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, workers=8)
