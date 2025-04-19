import json
import boto3
import requests
import os
import urllib.parse
import re
from collections import Counter
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
comprehend = boto3.client('comprehend')
table_name = 'FakeNewsAnalysisResults'
ddb_table = dynamodb.Table(table_name)

# Get S3 bucket name from environment variable
s3_bucket_name = os.environ.get('fakenewsresults', '').strip()
if not s3_bucket_name:
    raise EnvironmentError("Environment variable 'fakenewsresults' is missing.")

def analyze_news(news_text):
    try:
        # Use Amazon Comprehend for sentiment and entity analysis
        sentiment_response = comprehend.detect_sentiment(Text=news_text, LanguageCode='en')
        entity_response = comprehend.detect_entities(Text=news_text, LanguageCode='en')

        sentiment = sentiment_response['Sentiment']
        sentiment_score = max(sentiment_response['SentimentScore'].values())
        entities = entity_response.get('Entities', [])
        entity_count = len(entities)

        # Improved classification logic
        if sentiment == 'POSITIVE' and sentiment_score > 0.8 and entity_count > 2:
            return 'Real', sentiment_score
        elif sentiment == 'NEGATIVE' and sentiment_score > 0.8 and entity_count < 2:
            return 'Fake', sentiment_score
        elif sentiment == 'NEUTRAL' and entity_count >= 2:
            return 'Real', sentiment_score
        else:
            return 'Uncertain', sentiment_score
    except Exception as e:
        print(f"Comprehend Error: {e}")
        return 'Error', 0.0

def extract_keywords(text, max_keywords=10):
    # Remove special characters and split words
    words = re.findall(r'\w+', text.lower())
    common_words = set(['the', 'is', 'and', 'in', 'to', 'a', 'of', 'on', 'for', 'with', 'as', 'at', 'it', 'by', 'this', 'from'])
    filtered_words = [word for word in words if word not in common_words]

    # Get the most common words as keywords
    keywords = [word for word, _ in Counter(filtered_words).most_common(max_keywords)]
    return " ".join(keywords)

def check_fact_external_api(news_text):
    try:
        api_key = '91e36392ffd8b26083d26252074eeb37'
        url = 'http://api.mediastack.com/v1/news'

        # Extract keywords from the news text for a concise query
        query_text = extract_keywords(news_text)
        params = {
            'access_key': api_key,
            'keywords': query_text,
            'languages': 'en'
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            articles = response.json().get('data', [])
            return 'Real' if articles else 'Fake'
        else:
            return f'API Error: {response.status_code}, {response.json().get("error", {}).get("message", response.text)}'
    except Exception as e:
        return str(e)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        news_text = body.get('news')
        if not news_text:
            return {'statusCode': 400, 'body': 'Missing news text'}

        analysis_result, confidence_score = analyze_news(news_text)
        external_check_result = check_fact_external_api(news_text)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        news_id = f'news-{timestamp}'

        # Store results in S3
        s3.put_object(
            Bucket=s3_bucket_name,
            Key=f'news-results/{timestamp}.json',
            Body=json.dumps({
                'news_id': news_id,
                'news': news_text,
                'analysis_result': analysis_result,
                'confidence_score': f'{confidence_score * 100:.2f}%',
                'external_check': external_check_result,
                'timestamp': timestamp
            })
        )

        # Store results in DynamoDB
        ddb_table.put_item(
            Item={
                'news_id': news_id,
                'news': news_text,
                'analysis_result': analysis_result,
                'confidence_score': f'{confidence_score * 100:.2f}%',
                'external_check': external_check_result,
                'timestamp': timestamp
            }
        )

        return {'statusCode': 200, 'body': json.dumps({'result': analysis_result, 'confidence_score': f'{confidence_score * 100:.2f}%', 'external_check': external_check_result})}

    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}
