# -*- coding=utf-8 -*-

import telebot
import requests
import json

import config
from apps.tiktok import tiktok

bot = telebot.TeleBot(config.TGTOKEN)
logger = config.setup_log()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, '欢迎使用，这是一个获取抖音无水印视频的机器人\n'
                                      '你只需要将抖音分享链接发给我就行了，我会帮你提取出无水印视频链接')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "你只需要将抖音分享链接发给我就行了，我会帮你提取出无水印视频链接")


@bot.message_handler(func=lambda m: True)
def talk_with_user(message):
    """
    此处用于无水印的抖音视频
    :param message:
    :return:
    """
    logger.info("获取到用户:{}，输入数据:{}".format(message.chat.id, message.text))
    shareUrl = tiktok.getShareVideoUrl(message.text)
    if shareUrl is None:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "客官，从你提供的分享链接中未找到URL，你确定这是抖音视频分享吗")
    else:
        apiUrl = "http://127.0.0.1:8080/api/v1/dy"
        apiParams = {
            "url": "{}".format(shareUrl)
        }
        response = requests.request("GET", apiUrl, params=apiParams)
        text = json.loads(response.text)
        if text['code'] != 0:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, "Ops,没找到视频信息")
        else:
            logger.info("接口返回结果:{}".format(response.text))
            photo_url = text['tiktok_info'].get('photo_url')
            wm_url = text['tiktok_info'].get('wm_url')
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_photo(message.chat.id, photo=photo_url)
            bot.send_message(message.chat.id, wm_url)


def run_bot():
    bot.polling(none_stop=True, timeout=600)


if __name__ == '__main__':
    run_bot()