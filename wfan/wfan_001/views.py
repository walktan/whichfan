from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from wfan_001.models import twitDra,twitSwa,twitGia,twitTig,twitCar,twitBay
from requests_oauthlib import OAuth1Session
import json,datetime
from django.db.models import Max

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
    id_Dra = twitDra.objects.aggregate(max=Max('twit_id'))
    tweetsDra = tweet_search('ドラゴンズ -rt -bot',id_Dra["max"], oath_key_dict)
    id_Swa = twitSwa.objects.aggregate(max=Max('twit_id'))
    tweetsSwa = tweet_search('スワローズ -rt -bot',id_Swa["max"], oath_key_dict)
    id_Gia = twitGia.objects.aggregate(max=Max('twit_id'))
    tweetsGia = tweet_search('ジャイアンツ -rt -bot',id_Gia["max"], oath_key_dict)
    id_Tig = twitTig.objects.aggregate(max=Max('twit_id'))
    tweetsTig = tweet_search('タイガース -rt -bot',id_Tig["max"], oath_key_dict)
    id_Car = twitCar.objects.aggregate(max=Max('twit_id'))
    tweetsCar = tweet_search('カープ -rt -bot',id_Car["max"], oath_key_dict)
    id_Bay = twitBay.objects.aggregate(max=Max('twit_id'))
    tweetsBay = tweet_search('ベイスターズ -rt -bot',id_Bay["max"], oath_key_dict)
    for tweet in tweetsDra["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twitDra(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    for tweet in tweetsSwa["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twitSwa(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    for tweet in tweetsGia["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twitGia(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    for tweet in tweetsTig["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twitTig(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    for tweet in tweetsCar["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twitCar(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    for tweet in tweetsBay["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twitBay(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    return


def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
    oath_key_dict["consumer_key"],
    oath_key_dict["consumer_secret"],
    oath_key_dict["access_token"],
    oath_key_dict["access_token_secret"]
    )
    return oath

def tweet_search(search_word,max_id,oath_key_dict):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    params = {
        "q": search_word,
        "lang": "ja",
        "result_type": "recent",
        "count": "10",
        "since_id": max_id
        }
    oath = create_oath_session(oath_key_dict)
    responce = oath.get(url, params = params)
    tweets = json.loads(responce.text)
    return tweets

def change_ja_time(time):
    t_list = time.split(" ")
    t_cut = " ".join(t_list[:4] + t_list[5:])
    dt = datetime.datetime.strptime(t_cut, "%a %b %d %H:%M:%S %Y")
    dt += datetime.timedelta(hours=18)
    twit_at = dt.strftime("%Y-%m-%d %H:%M:%S")
    return twit_at