from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from cms.models import twitDra,twitSwa,twitGia,twitTig,twitCar,twitBay
import json,string
from datetime import datetime,timedelta
from django.shortcuts import render
from django.http import HttpResponse,Http404
from collections import OrderedDict

### Constants
oath_key_dict = {
    "consumer_key": "hD5R5jSasiJ40oVenvN0NvnOh",
    "consumer_secret": "LpnOvbof9Cd0UJBc1mgWd3yQnxwQIvBO90ftD78dPtednzMmHc",
    "access_token": "182051631-UjzLI6mbNotb46qz7VJgmQAwign1K9q9GMwG6MVq",
    "access_token_secret": "zdpxnKgL5wmq37ylDQDKbgwB5QX2IMsYTO4vklzjC2vsH"
}

def index(request):
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
            from_time = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=11)
            to_time = datetime.now().replace(minute=0, second=0, microsecond=0)

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
            from_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=11)
            to_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

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