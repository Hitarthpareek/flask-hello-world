app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from git'

if __name__ == "__main__":
    app.run()
