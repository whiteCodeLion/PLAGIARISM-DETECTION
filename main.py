from flask import Flask, request, render_template
import spacy
import requests
import json
from difflib import SequenceMatcher

# Load the spaCy model for named entity recognition
nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

def extract_named_entities(text):
    """Extract named entities from the input text"""
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'WORK_OF_ART', 'DATE']:
            entities.append(ent.text)
    return entities

def search_and_scrape(entities):
    """Search and scrape the internet for the named entities and store the information in JSON format"""
    results = []
    for entity in entities:
        url = f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles={entity}'
        response = requests.get(url)
        data = response.json()
        page = data['query']['pages']
        if '-1' not in page:
            result = {'entity': entity, 'content': page[list(page.keys())[0]]['extract']}
            results.append(result)
    with open('data.json', 'w') as f:
        json.dump(results, f)

def check_similarity(original_text, downloaded_text):
    """Check the similarity score between the original document and the downloaded document using SequenceMatcher"""
    similarity = SequenceMatcher(None, original_text, downloaded_text).ratio()
    print(f"Similarity score: {similarity:.2f}")
    return similarity

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    original_text = request.form['text']
    named_entities = extract_named_entities(original_text)
    search_and_scrape(named_entities)

    with open('data.json') as f:
        downloaded_data = json.load(f)

    plagiarism_detected = False
    for item in downloaded_data:
        downloaded_text = item['content']
        similarity = check_similarity(original_text, downloaded_text)
        if similarity <= 0.3:
            print(f"Plagiarism detected! The similarity score is {similarity:.2f}")
            plagiarism_detected = True

    if plagiarism_detected:
        result = "Plagiarism detected! Please check your work and try again."
    else:
        result = "No plagiarism detected. Congratulations!"

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
