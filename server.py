from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import wikipedia
from flask_cors import cross_origin
from translate import Translator
from dotenv import load_dotenv
# Initialize Flask app
app = Flask(__name__)
CORS(app)
load_dotenv()

api_key = os.getenv('GOOGLE_API')

# Validate the presence of the API key
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY environment variable. Please set it in your .env file.")

# Configure the GenAI library
genai.configure(api_key=api_key)

# Create a Generative Model instance
model = genai.GenerativeModel('gemini-pro')

# Initialize a chat history
history = []

# Start a chat session
chat = model.start_chat(history=history)
def translate_to_english(text, source_language):
    translator = Translator(to_lang="english")
    translated_text = translator.translate(text, src=source_language)
    return translated_text

# Route to receive voice input from the HTML file
@app.route('/gemini', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:5500')
def receive_voice_input():
    data = request.json
    voice_input = data.get('gemini', '')
    # selected_language = data.get('selected_language', 'en')
    response = chat.send_message(voice_input + " (Keep the answer short and to the point and give answer only in english)")
    # response = chat.send_message(voice_input)
    ai_response = response.text
    return jsonify({'ai_response': ai_response})

@app.route('/wiki_summary', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:5500')
def get_wikipedia_summary():
    data = request.json
    search_query = data.get('search_query', '')
    selected_language = data.get('selected_language', 'en')
    if selected_language != 'en':
        search_query = translate_to_english(search_query, selected_language)
    # print(search_query)
    # Fetch the Wikipedia summary for the given search query
    summary = wikipedia.summary(search_query, sentences=3)
    return jsonify({'summary': summary})


@app.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    file_name = data.get('file_name', '')
    note_content = data.get('note_content', '')
    file_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name + ".txt")
    try:
        with open(file_path, 'w') as file:
            file.write(note_content)
        return jsonify({'file_created': file_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#notes
@app.route('/notes', methods=['POST'])
@cross_origin(origin='http://127.0.0.1:5500')
def create_notes():
    data = request.json
    file_name = data.get('file_name', '') + '.txt'  # Append '.txt' extension
    note_content = data.get('note_content', '')

    # Save the note content to a text file
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_dir, file_name)
    with open(file_path, 'w') as file:
        file.write(note_content)

    return jsonify({'status': 'success', 'message': 'Note saved successfully.'})


if __name__ == '__main__':
    app.run(debug=True)









# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import os
# import wikipedia
# from translate import Translator

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)
# # Set the API key from environment variable
# os.environ['GOOGLE_API_KEY'] = 'your_google_api_key_here'

# # Configure the GenAI library
# genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# # Create a Generative Model instance
# model = genai.GenerativeModel('gemini-pro')

# # Initialize a chat history
# history = []

# # Start a chat session
# chat = model.start_chat(history=history)


# # Translate function to translate the input text to English
# def translate_to_english(text, source_language):
#     translator = Translator(to_lang="english")
#     translated_text = translator.translate(text, src=source_language)
#     return translated_text


# # Route to receive voice input from the HTML file
# @app.route('/gemini', methods=['POST'])
# def receive_voice_input():
#     data = request.json
#     voice_input = data.get('gemini', '')
#     selected_language = data.get('selected_language', 'en')
    
#     # Translate to English if the selected language is not English
#     if selected_language != 'en':
#         voice_input = translate_to_english(voice_input, selected_language)
    
#     response = chat.send_message(voice_input + " (Keep the answer short and to the point and give answer only in english)")
#     ai_response = response.text
#     return jsonify({'ai_response': ai_response})

# @app.route('/wiki_summary', methods=['POST'])
# def get_wikipedia_summary():
#     data = request.json
#     search_query = data.get('search_query', '')
#     selected_language = data.get('selected_language', 'en')
    
#     # Translate to English if the selected language is not English
#     if selected_language != 'en':
#         search_query = translate_to_english(search_query, selected_language)
    
#     # Fetch the Wikipedia summary for the given search query
#     summary = wikipedia.summary(search_query, sentences=3)
#     return jsonify({'summary': summary})

# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import os
# import wikipedia
# from flask_cors import cross_origin
# from translate import Translator
# from dotenv import load_dotenv
# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)
# load_dotenv()
# # Set the API key from environment variable

# os.environ['GOOGLE_API_KEY'] = 'api_here'

# # Configure the GenAI library
# genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# # Create a Generative Model instance
# model = genai.GenerativeModel('gemini-pro')

# # Initialize a chat history
# history = []

# # Start a chat session
# chat = model.start_chat(history=history)
# def translate_to_english(text, source_language):
#     translator = Translator(to_lang="english")
#     translated_text = translator.translate(text, src=source_language)
#     return translated_text

# # Route to receive voice input from the HTML file
# @app.route('/gemini', methods=['POST'])
# @cross_origin(origin='http://127.0.0.1:5500')
# def receive_voice_input():
#     data = request.json
#     voice_input = data.get('gemini', '')
#     # selected_language = data.get('selected_language', 'en')
#     response = chat.send_message(voice_input + " (Keep the answer short and to the point and give answer only in english)")
#     # response = chat.send_message(voice_input)
#     ai_response = response.text
#     return jsonify({'ai_response': ai_response})

# @app.route('/wiki_summary', methods=['POST'])
# @cross_origin(origin='http://127.0.0.1:5500')
# def get_wikipedia_summary():
#     data = request.json
#     search_query = data.get('search_query', '')
#     selected_language = data.get('selected_language', 'en')
#     if selected_language != 'en':
#         search_query = translate_to_english(search_query, selected_language)
#     # print(search_query)
#     # Fetch the Wikipedia summary for the given search query
#     summary = wikipedia.summary(search_query, sentences=3)
#     return jsonify({'summary': summary})


# @app.route('/notes', methods=['POST'])
# def create_note():
#     data = request.json
#     file_name = data.get('file_name', '')
#     note_content = data.get('note_content', '')
#     file_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name + ".txt")
#     try:
#         with open(file_path, 'w') as file:
#             file.write(note_content)
#         return jsonify({'file_created': file_path})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# #notes
# @app.route('/notes', methods=['POST'])
# @cross_origin(origin='http://127.0.0.1:5500')
# def create_notes():
#     data = request.json
#     file_name = data.get('file_name', '') + '.txt'  # Append '.txt' extension
#     note_content = data.get('note_content', '')

#     # Save the note content to a text file
#     downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
#     file_path = os.path.join(downloads_dir, file_name)
#     with open(file_path, 'w') as file:
#         file.write(note_content)

#     return jsonify({'status': 'success', 'message': 'Note saved successfully.'})


# if __name__ == '__main__':
#     app.run(debug=True)