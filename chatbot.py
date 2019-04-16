from flask import Flask, render_template
from flask import request, Response
from json import dumps
from LEGAL_LSI import *

text = TextProcessing()

app = Flask(__name__)
app.config['debug'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_message/', methods = ['GET','POST'])
def get_message():

    input_msg = request.get_json(silent = True)
    print(input_msg)

    for col, vals in input_msg.items():
        if col == "MESSAGE":
            input = vals

    output= text.Main(input)

    print(output)

    return Response(response = dumps(output, ensure_ascii = False, allow_nan = True),
                    status = 200,
                    mimetype = 'application/json')


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8000)
