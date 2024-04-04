from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def hello_world():
    input_string = str(request.args['query'])

    # Check if input_string is provided
    if input_string is None:
        return jsonify({'error': 'No input string provided'}), 400

    # Process the string (here, we just return the same string)
    processed_string = input_string

    # Return the processed string as JSON
    return jsonify({'processed_string': processed_string})

if __name__ == "__main__":
    app.run()
