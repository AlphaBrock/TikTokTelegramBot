# -*- coding=utf-8 -*-
import requests
import re
import random
import json

import config

logger = config.setup_log()


def getShareVideoUrl(shareInfo):
    shareVideoUrl = re.compile(r'https://[a-zA-Z0-9/.]+').search(shareInfo)
    if shareVideoUrl is None:
        logger.error("获取视频分享链接失败")
        return None
    else:
        logger.info("获取视频分享链接成功:{}".format(shareVideoUrl.group(0)))
        return shareVideoUrl.group(0)


def getVideoID(shareUrl):
    headers = {
        "User-Agent": "{}".format(random.choice(config.UserAgent))
    }
    response = requests.request("GET", shareUrl, headers=headers)
    if response.status_code == 200:
        trueUrl = re.compile(r'video/(\d+)').search(response.url)
        if trueUrl is None:
            logger.error("获取到视频ID失败")
            return None
        else:
            logger.info("获取到视频ID:{}".format(trueUrl.group(1)))
            return trueUrl.group(1)
    else:
        logger.error("解析真实URL链接失败，返回结果:{}".format(response.text))
        return None


def getVideoInfo(videoID):
    url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + str(videoID)
    headers = {
        "User-Agent": "{}".format(random.choice(config.UserAgent))
    }
    response = requests.request("GET", url, headers=headers)
    text = json.loads(response.text)
    try:
        title = text["item_list"][0]["desc"]
        wm_url = text["item_list"][0]["video"]["play_addr"]["url_list"][0].replace('playwm', 'play')
        mp3_url = text["item_list"][0]["music"]["play_url"]["uri"]
        photo_url = text["item_list"][0]["video"]["origin_cover"]["url_list"][0]
        logger.info("获取视频连接成功，视频ID:{}，标题:{}，视频链接:{}，MP3链接:{}，图片链接:{}".format(videoID, title, wm_url, mp3_url, photo_url))
        return [title, wm_url, mp3_url, photo_url]
    except Exception as e:
        logger.exception("获取视频连接失败，视频ID:{}，抛出异常:{}".format(videoID, e))
        return None


if __name__ == '__main__':
    shareInfo = "每次听到这首歌里的口哨 就会想起太阳的后裔里的场景 #音乐分享 #kwill #神曲 #韩剧ost  https://v.douyin.com/JrAbnd7/ 复制此链接，打开【抖音短视频】，直接观看视频！"
    url = getShareVideoUrl(shareInfo)
    videoID = getVideoID(url)
    getVideoInfo(videoID)
