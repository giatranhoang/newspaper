# Import Streamlit library
import streamlit as st

from google.oauth2 import service_account

# Import Newspaper library
import newspaper
import pandas as pd
from newspaper import Article
from newspaper import news_pool
import nltk
nltk.download('punkt')

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"])

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    

    translate_client = translate.Client(credentials=credentials)

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    return result

def as_dict(self):
    return {'title': self.title, 'url':self.url}

st.title("COVID-19 - Press and Media Monitor App")

summary = ''
with st.form('my_form'):
    url = st.text_input("Input URL of the news you want to summary")

    submitted = st.form_submit_button('Submit')
    if submitted:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        summary = article.summary
        st.markdown(summary)

translated = translate_text('en', summary)
st.markdown(translated["translatedText"])



        
