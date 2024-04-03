from flask import Flask
app = Flask(__name__)

@app.route('/get')
def hello_world():
    input_string = request.json.get('input_string')

    # Check if input_string is provided
    if input_string is None:
        return jsonify({'error': 'No input string povided'}), 400

    # Process the string (here, we just return the same string)
    processed_string = input_string

    # Return the processed string as JSON
    return jsonify({'processed_string': processed_string})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
