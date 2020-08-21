# -*- coding=utf-8 -*-
import config
from apps.bot import tgbot
from api import tiktok_api

logger = config.setup_log()

if __name__ == '__main__':
    try:
        tiktok_api.app.run(port=8080, debug=False, threaded=True)
        tgbot.run_bot()
    except Exception as e:
        logger.exception("ops,主程序运行异常了，{}".format(e))