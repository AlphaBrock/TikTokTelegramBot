daemon [戳我](https://cdn.jsdelivr.net/gh/AlphaBrock/md_img/macos/20200821112721.mp4)

## 食用

目前刚学习flask，所以API启动的方式比较low
api目录下uwsgi.ini中涉及到目录的都改成你现在用的目录路径
然后启动api
```
uwsgi -d --ini uwsgi.ini
```

然后config.py文件，TGTOKEN填入token号，日志打印路径也改下`Users/rizhiyi/github/TikTokTelegramBot/log/TikTokTelegramBot.log`

最后启动下机器人
```
python3 main.py
```


