# whichfan

・ 2016/2/26

##■プログラム概要
    プロ野球セリーグ6球団の関連tweet数を可視化するwebアプリケーション
        - 公開URL : http://whichfan-dev.elasticbeanstalk.com/cms/
        - フレームワーク : Django 1.9
        - データベース : MySQL 5.6
        - サーバ : Amazon Linux 2015.09
        - 言語 : Python 3.4 JavaScript
        - JSライブラリ : jQuery v1.12.0, jQuery UI - v1.11.4, D3.js v3

##■機能概要
    ・バックエンド
    　　- Twitter API を使用し、Cronで10分毎にツイートを取得してDBに格納する
    　        (/wfan/cms/management/command.insert.pyをcall)
    ・ フロントエンド
    　　- 開始時間、終了時間、時間単位をインプットとし、単位時間毎のtweet数グラフ化する
    　　- 棒グラフ および 円グラフをマウスオーバすると、各グラフが連動する
  
##■課題、展望
    ・Twitterの検索ワードが球団名のみとなっており、ツイート取得のカバー率が低い
    　　-> 機械学習を用いてテキスト分類の精度を上げる
    ・ tweet数から各試合の盛り上がりを観測したい
    　　-> tweet数を球団間のマトリックス表にし、盛り上がっている（tweet数が上昇している）
    　　    組合を観測できるヒープチャートを作成する
    　　    ※どこのファン（Which fan）が盛り上がっているか可視化できるように...
