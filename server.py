import requests
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

HF_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

HUGGINGFACE_API_KEY = "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"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    # Get the text input from the form
    text = request.form['text']

    data = {
        "inputs": text
    }

    response = requests.post(HF_URL, headers=headers, json=data)

    if response.status_code == 200:

        summary = response.json()[0]['summary_text']
        return render_template('index.html', summary=summary, original_text=text)
    else:
        # Handle errors
        error_message = "There was an error with the Hugging Face API request."
        return render_template('index.html', error=error_message)


@app.route('/api/data')
def api_data():
    data = {
        "message": "Welcome to the Flask API!",
        "status": "success"
    }
    return jsonify(data)


@app.route('/<path:filename>')
def serve_static_file(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(debug=True)
