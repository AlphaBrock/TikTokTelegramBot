#!flask/bin/python
import sys

sys.path.append('../')
from apps.tiktok import tiktok
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


@app.route('/api/v1/dy', methods=['GET'])
def getVideoURL():
    return_dict = {
        "code": 0,
        "display_message": "",
        "tiktok_info": {
            "title": "",
            "wm_url": "",
            "mp3_url": "",
            "photo_url": ""
        }
    }
    data = request.args.to_dict()
    if 'url' not in data:
        return_dict['code'] = 1
        return_dict['display_message'] = "缺少url参数"
        response = make_response(jsonify(return_dict), 200)
        return response

    videoID = tiktok.getVideoID(data.get('url'))
    if videoID is None:
        return_dict['code'] = 2
        return_dict['display_message'] = "获取视频ID出错"
        response = make_response(jsonify(return_dict), 200)
        return response
    else:
        videoInfo = tiktok.getVideoInfo(videoID)
        if videoInfo is None:
            return_dict['code'] = 3
            return_dict['display_message'] = "获取视频URL出错"
            response = make_response(jsonify(return_dict), 200)
            return response
        else:
            return_dict['display_message'] = "获取数据成功"
            return_dict['tiktok_info']['title'] = videoInfo[0]
            return_dict['tiktok_info']['wm_url'] = videoInfo[1]
            return_dict['tiktok_info']['mp3_url'] = videoInfo[2]
            return_dict['tiktok_info']['photo_url'] = videoInfo[3]
            response = make_response(jsonify(return_dict), 200)
            return response


if __name__ == '__main__':
    app.run(port=8080, debug=True, threaded=True)
