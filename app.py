import datetime
import json
import requests
from flask import Flask, render_template, jsonify, request
import requests
import pandas as pd

app = Flask(__name__, static_url_path='/static')

query_url = 'http://stuinfo.ntust.edu.tw/classroom_user/classroom_usecondition.aspx'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/ajax', methods=['POST'])
def ajax():
    recv_json = json.loads(request.data)
    cookies = {
        '_ga': 'GA1.3.2114523626.1653109984',
        'ntustLan': 'zh-TW',
        '_gid': 'GA1.3.779935963.1659412891',
        '_gat_gtag_UA_134331597_1': '1',
    }

    headers = {
        'authority': 'querycourse.ntust.edu.tw',
        'accept': '*/*',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json; charset=utf-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_ga=GA1.3.2114523626.1653109984; ntustLan=zh-TW; _gid=GA1.3.779935963.1659412891; _gat_gtag_UA_134331597_1=1',
        'origin': 'https://querycourse.ntust.edu.tw',
        'referer': 'https://querycourse.ntust.edu.tw/querycourse/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
    }
    
    json_data = {
        'Semester': '1111',
        'CourseNo': recv_json['CourseNo'],
        'CourseName': recv_json['CourseName'],
        'CourseTeacher': '',
        'Dimension': '',
        'CourseNotes': '',
        'ForeignLanguage': recv_json['ForeignLanguage'],
        'OnlyGeneral': recv_json['OnlyGeneral'],
        'OnleyNTUST': recv_json['OnleyNTUST'],
        'OnlyMaster': recv_json['OnlyMaster'],
        'Language': 'zh',
    }

    response = requests.post('https://querycourse.ntust.edu.tw/querycourse/api/courses', cookies=cookies, headers=headers, json=json_data)
    print(response.status_code)
    df = pd.json_normalize(response.json())
    df.loc[:, 'Restrict1'] = df.Restrict1.astype('int')
    df.loc[:, 'Rate'] =   df.Restrict1 / df.ChooseStudent
    df = df[df.ChooseStudent < df.Restrict1]
    df = df.sort_values(by=['Rate', 'ChooseStudent'])
    js = df.to_json(orient = 'records')
    return js


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
