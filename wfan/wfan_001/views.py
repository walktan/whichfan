from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from wfan_001.models import twitDra,twitSwa,twitGia,twitTig,twitCar,twitBay
import MySQLdb
from requests_oauthlib import OAuth1Session
import json

### Constants
oath_key_dict = {
    "consumer_key": "hD5R5jSasiJ40oVenvN0NvnOh",
    "consumer_secret": "LpnOvbof9Cd0UJBc1mgWd3yQnxwQIvBO90ftD78dPtednzMmHc",
    "access_token": "182051631-UjzLI6mbNotb46qz7VJgmQAwign1K9q9GMwG6MVq",
    "access_token_secret": "zdpxnKgL5wmq37ylDQDKbgwB5QX2IMsYTO4vklzjC2vsH"
}

def index(request):
    #中日
    tdra = main('ドラゴンズ')
    dra = twitDra(twit=tdra).save()
    #ヤクルト
    tswa = main('スワローズ')
    swa = twitSwa(twit=tswa).save()
    #巨人
    tgia = main('ジャイアンツ')
    gia = twitGia(twit=tgia).save()
    #阪神
    ttig = main('タイガース')
    tig = twitTig(twit=ttig).save()
    #広島
    tcar = main('カープ')
    car = twitCar(twit=tcar).save()
    #横浜
    tbay = main('ベイスターズ')
    bay = twitBay(twit=tbay).save()
    return HttpResponse("Hello, world.")

def main(key):
    tweets = tweet_search(key, oath_key_dict)
    for tweet in tweets["statuses"]:
        text = tweet[u'text']
        return text

def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
    oath_key_dict["consumer_key"],
    oath_key_dict["consumer_secret"],
    oath_key_dict["access_token"],
    oath_key_dict["access_token_secret"]
    )
    return oath

def tweet_search(search_word, oath_key_dict):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    params = {
        "q": search_word,
        "lang": "ja",
        "result_type": "recent",
        "count": "10"
        }
    oath = create_oath_session(oath_key_dict)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
   #     print "Error code: %d" %(responce.status_code)
        return None
    tweets = json.loads(responce.text)
    return tweets