from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from cms.models import twitDra,twitSwa,twitGia,twitTig,twitCar,twitBay
from cms.models import twiDra,twiSwa,twiGia,twiTig,twiCar,twiBay
from requests_oauthlib import OAuth1Session
import json,string
from datetime import datetime,timedelta
from django.db.models import Max,Min
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.core import serializers
from django.shortcuts import render_to_response
from django.template import RequestContext
from collections import OrderedDict
#import datetime

### Constants
oath_key_dict = {
    "consumer_key": "hD5R5jSasiJ40oVenvN0NvnOh",
    "consumer_secret": "LpnOvbof9Cd0UJBc1mgWd3yQnxwQIvBO90ftD78dPtednzMmHc",
    "access_token": "182051631-UjzLI6mbNotb46qz7VJgmQAwign1K9q9GMwG6MVq",
    "access_token_secret": "zdpxnKgL5wmq37ylDQDKbgwB5QX2IMsYTO4vklzjC2vsH"
}

def index(request):
    #newinsert()
    return render(request, 'cms/index.html',)

def get_json(req):
    try:
        if req.POST['frequency'] == 'dayly':
            response = for_dayly(req)
        else:
            response = for_hourly(req)
    except KeyError:
        response = for_dayly(req)
    return HttpResponse(response,content_type="text/javascript")

def for_hourly(req):    # AJAXに答える関数
    print ("hourly?")
    import json
    from django.http import HttpResponse,Http404

    if req.method == 'POST':
        print ("POST?")
        try:
            get_from_time = req.POST['from_time']
            get_to_time = req.POST['to_time']
            from_time = datetime.strptime(get_from_time, '%Y/%m/%d %H:%M').replace(minute=0, second=0, microsecond=0)
            to_time = datetime.strptime(get_to_time, '%Y/%m/%d %H:%M').replace(minute=0, second=0, microsecond=0)
        except (KeyError,ValueError):
            print ("KeyError?")
            from_time = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=240)
            to_time = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=231)

        print(from_time)
        print(to_time)
        diff_time = int((to_time - from_time).total_seconds() / 3600)
        print(diff_time)

        link_time = []

        for var in range(0,diff_time+1):
            countDra = twitDra.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countSwa = twitSwa.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countGia = twitGia.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countTig = twitTig.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countCar = twitCar.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countBay = twitBay.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countall = (('Swallows',countSwa),('Giants',countGia),('Dragons',countDra),('Carp',countCar),('Baystars',countBay),('Tiggers',countTig))
            sort_countall = OrderedDict(countall)
            link_time.append({'State':from_time.strftime('%-m/%-d %-H:%M'),'freq':sort_countall})
            from_time += timedelta(hours=1)

        print(json.dumps(link_time))
        response = json.dumps(link_time)
        return HttpResponse(response,content_type="text/javascript")

    else:
        raise Http404

def for_dayly(req):    # AJAXに答える関数
    import json
    from django.http import HttpResponse,Http404

    if req.method == 'POST':
        print ("POST?")
        try:
            get_from_time = req.POST['from_time']
            get_to_time = req.POST['to_time']
            from_time = datetime.strptime(get_from_time, '%Y/%m/%d %H:%M').replace(hour=0, minute=0, second=0, microsecond=0)
            to_time = datetime.strptime(get_to_time, '%Y/%m/%d %H:%M').replace(hour=0, minute=0, second=0, microsecond=0)
        except (KeyError,ValueError):
            print ("KeyError?")
            from_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=14)
            to_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=8)

        print(from_time)
        print(to_time)
        diff_time = int((to_time - from_time).total_seconds() / (3600 * 24))
        print(diff_time)

        link_time = []

        for var in range(0,diff_time+1):
            countDra = twitDra.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countSwa = twitSwa.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countGia = twitGia.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countTig = twitTig.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countCar = twitCar.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countBay = twitBay.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countall = (('Swallows',countSwa),('Giants',countGia),('Dragons',countDra),('Carp',countCar),('Baystars',countBay),('Tiggers',countTig))
            sort_countall = OrderedDict(countall)
            link_time.append({'State':from_time.strftime('%-m/%-d') + string.whitespace + string.whitespace,'freq':sort_countall})
            print(from_time)
            from_time += timedelta(days=1)

        print(json.dumps(link_time))
        response = json.dumps(link_time)
        return HttpResponse(response,content_type="text/javascript")

    else:
        raise Http404

def insert():
    id_Dra = twitDra.objects.aggregate(max=Min('twit_id'))
    tweetsDra = tweet_search('中日ドラゴンズ -rt -bot',id_Dra["max"], oath_key_dict)
    id_Swa = twitSwa.objects.aggregate(max=Min('twit_id'))
    tweetsSwa = tweet_search('ヤクルトスワローズ -rt -bot',id_Swa["max"], oath_key_dict)
    id_Gia = twitGia.objects.aggregate(max=Min('twit_id'))
    tweetsGia = tweet_search('読売ジャイアンツ -rt -bot',id_Gia["max"], oath_key_dict)
    id_Tig = twitTig.objects.aggregate(max=Min('twit_id'))
    tweetsTig = tweet_search('阪神タイガース -rt -bot',id_Tig["max"], oath_key_dict)
    id_Car = twitCar.objects.aggregate(max=Min('twit_id'))
    tweetsCar = tweet_search('広島カープ -rt -bot',id_Car["max"], oath_key_dict)
    id_Bay = twitBay.objects.aggregate(max=Min('twit_id'))
    tweetsBay = tweet_search('横浜ベイスターズ -rt -bot',id_Bay["max"], oath_key_dict)
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

def newinsert():
    id_Dra = twiDra.objects.aggregate(max=Min('twit_id'))
    tweetsDra = tweet_search('ドラゴンズ -rt -bot since:2016-02-12',id_Dra["max"], oath_key_dict)
    id_Swa = twiSwa.objects.aggregate(max=Min('twit_id'))
    tweetsSwa = tweet_search('スワローズ -rt -bot since:2016-02-12',id_Swa["max"], oath_key_dict)
    id_Gia = twiGia.objects.aggregate(max=Min('twit_id'))
    tweetsGia = tweet_search('ジャイアンツ -rt -bot since:2016-02-12',id_Gia["max"], oath_key_dict)
    id_Tig = twiTig.objects.aggregate(max=Min('twit_id'))
    tweetsTig = tweet_search('タイガース -rt -bot since:2016-02-12',id_Tig["max"], oath_key_dict)
    id_Car = twiCar.objects.aggregate(max=Min('twit_id'))
    tweetsCar = tweet_search('カープ -rt -bot since:2016-02-12',id_Car["max"], oath_key_dict)
    id_Bay = twiBay.objects.aggregate(max=Min('twit_id'))
    tweetsBay = tweet_search('ベイスターズ -rt -bot since:2016-02-12',id_Bay["max"], oath_key_dict)
    for tweet in tweetsDra["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twiDra(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    for tweet in tweetsSwa["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twiSwa(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    for tweet in tweetsGia["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twiGia(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    for tweet in tweetsTig["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twiTig(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    for tweet in tweetsCar["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twiCar(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
    for tweet in tweetsBay["statuses"]:
        twit_at = change_ja_time(tweet[u'created_at'])
        p = twiBay(twit_id=tweet[u'id_str'],twit=tweet[u'text'],twit_at=twit_at).save()
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
        "count": "100",
        "max_id": max_id - 1,
        }
    oath = create_oath_session(oath_key_dict)
    responce = oath.get(url, params = params)
    tweets = json.loads(responce.text)
    return tweets

def change_ja_time(time):
    t_list = time.split(" ")
    t_cut = " ".join(t_list[:4] + t_list[5:])
    dt = datetime.datetime.strptime(t_cut, "%a %b %d %H:%M:%S %Y")
    dt += datetime.timedelta(hours=9)
    twit_at = dt.strftime("%Y-%m-%d %H:%M:%S")
    return twit_at