from flask import Flask, request, render_template_string


import os

app = Flask(__name__)


def get_source(question):
    """
    response = RetrievalData.query_response(question)
    source = response.sources
"""
    return f"The Source: {question}"


def process_question(question):
    """
    response = RetrievalData.query_response(question)
    answer = response.response_text

    """

    return f"Response to your question: {question} "


def upload_directory(directory_path):
    """
    pdf_docs1 = load_documents(directory_path)
    text_chunks = split_documents(pdf_docs1)
    uploaded_docs = add_to_chroma(text_chunks)
    uploaded_files = []
    """
    return f"Uploaded files: {directory_path}"


@app.route("/", methods=["GET", "POST"])
def index():
    upload_response = ""
    question_response = ""
    source_response = ""

    if request.method == "POST":
        if 'directory_path' in request.form:
            directory_path = request.form.get("directory_path")
            if directory_path:
                upload_response = upload_directory(directory_path)

        if 'question' in request.form:
            question = request.form.get("question")
            if question:
                question_response = process_question(question)
                source_response = get_source(question)

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Directory Upload and Question Processing</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    margin: 0;
                    padding: 20px;
                }
        
                h2 {
                    color: #333;
                }
        
                form {
                    margin-bottom: 20px;
                    padding: 20px;
                    background-color: #fff;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
        
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: bold;
                }
        
                input[type="text"],
                textarea {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                }
        
                button {
                    display: inline-block;
                    padding: 10px 20px;
                    color: #fff;
                    background-color: #007bff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    text-align: center;
                    font-size: 16px;
                }
        
                button:hover {
                    background-color: #0056b3;
                }
        
                .output {
                    margin-top: 20px;
                }
        
                .json-output {
                    white-space: pre-wrap;
                    font-family: monospace;
                    background-color: #f4f4f4;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    margin-top: 10px;
                }
        
                ul {
                    list-style-type: none;
                    padding: 0;
                }
        
                ul li {
                    background-color: #e9ecef;
                    margin: 5px 0;
                    padding: 10px;
                    border-radius: 4px;
                }
            </style>
        </head>
        
        <body>
            <h2>Upload Files from Directory</h2>
            <form method="POST" action="/">
                <label for="directory_path">Enter directory path:</label>
                <input type="text" name="directory_path" id="directory_path" required>
                <button type="submit">Upload</button>
            </form>
        
            {% if upload_response %}
            <h3>Uploaded Files:</h3>
            <ul>
                <div class="json-output">
                    {{ upload_response | tojson(indent=4) | safe }}
                 </div>
            </ul>
            {% endif %}
            <div class="output">{{ get_flashed_messages() }}</div>
        
            <h2>Ask a Question</h2>
            <form method="POST" action="/">
                <label for="question">Enter your question:</label>
                <textarea id="question" name="question" rows="4" required></textarea>
                <button type="submit">Get Answer</button>
            </form>
        
            {% if question_response %}
            <h3>Answer:</h3>
            <div class="json-output">
                {{ question_response | tojson(indent=4) | safe }}
            </div>
            {% endif %}
        
            {% if source_response %}
            <h3>Source:</h3>
            <div class="json-output">
                {{ source_response | tojson(indent=4) | safe }}
            </div>
            {% endif %}
        </body>
        
        </html>
    ''', upload_response=upload_response, question_response=question_response, source_response=source_response)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
