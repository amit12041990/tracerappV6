import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
import neattext.functions as ntf
from sklearn.pipeline import Pipeline

class Scraper:
    def __init__(self):
        self.keywords = []
        self.emotion_model, self.tfidf_model = self.train_emotion_model('static/dataset/emotion.csv')
        self.tonality_model = self.train_tonality_model('static/dataset/tonality.csv')

    async def analyze_tonality(self, text):
        prediction = self.tonality_model.predict([text])
        return prediction

    async def analyze_emotion(self, text):
        user_input_tfidf = self.tfidf_model.transform([text])
        prediction = self.emotion_model.predict(user_input_tfidf)
        return self.emo_ji(prediction[0])

    async def scrape_comment_url(self, urls):
        for i in urls:
            if 'form_url' in i and bool(i['comment']):
                comment = []
                user_input = str(i['comment'])
                print(user_input)
                ton = await self.analyze_tonality(user_input)
                emo = await self.analyze_emotion(user_input)
                print("Emotion:", emo)
                print("Tonality:", ton)
                comment.append({
                    'date': i['date'],
                    'title': i['title'],
                    'url': i['form_url'],
                    'comment': i['comment'],
                    'tonality': ton[0],
                    'emotion': emo
                })

                r = await self.fetch_url(i['form_url'])
                if r is not None:
                    keywords = self.extract_keywords_from_html(r.content, comment)
                    self.keywords.extend(keywords)


    async def scrape_video_url(self, urls):
        for i in urls:
            r = await self.fetch_url(i['url'])
            if r is not None:
                keywords = self.extract_keywords_from_html(r.content, [], i['sec'], video_url=i['url'])
                self.keywords.extend(keywords)

    async def scrape_urls(self, urls):
        for i in urls:
            r = await self.fetch_url(i['url'])
            if r is not None:
                keywords = self.extract_keywords_from_html(r.content, [], i['sec'])
                self.keywords.extend(keywords)

    async def fetch_url(self, url):
        try:
            r = await self.async_request(url)
            return r
        except:
            return None

    async def async_request(self, url):
        return requests.get(url)

    def extract_keywords_from_html(self, html_content, comment, sec=None, video_url=None):
        keywords = []
        if html_content is not None:
            soup = BeautifulSoup(html_content, 'html.parser')

            try:
                meta = soup.find("meta", {"name": "keywords"}).attrs['content']
                remove_space = meta.replace(" ", "")
                meta_list = remove_space.split(',')
                for meta_keyword in meta_list:
                    keyword_data = {
                        'keyword': meta_keyword,
                        'pages': 1,
                        'comment': comment,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    if sec is not None:
                        keyword_data['sec'] = sec
                    if video_url is not None:
                        keyword_data['video'] = 1
                        keyword_data['video_url'] = [video_url]
                    keywords.append(keyword_data)
            except AttributeError:
                print('attribute error')
                try:
                    meta = soup.find("meta", {"name": "Keywords"}).attrs['content']
                    remove_space = meta.replace(" ", "")
                    meta_list = remove_space.split(',')
                    for meta_keyword in meta_list:
                        keyword_data = {
                            'keyword': meta_keyword,
                            'pages': 1,
                            'comment': comment,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        if sec is not None:
                            keyword_data['sec'] = sec
                        if video_url is not None:
                            keyword_data['video'] = 1
                            keyword_data['video_url'] = [video_url]
                        keywords.append(keyword_data)
                except:
                    pass
        return keywords

    def train_emotion_model(self, filename):
        df = pd.read_csv(filename)
        df['Clean_Text'] = df['Text'].apply(self.preprocess_text)

        X_features = df['Clean_Text']
        y_labels = df['Emotion']

        x_train, x_test, y_train, y_test = train_test_split(X_features, y_labels, test_size=0.3, random_state=42)

        tfidf = TfidfVectorizer()
        x_train_tfidf = tfidf.fit_transform(x_train)
        x_test_tfidf = tfidf.transform(x_test)

        lr = LogisticRegression(max_iter=5000)
        lr.fit(x_train_tfidf, y_train)

        return lr, tfidf

    def train_tonality_model(self, filename):
        df = pd.read_csv(filename)
        df['Clean_Text'] = df['Text'].apply(self.preprocess_text)

        X_features = df['Clean_Text']
        y_labels = df['Tonality']

        x_train, x_test, y_train, y_test = train_test_split(X_features, y_labels, test_size=0.3, random_state=42)

        pipe_lr = Pipeline(steps=[('cv', CountVectorizer()), ('lr', LogisticRegression())])
        pipe_lr.fit(x_train, y_train)

        return pipe_lr

    def preprocess_text(self, text):
        text = ntf.remove_userhandles(text)
        text = ntf.remove_stopwords(text)
        return text

    def emo_ji(self, mood):
        mood_mapping = {
            "joy": "😄 JOY",
            "sadness": "😢 SAD",
            "fear": "😨 FEAR",
            "anger": "😡 ANGER",
            "surprise": "😮 SURPRISE",
            "neutral": "😐 NEUTRAL",
            "disgust": "🤢 DISGUST",
            "shame": "😳 SHAME"
        }
        return mood_mapping.get(mood.lower(), "❓")

    async def run_scraper(self, urls, scrape_type):
        self.keywords = []  # Reset keywords
        if scrape_type == 'video_url':
            await self.scrape_video_url(urls)
            return self.keywords
        elif scrape_type == 'url':
            await self.scrape_urls(urls)
            return self.keywords
        elif scrape_type == 'url_comment':
            await self.scrape_comment_url(urls)
            return self.keywords
