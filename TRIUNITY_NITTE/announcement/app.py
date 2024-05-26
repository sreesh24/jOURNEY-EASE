from flask import Flask, render_template, request
import pandas as pd
from googletrans import Translator

app = Flask(__name__)

# Read your CSV file
csv_file_path = 'announcements.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Function to translate text
def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language).text
    return translated_text

# Define routes and views
@app.route('/')
def index():
    # Get unique stations and languages from the DataFrame
    stations = df['Station'].unique().tolist()
    languages = ['Amharic', 'Arabic', 'Basque', 'Bengali', 'English (UK)', 'Portuguese (Brazil)', 'Bulgarian', 
                 'Catalan', 'Cherokee', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English (US)', 'Estonian', 
                 'Filipino', 'Finnish', 'French', 'German', 'Greek', 'Gujarati', 'Hebrew', 'Hindi', 'Hungarian', 
                 'Icelandic', 'Indonesian', 'Italian', 'Japanese', 'Kannada', 'Korean', 'Latvian', 
                 'Lithuanian', 'Malay', 'Malayalam', 'Marathi', 'Norwegian', 'Polish', 
                 'Portuguese (Portugal)', 'Romanian', 'Russian', 'Serbian', 'Chinese (PRC)', 
                 'Slovak', 'Slovenian', 'Spanish', 'Swahili', 'Swedish', 'Tamil', 'Telugu', 
                 'Thai', 'Chinese (Taiwan)', 'Turkish', 'Urdu', 'Ukrainian', 'Vietnamese', 'Welsh'
]  # Add more languages as needed

    return render_template('index.html', stations=stations, languages=languages)

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    # Get user selections from the form
    selected_station = request.form['station']
    selected_language = request.form['language']

    # Filter the DataFrame based on user selections
    filtered_df = df[(df['Station'] == selected_station)]

    # Translate text to the selected language
    filtered_df['TranslatedText'] = filtered_df['Announcement'].apply(lambda x: translate_text(x, selected_language))

    # Display the result
    return render_template('results.html', data=filtered_df.to_html(), selected_station=selected_station, selected_language=selected_language)

if __name__ == '__main__':
    app.run(port=5002)
