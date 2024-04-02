from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def echo_string():
    if request.method == 'POST':
        input_string = request.form.get('input_string')
        return input_string
    else:
        return 'Invalid request method'

if __name__ == '__main__':
    app.run(debug=True)
