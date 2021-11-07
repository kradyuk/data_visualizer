import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

from plotly.subplots import make_subplots 
import plotly.graph_objects as go


st.title("Анализ комментариев инстаграм-аккаунта @uo_ggkttid")
st.sidebar.title("Боковая панель настройки")

st.markdown("Ресурс представляет собой панели визуализации для анализа комментариев на примере инстаграм-аккаунта @uo_ggkttid 📊")
st.sidebar.markdown("Анализ комментариев инстаграм-аккаунта @uo_ggkttid")

#DATA_URL = ("/Users/admin/Projects/py_example/data.csv")
DATA_URL = ("01_data.csv")

@st.cache(persist=False)
def load_data():
  data = pd.read_csv(DATA_URL, encoding='utf-8')
  data['comment_created'] = pd.to_datetime(data['comment_created'])
  return data


data = load_data()

st.sidebar.subheader("Показать случайный комментарий")
random_comment = st.sidebar.radio('Сентименты', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('year_sentiment == @random_comment')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Количественное сравнение комментариев")
select = st.sidebar.selectbox('Тип визуализации', ['Гистограмма', 'Круговая диаграмма'], key='1')
# Why re-dermination of the same var here?
sentiment_count = data['year_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Comments':sentiment_count.values})

if not st.sidebar.checkbox("Скрыть", True):
  st.markdown("### Количественное сравнение комментариев")
  if select == "Гистограмма":
    fig2 = px.bar(sentiment_count, x='Sentiment', y='Comments', color='Comments', height=500)
    st.plotly_chart(fig2)
  else:
    fig1 = px.pie(sentiment_count, values='Comments', names='Sentiment')
    st.plotly_chart(fig1)


st.sidebar.subheader("Когда и откуда пользователи оставляли комментарии?")
hour = st.sidebar.number_input("Время суток", min_value=1, max_value=24)
modified_data = data[data['comment_created'].dt.hour == hour]
if not st.sidebar.checkbox("Скрыть", True, key='1'):
  st.markdown("### Местоположение пользователей оставивших комментарии в зависимости от времени суток")
  st.markdown("%i комментариев в период с %i:00 до %i:00" % (len(modified_data), hour, (hour+1)%24))
  st.map(modified_data)
  if st.sidebar.checkbox("Показать необработанные данные", False):
    st.write(modified_data)


st.sidebar.subheader("Распределение комментариев по годам")
choice = st.sidebar.multiselect('Выбрать год', (2020, 2021, 2019))
if len(choice) > 0:
  choice_data = data[data.year.isin(choice)]
  fig_choice = px.histogram(choice_data, x='year', y='year_sentiment', histfunc='count', color='year_sentiment',
  facet_col='year_sentiment',labels={'year_sentiment':'comments'}, height=600, width=800)
  st.plotly_chart(fig_choice)


st.sidebar.header("Облако комментариев")
word_sentiment = st.sidebar.radio('Sentiment', ('positive','neutral', 'negative'))
st.set_option('deprecation.showPyplotGlobalUse', False)

if not st.sidebar.checkbox("Скрыть", True, key='3'):
  st.header('Облако комментариев - %s' % (word_sentiment))
  df = data[data['year_sentiment']==word_sentiment]
  words = ' '.join(df['text'])
  processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
  wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
  plt.imshow(wordcloud)
  plt.xticks([])
  plt.yticks([])
  st.pyplot()

