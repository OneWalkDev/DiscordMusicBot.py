# DiscordMusicBot.py

## 概要
[DiscordMusicBot-dotNet](https://github.com/OneWalkDev/DiscordMusicBot-dotNet)の後継です。

Discordの音楽botです。

ボイスチャットにyoutubeの音楽を再生することができます。

/play キーワード | url | playlist url

ループ再生、キューループ再生、シャッフルにも対応しています。

## ビルド 

このbotはオープンソースなので、自分のbotとして動かすこともできます。

## bot運用の仕方

### １，docker環境
Dockerが動く環境ならどこでも使用できます
#### 必要ソフトウェア
 - Docker
#### 詳細
DiscordDevelopperPortalでbotのトークンを取得します。

```bash
cp .env.example .env #.env.exampleをコピーし.envという名前で保存してください
```

.env内の DISCORD_TOKEN= に取得したトークンを貼り付けます

```bash
cd .devcontainer
docker compose up --build -d #これで起動完了です。
docker compose down #これで終了できます。
```

### 2，ローカル環境
#### 必要ソフトウェア
 - ffmpeg
 - python(pip) 3.12

#### 詳細

[ffmpeg](https://ffmpeg.org/download.html)をあなたの使用しているOSに合わせてダウンロードします。

[python](https://apps.microsoft.com/detail/9ncvdn91xzqp?hl=ja-jp&gl=JP)をダウンロードします。

```bash
cp .env.example .env #.env.exampleをコピーし.envという名前で保存してください

cd src
pip install -r requirements.txt
python DiscordMusicBot2.py
```



