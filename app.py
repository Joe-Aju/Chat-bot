from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if request.method == "POST":
        data = request.json
        question = data.get("message", "")
        try:
            # OpenAI Chat Response
            client = openai.AzureOpenAI(
                api_key=AZURE_OPENAI_KEY,
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_version=AZURE_API_VERSION
            )

            response = client.chat.completions.create(
                model=AZURE_DEPLOYMENT_NAME,
                messages=[{"role": "user", "content": question}],
                temperature=0.7
            )
            answer = response.choices[0].message.content
            return jsonify({"response": answer})
        except Exception as e:
            return jsonify({"response": f"Error: {str(e)}"}), 500
    else:
        return jsonify({"response": "Method not allowed"}), 405


if __name__ == "__main__":
    # Run on port 80 to work with Azure App Service
    app.run(debug=True, host="0.0.0.0", port=80)
