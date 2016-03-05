from django.core.management.base import BaseCommand
import datetime, json,os
from django.db.models import Max, Min
from cms.models import TeamMst,TweetTable
from requests_oauthlib import OAuth1Session

#twitter apiを介してDBにツイートを取り込む
#Cronで10分毎に実行し、最新ツイートを取得する
class Command(BaseCommand):
    # Twitter api接続情報
    oath_key_dict = {
        "consumer_key": os.environ['CONSUMER_KEY'],
        "consumer_secret": os.environ['CONSUMER_SECRET'],
        "access_token": os.environ['ACCESS_TOKEN'],
        "access_token_secret": os.environ['ACCESS_TOKEN_SECRET'],
    }

    def handle(self, *args, **options):
        max_id = TweetTable.objects.aggregate(max=Max('twit_id'))
        for search in TeamMst.objects.values('team_name','search_word'):
            get_tweets = Command.tweet_search(search['search_word'] + ' -rt -bot', max_id["max"], self.oath_key_dict)
            for tweet in get_tweets["statuses"]:
                twit_at = Command.change_ja_time(tweet[u'created_at'])
                TweetTable(twit_id=tweet[u'id_str'], twit=tweet[u'text'], twit_at=twit_at, team_name_id=search['team_name']).save()

    def create_oath_session(oath_key_dict):
        oath = OAuth1Session(
                oath_key_dict["consumer_key"],
                oath_key_dict["consumer_secret"],
                oath_key_dict["access_token"],
                oath_key_dict["access_token_secret"]
        )
        return oath


    def tweet_search(search_word, max_id, oath_key_dict):
        url = "https://api.twitter.com/1.1/search/tweets.json?"
        params = {
            "q": search_word,
            "lang": "ja",
            "result_type": "recent",
            "count": "100",
            "since_id": max_id + 1,
        }
        oath = Command.create_oath_session(oath_key_dict)
        responce = oath.get(url, params=params)
        tweets = json.loads(responce.text)
        return tweets

    def change_ja_time(time):
        t_list = time.split(" ")
        t_cut = " ".join(t_list[:4] + t_list[5:])
        dt = datetime.datetime.strptime(t_cut, "%a %b %d %H:%M:%S %Y")
        dt += datetime.timedelta(hours=9)
        twit_at = dt.strftime("%Y-%m-%d %H:%M:%S")
        return twit_at
