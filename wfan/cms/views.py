from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from cms.models import twitDra,twitSwa,twitGia,twitTig,twitCar,twitBay
from datetime import datetime,timedelta
from django.shortcuts import render
from django.http import HttpResponse,Http404
from collections import OrderedDict
import string,json

#Top画面表示
def index(request):
    return render(request, 'cms/index.html',)

#graph描画用jsonの取得
def get_json(req):
    try:
        if req.POST['frequency'] == 'daily':
            response = for_daily(req)
        else:
            response = for_hourly(req)
    except KeyError:
        response = for_daily(req)
    return HttpResponse(response,content_type="text/javascript")

#hourly用jsonの取得
def for_hourly(req):
    if req.method == 'POST':
        try:
            get_from_time = req.POST['fromTime']
            get_to_time = req.POST['toTime']
            from_time = datetime.strptime(get_from_time, '%Y/%m/%d %H:%M').replace(minute=0, second=0, microsecond=0)
            to_time = datetime.strptime(get_to_time, '%Y/%m/%d %H:%M').replace(minute=0, second=0, microsecond=0)
        #開始、終了時間が未入力の場合、直近の12時間を取得
        except (KeyError,ValueError):
            from_time = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=11)
            to_time = datetime.now().replace(minute=0, second=0, microsecond=0)

        diff_time = int((to_time - from_time).total_seconds() / 3600)
        link_time = []

        for var in range(0,diff_time+1):
            countDra = twitDra.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countSwa = twitSwa.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countGia = twitGia.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countTig = twitTig.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countCar = twitCar.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countBay = twitBay.objects.filter(twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
            countall = (('Swallows',countSwa),('Giants',countGia),('Dragons',countDra),('Carp',countCar),('BayStars',countBay),('Tigers',countTig))
            sort_countall = OrderedDict(countall)
            link_time.append({'Team':from_time.strftime('%-m/%-d %-H:%M'),'twicnt':sort_countall})
            from_time += timedelta(hours=1)

        response = json.dumps(link_time)
        return HttpResponse(response,content_type="text/javascript")
    else:
        raise Http404

#daily用jsonの取得
def for_daily(req):
    if req.method == 'POST':
        try:
            get_from_time = req.POST['fromTime']
            get_to_time = req.POST['toTime']
            from_time = datetime.strptime(get_from_time, '%Y/%m/%d %H:%M').replace(hour=0, minute=0, second=0, microsecond=0)
            to_time = datetime.strptime(get_to_time, '%Y/%m/%d %H:%M').replace(hour=0, minute=0, second=0, microsecond=0)
        #開始、終了時間が未入力の場合、直近の7日間を取得
        except (KeyError,ValueError):
            from_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=6)
            to_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        diff_time = int((to_time - from_time).total_seconds() / (3600 * 24))
        link_time = []

        for var in range(0,diff_time+1):
            countDra = twitDra.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countSwa = twitSwa.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countGia = twitGia.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countTig = twitTig.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countCar = twitCar.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countBay = twitBay.objects.filter(twit_at__range=(from_time, from_time + timedelta(days=1))).count()
            countall = (('Swallows',countSwa),('Giants',countGia),('Dragons',countDra),('Carp',countCar),('BayStars',countBay),('Tigers',countTig))
            sort_countall = OrderedDict(countall)
            link_time.append({'Team':from_time.strftime('%-m/%-d') + string.whitespace,'twicnt':sort_countall})
            from_time += timedelta(days=1)

        response = json.dumps(link_time)
        return HttpResponse(response,content_type="text/javascript")
    else:
        raise Http404