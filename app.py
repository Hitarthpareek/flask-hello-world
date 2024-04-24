from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def process_string():
    to_send = {}
    # inputchr = str(request.args['query'])
    # answer = str(ord(inputchr))
    # to_send['output']=answer
    # return to_send
 #   Get the string from the request data
    input_string = str(request.args['query'])

    # Check if input_string is provided
    if input_string is None:
        return jsonify({'error': 'No input string provided'}), 400


    # import requests
# import json
# payload = { 'api_key': '8bbf28f5b1375db41ce4b2c6d8c93213', 'query': 'how to make tea', 'country_code': 'in' }
# r = requests.get('https://api.scraperapi.com/structured/google/search', params=payload)

    json_data = '''
    {
        "search_information": {
            "query_displayed": "election"
        },
        "organic_results": [
        {
            "position": 0,
            "title": "eci. gov. in",
            "link": "https://eci.gov.in/",
            "displayed_link": "https://eci.gov.in",
            "sitelinks": {
                "inline": [
                    {
                        "title": "More results from eci.gov.in »",
                        "link": "https://www.google.co.in/searchq=election+site:eci.gov.in&sca_esv=ddd81285843a68ee&sca_upv=1&gl=IN&sa=X&ved=2ahUKEwi5sv6VnNqFAxUKm4kEHf-OCuIQrAN6BAgbEAE"
                    }
                ]
            }
        },
        {
            "position": 1,
            "title": "eci. gov. in",
            "link": "https://eci.gov.in/",
            "displayed_link": "https://eci.gov.in"
        },
        {
            "position": 2,
            "title": "Chief Electoral Officer, Maharashtra",
            "snippet": "CEO Maharashtra मुख्य निवडणूक अधिकारी, महाराष्ट्र राज्य Chief Electoral Officer, Maharashtra.",
            "link": "https://ceo.maharashtra.gov.in/",
            "displayed_link": "https://ceo.maharashtra.gov.in"
        },
        {
            "position": 7,
            "title": "Election Commission of India (@ECISVEEP) · X",
            "link": "https://twitter.com/ECISVEEP?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor",
            "displayed_link": "https://twitter.com/ECISVEEP"
        },
        {
            "position": 8,
            "title": "Lok Sabha Election 2024 Live Updates: BJP govt controlled ...",
            "snippet": "25 minutes ago — Lok Sabha Election 2024 Live Updates: PM Narendra Modi is all set to address the election rally today in Chhattisgarh and Madhya Pradesh.",
            "highlighs": ["Election", "election"],
            "link": "https://timesofindia.indiatimes.com/india/lok-sabha-election-2024-live-updates-pm-narendra-modi-rahul-gandhi-bjp-congress-india-general-elections-2024/liveblog/109511029.cms",
            "displayed_link": "https://timesofindia.indiatimes.com › India News"
        },
        {
            "position": 9,
            "title": "Lok Sabha elections 2024 updates",
            "snippet": "18 hours ago — Election 2024, April 23 Key highlights: 1. 1351 candidates in fray for phase 3 of Lok Sabha polls: EC.",
            "highlighs": ["Election"],
            "link": "https://www.thehindu.com/elections/lok-sabha/lok-sabha-elections-2024-live-updates-april-23/article68095342.ece",
            "displayed_link": "https://www.thehindu.com › ... › Lok Sabha Elections"
        }
    ]
}
'''

    data = json.loads(json_data)
#data = json.loads(r.text)
# Extract organic results
    organic_results = data["organic_results"]

# Extract relevant fields from organic results
    extracted_results = []
    for result in organic_results:
        extracted_result = {
            "title": result["title"],
            "link": result["link"],
            "snippet": result.get("snippet", "nosnip")  # If snippet is not available, put "nosnip"
        }
        extracted_results.append(extracted_result)
   
   # extracted_results_json = json.dumps(extracted_results, indent=4)
    return extracted_results

if __name__ == '__main__':
    app.run()
