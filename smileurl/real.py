# flask 모듈 임포트
from flask import Flask, render_template, request, redirect, url_for
import change

# flask 객체 생성
app = Flask(__name__)


@app.route('/')
def index():
    url_rank = change.get_url_rank()
    return render_template('smilehome.html', url_rank = url_rank)


@app.route('/shorten', methods=['GET', 'POST'])
def change_url():
    input_url = request.args["input"]

    # 여기서 예외처리 필요

    url_converted = change.process_input(input_url)

    return render_template('shorten_url.html', url_converted=url_converted)


@app.route('/https://smi.le/<short_url>')
def connect_url(short_url):
    print(short_url)
    if short_url == "favicon.ico":
        return redirect('/')
    
    return redirect(change.take_url(short_url))


# 앱 실행 항상 마지막
# 웹주소와 포트 지정
# 127.0.0.1:5000
app.run(host='127.0.0.1', port=5000, debug=True)
