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
    insert()
    return HttpResponse("Hello, world.")

def insert():
    tweetsDra = tweet_search('ドラゴンズ', oath_key_dict)
    tweetsSwa = tweet_search('スワローズ', oath_key_dict)
    tweetsGia = tweet_search('ジャイアンツ', oath_key_dict)
    tweetsTig = tweet_search('タイガース', oath_key_dict)
    tweetsCar = tweet_search('カープ', oath_key_dict)
    tweetsBay = tweet_search('ベイスターズ', oath_key_dict)
    for tDra in tweetsDra["statuses"]:
        dra = twitDra(twit=tDra[u'text']).save()
    for tSwa in tweetsSwa["statuses"]:
        swa = twitSwa(twit=tSwa[u'text']).save()
    for tGia in tweetsGia["statuses"]:
        gia = twitGia(twit=tGia[u'text']).save()
    for tTig in tweetsTig["statuses"]:
        tig = twitTig(twit=tTig[u'text']).save()
    for tCar in tweetsCar["statuses"]:
        car = twitCar(twit=tCar[u'text']).save()
    for tBay in tweetsBay["statuses"]:
        bay = twitBay(twit=tBay[u'text']).save()
    return

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