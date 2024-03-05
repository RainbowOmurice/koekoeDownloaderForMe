import requests, time
from bs4 import BeautifulSoup

#URLを打ち込む。オートプレイページのみ対応　単一音声ページも可能ならしたいかもしれない。
url = input("urlを入力してください。")

print("\n処理を開始します。\n")

#気持ちではここでif処理

#オートプレイページのURLでレスポンスを取得し、contentの中身まで取得する。
res = requests.get(url)
bs = BeautifulSoup(res.content, "html.parser")

#投稿者名を保管するための変数。
userName = ""
#対象音声の位置をチェックするためのカウント変数。
count = 1

#負荷対策 3秒待機
time.sleep(3)

#音声のみに切り分けたいので、タイトルが付いているものを対象にする。
for i in bs.select("a[title]"):

    #アイコンと名前の部分にtitle,urlが存在するので、1音声につき2個存在する。そのため、奇数個目は除外する。
    if count % 2 != 0:
        count = count + 1
        continue
    elif count % 2 == 0:
        
        if count == 2:
            userName = i.string

        #デバッグ用　多分残すけど対象音声表示
        print(i)

        #URL部分を対象としてレスポンスを取得する。 = これで単一音声ページが取得できる。
        pageUrl = i['href']
        pageRes = requests.get("https://koe-koe.com/" + pageUrl)

        # 単一音声ページのコンテンツを取得し、mp3のURLを特定する。
        pageBs = BeautifulSoup(pageRes.content, "html.parser")
        mp3url = pageBs.find('source')['src']

        #タイトルも取得する
        titleStr = i['title']
        mp3title = titleStr[1:-4]

        #音声番号の取得
        index = pageUrl.find("=")
        urlNo = pageUrl[index + 1:]

        #負荷対策 3秒待機
        time.sleep(3)

        #mp3のURLのレスポンスを取得して、mp3自体を取得する。
        mp3res = requests.get("https:" + mp3url)
        mp3 = mp3res.content

        # #mp3保存処理
        fileName = userName + "__" + "[" + urlNo + "]" + "__" + mp3title + ".mp3"
        with open(fileName,'wb') as saveFile:
            saveFile.write(mp3)
        saveFile.closed
            
        count = count + 1

    #負荷対策 3秒待機
    time.sleep(3)

print("\n終了しました。")