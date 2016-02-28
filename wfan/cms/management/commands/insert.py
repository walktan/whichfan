from django.core.management.base import BaseCommand
import datetime, json
from django.db.models import Max, Min
from cms.models import twitDra, twitSwa, twitGia, twitTig, twitCar, twitBay
from requests_oauthlib import OAuth1Session

#twitter apiを介してDBにツイートを取り込む
#Cronで10分毎に実行し、最新ツイートを取得する
class Command(BaseCommand):
    # Twitter api接続情報
    oath_key_dict = {
        "consumer_key": "hD5R5jSasiJ40oVenvN0NvnOh",
        "consumer_secret": "LpnOvbof9Cd0UJBc1mgWd3yQnxwQIvBO90ftD78dPtednzMmHc",
        "access_token": "182051631-UjzLI6mbNotb46qz7VJgmQAwign1K9q9GMwG6MVq",
        "access_token_secret": "zdpxnKgL5wmq37ylDQDKbgwB5QX2IMsYTO4vklzjC2vsH"
    }

    def handle(self, *args, **options):
        id_Dra = twitDra.objects.aggregate(max=Max('twit_id'))
        tweetsDra = Command.tweet_search('中日ドラゴンズ -rt -bot', id_Dra["max"], self.oath_key_dict)
        id_Swa = twitSwa.objects.aggregate(max=Max('twit_id'))
        tweetsSwa = Command.tweet_search('ヤクルトスワローズ -rt -bot', id_Swa["max"], self.oath_key_dict)
        id_Gia = twitGia.objects.aggregate(max=Max('twit_id'))
        tweetsGia = Command.tweet_search('読売ジャイアンツ -rt -bot', id_Gia["max"], self.oath_key_dict)
        id_Tig = twitTig.objects.aggregate(max=Max('twit_id'))
        tweetsTig = Command.tweet_search('阪神タイガース -rt -bot', id_Tig["max"], self.oath_key_dict)
        id_Car = twitCar.objects.aggregate(max=Max('twit_id'))
        tweetsCar = Command.tweet_search('広島カープ -rt -bot', id_Car["max"], self.oath_key_dict)
        id_Bay = twitBay.objects.aggregate(max=Max('twit_id'))
        tweetsBay = Command.tweet_search('横浜ベイスターズ -rt -bot', id_Bay["max"], self.oath_key_dict)
        for tweet in tweetsDra["statuses"]:
            twit_at = Command.change_ja_time(tweet[u'created_at'])
            twitDra(twit_id=tweet[u'id_str'], twit=tweet[u'text'], twit_at=twit_at).save()

        for tweet in tweetsSwa["statuses"]:
            twit_at = Command.change_ja_time(tweet[u'created_at'])
            twitSwa(twit_id=tweet[u'id_str'], twit=tweet[u'text'], twit_at=twit_at).save()

        for tweet in tweetsGia["statuses"]:
            twit_at = Command.change_ja_time(tweet[u'created_at'])
            twitGia(twit_id=tweet[u'id_str'], twit=tweet[u'text'], twit_at=twit_at).save()

        for tweet in tweetsTig["statuses"]:
            twit_at = Command.change_ja_time(tweet[u'created_at'])
            twitTig(twit_id=tweet[u'id_str'], twit=tweet[u'text'], twit_at=twit_at).save()

        for tweet in tweetsCar["statuses"]:
            twit_at = Command.change_ja_time(tweet[u'created_at'])
            twitCar(twit_id=tweet[u'id_str'], twit=tweet[u'text'], twit_at=twit_at).save()

        for tweet in tweetsBay["statuses"]:
            twit_at = Command.change_ja_time(tweet[u'created_at'])
            twitBay(twit_id=tweet[u'id_str'], twit=tweet[u'text'], twit_at=twit_at).save()
            return

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
