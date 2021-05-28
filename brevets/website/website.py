from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    render_template('index.html')


@app.route('/listeverything')
def listeverything():
    r = requests.get('http://restapi:5000/listAll')
    return r.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
