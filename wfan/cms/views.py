from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from cms.models import TeamMst,TweetTable
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
    if req.method == 'POST':
        try:
            if req.POST['frequency'] == 'daily':
                response = for_daily(req)
            else:
                response = for_hourly(req)
        except KeyError:
            response = for_daily(req)
        return HttpResponse(response,content_type="text/javascript")
    else:
        raise Http404

#hourly用jsonの取得
def for_hourly(req):
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
        countAll = []

        #tweet数取得
        for var in range(0,diff_time+1):
            for team in TeamMst.objects.values('team_name').order_by('team_id'):
                countTweet = TweetTable.objects.filter(team_name_id=team['team_name'],twit_at__range=(from_time, from_time + timedelta(hours=1))).count()
                countAll.append((team['team_name'], countTweet))
            sort_countall = OrderedDict(countAll)
            link_time.append({'twiDate':from_time.strftime('%-m/%-d %-H:%M'),'twicnt':sort_countall})
            from_time += timedelta(hours=1)

        response = json.dumps(link_time)
        return HttpResponse(response,content_type="text/javascript")


#daily用jsonの取得
def for_daily(req):
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
        countAll = []

        #tweet数取得
        for var in range(0,diff_time+1):
            for team in TeamMst.objects.values('team_name').order_by('team_id'):
                countTweet = TweetTable.objects.filter(team_name_id=team['team_name'],twit_at__range=(from_time, from_time + timedelta(days=1))).count()
                countAll.append((team['team_name'],countTweet))
            sort_countall = OrderedDict(countAll)
            link_time.append({'twiDate':from_time.strftime('%-m/%-d') + string.whitespace,'twicnt':sort_countall})
            from_time += timedelta(days=1)

        response = json.dumps(link_time)
        return HttpResponse(response,content_type="text/javascript")