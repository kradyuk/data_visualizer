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
DATA_URL = ("data.csv")

@st.cache(persist=False)
def load_data():
  data = pd.read_csv(DATA_URL, encoding='utf-8')
  data['tweet_created'] = pd.to_datetime(data['tweet_created'])
  return data


data = load_data()

st.sidebar.subheader("Показать случайный комментарий")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Количественное сравнение комментариев")
select = st.sidebar.selectbox('Тип визуализации', ['Гистограмма', 'Круговая диаграмма'], key='1')
# Why re-dermination of the same var here?
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Скрыть", True):
  st.markdown("### Количественное сравнение комментариев")
  if select == "Гистограмма":
    fig2 = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
    st.plotly_chart(fig2)
  else:
    fig1 = px.pie(sentiment_count, values='Tweets', names='Sentiment')
    st.plotly_chart(fig1)


st.sidebar.subheader("Когда и откуда пользователи оставляли комментарии?")
hour = st.sidebar.number_input("Время суток", min_value=1, max_value=24)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Скрыть", True, key='1'):
  st.markdown("### Местоположение пользователей оставивших комментарии в зависимости от времени суток")
  st.markdown("%i комментариев в период с %i:00 до %i:00" % (len(modified_data), hour, (hour+1)%24))
  st.map(modified_data)
  if st.sidebar.checkbox("Показать необработанные данные", False):
    st.write(modified_data)


st.sidebar.subheader("Распределение комментариев по годам")
choice = st.sidebar.multiselect('Выбрать год', ('2020', '2021', '2019'))
if len(choice) > 0:
  choice_data = data[data.airline.isin(choice)]
  fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment',
  facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'}, height=600, width=800)
  st.plotly_chart(fig_choice)

#####Before changes (original part):
#
#@st.cache(persist=True) 
#def plot_sentiment(airline):  
#  df = data[data['airline']==airline] 
#  count = df['airline_sentiment'].value_counts()  
#  count = pd.DataFrame({'Sentiment':count.index, 'Tweets':count.values.flatten()})  
#  return count
#
#st.sidebar.subheader("Breakdown airline by sentiment")
#choice = st.sidebar.multiselect('Pick airlines', ('US Airways','United','American','Southwest','Delta','Virgin America'))
#if len(choice) > 0:
#    st.subheader("Breakdown airline by sentiment")
#    breakdown_type = st.sidebar.selectbox('Visualization type', ['Pie chart', 'Bar plot', ], key='3')
#    fig_3 = make_subplots(rows=1, cols=len(choice), subplot_titles=choice)
#    if breakdown_type == 'Bar plot':
#        for i in range(1):
#            for j in range(len(choice)):
#                fig_3.add_trace(
#                    go.Bar(x=plot_sentiment(choice[j]).Sentiment, y=plot_sentiment(choice[j]).Tweets, showlegend=False),
#                    row=i+1, col=j+1
#                )
#        fig_3.update_layout(height=600, width=800)
#        st.plotly_chart(fig_3)
#    else:
#        fig_3 = make_subplots(rows=1, cols=len(choice), specs=[[{'type':'domain'}]*len(choice)], subplot_titles=choice)
#        for i in range(1):
#            for j in range(len(choice)):
#                fig_3.add_trace(
#                    go.Pie(labels=plot_sentiment(choice[j]).Sentiment, values=plot_sentiment(choice[j]).Tweets, showlegend=True),
#                    i+1, j+1
#                )
#        fig_3.update_layout(height=600, width=800)
#        st.plotly_chart(fig_3)
#st.sidebar.subheader("Breakdown airline by sentiment")
#choice = st.sidebar.multiselect('Pick airlines', ('US Airways','United','American','Southwest','Delta','Virgin America'), key=0)
#if len(choice) > 0:
#    choice_data = data[data.airline.isin(choice)]
#    fig_0 = px.histogram(
#                        choice_data, x='airline', y='airline_sentiment',
#                         histfunc='count', color='airline_sentiment',
#                         facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'},
#                          height=600, width=800)
#    st.plotly_chart(fig_0)
#
###

st.sidebar.header("Облако комментариев")
word_sentiment = st.sidebar.radio('sentiment', ('positive','neutral', 'negative'))
st.set_option('deprecation.showPyplotGlobalUse', False)

if not st.sidebar.checkbox("Скрыть", True, key='3'):
  st.header('Word cloud for %s sentiment' % (word_sentiment))
  df = data[data['airline_sentiment']==word_sentiment]
  words = ' '.join(df['text'])
  processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
  wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
  plt.imshow(wordcloud)
  plt.xticks([])
  plt.yticks([])
  st.pyplot()
