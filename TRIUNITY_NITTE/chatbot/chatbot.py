from flask import Flask, render_template, request
import google.generativeai as genai

# Replace with your actual API key (store securely)
api_key = "YOUR_API_KEY"

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
from flask import Flask, render_template, request
import google.generativeai as genai

# Replace with your actual API key (store securely)
api_key = "AIzaSyA6LLyc0EMItY8dyjIx2YpdJwXajxogUVU"

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    
    system_instruction="You are a Indian railway information dissiminator. Your job is to answer user queries related to stations. They will be giving you station or city names of source and destination. You have to give them all the avaailable trains, arrival and departure time, and the distance in sentences. Answer any questions related to Indian Railways. Give the user direct answers. Do not ask them to lookup other websites. Keep the answer to the point",
)

chat_session = model.start_chat(history=[])

app = Flask(__name__)

def preprocess_text(text):
    # Remove newlines and extra spaces
    return text.replace('\n', ' ').replace('  ', ' ')

def preprocess_chat_history(chat_history):
    # Preprocess chat history to remove newline characters
    for message in chat_history:
        if 'parts' in message:
            for part in message['parts']:
                if 'text' in part:
                    part['text'] = preprocess_text(part['text'])
    return chat_history

@app.route("/")
def home():
    # chat_history = chat_session.history
    chat_history = preprocess_chat_history(chat_session.history)
    return render_template("indexchatbot.html", chatbot_history=chat_history)


@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.form["message"]
    chat_session.send_message(user_message)

    # Ensure the response handling is robust and check the structure of history
    try:
        response_content = chat_session.history[-1]["parts"][0]
        response = response_content.get("text", "") if isinstance(response_content, dict) else response_content
    except (IndexError, KeyError, TypeError) as e:
        response = "Error processing response: " + str(e)

    # Remove newlines from the response
    response = response.replace('\n', ' ')


    return render_template("indexchatbot.html", message=user_message, response=response, chatbot_history=chat_session.history)

if __name__ == "__main__":
    app.run(port=5001)

