from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)


def fetch_html(link):
    try:
        response = requests.get(link)
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            return response.text  # Return HTML content
        else:
            print(f"Failed to fetch HTML from {link}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching HTML from {link}: {e}")
        return None

def extract_body(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Find and extract <p> tag contents
    p_tags = soup.find_all('p')
    if p_tags:
        paragraphs = []
        for p in p_tags:
            # Extract text from <p> tag and clean it
            text = re.sub(r'\s+', ' ', p.get_text(strip=True))
            # Split text into sentences
            sentences = nltk.sent_tokenize(text)
            # Append each sentence to the paragraphs list
            paragraphs.extend(sentences)
        # Join paragraphs and replace consecutive spaces with a single space
        return ' '.join(paragraphs)
    else:
        return None


def summarize_text(input_text, num_sentences=2):
    # Step 1: Tokenize sentences
    sentences = sent_tokenize(input_text)

    # Step 2: Remove stop words, URLs, and hashtags
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(input_text.lower())
    filtered_words = [word for word in words if word not in stop_words and not re.match(r"(https?://\S+)|(#\S+)", word)]

    # Step 3: Create a frequency table of words
    freq_table = {}
    for word in filtered_words:
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1

    # Step 4: Assign scores to sentences based on word frequency
    sentence_scores = {}
    for sentence in sentences:
        if len(word_tokenize(sentence)) >= 15:  # Check if sentence has at least 15 words
            for word, freq in freq_table.items():
                if word in sentence.lower():
                    if sentence in sentence_scores:
                        sentence_scores[sentence] += freq
                    else:
                        sentence_scores[sentence] = freq

    # Get the top N sentences with highest scores
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    summary_sentences = [sentence for sentence, _ in sorted_sentences[:num_sentences]]

    return " ".join(summary_sentences)




@app.route('/api', methods=['GET'])
def process_string():

    input_string = str(request.args['query'])

    # Check if input_string is provided
    if input_string is None:
        return jsonify({'error': 'No input string provided'}), 400


    api_key = "660a65e32a73df400f66e17f"
    url = "https://api.scrapingdog.com/google/"
    params = {
        "api_key": api_key,
        "query": input_string,
        "results": 10,
        "country": "in",
        "page": 0
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")


    links = [item['link'] for item in data['organic_data']]


    p_contents = []
    for link in links:
        html = fetch_html(link)
        if html:
            p_content = extract_body(html)
            p_contents.append(p_content)

#handling none values
    p_contents = [p_content for p_content in p_contents if p_content is not None]


    final_summary = []

    for content in p_contents:
        input_text = content
        summary = summarize_text(input_text)
        if summary != '':
        # Truncate summary to 200 words
            summary = ' '.join(summary.split()[:80])
            final_summary.append(summary)


  #  summary_dict = {i: ' '.join(summary.split()[:200]) for i, summary in enumerate(final_summary)}


    return final_summary

if __name__ == "__main__":
    app.run()
