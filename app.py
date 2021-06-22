#!/usr/bin/env python
# coding: utf-8

# In[20]:


import flask
import csv
from flask import Flask, render_template, request
import difflib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

app = flask.Flask(__name__, template_folder='templates')

df2 = pd.read_csv('data.csv')
count = TfidfVectorizer(ngram_range=(1, 3))
count_matrix = count.fit_transform(df2['Tags'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['Title'])
all_titles = [df2['Title'][i] for i in range(len(df2['Title']))]


def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['Title'].iloc[movie_indices]
    date = df2['Publish_date'].iloc[movie_indices]
    tumbnail = df2['Thumbnails'].iloc[movie_indices]
    views = df2['Views'].iloc[movie_indices]
    likes = df2['Likes'].iloc[movie_indices]
    dislikes = df2['Dislikes'].iloc[movie_indices]
    url = df2['Urls'].iloc[movie_indices]

    rec_df = pd.DataFrame(
        {'Video': tit, 'Publish_date':date, 'tumbnail': tumbnail,'Views': views, 'Likes': likes,
         'Dislike': dislikes, 'Video_url': url})
    return rec_df

def get_suggestions():
    data = pd.read_csv('data.csv')
    return list(data['Title'])


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    suggestions = get_suggestions()
    return flask.render_template('home.html',suggestions=suggestions)

# Set up the main route
@app.route('/positive', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return (flask.render_template('home.html'))

    if flask.request.method == 'POST':
        m_name = flask.request.form['title_name']
        #m_name = m_name.title()
        if m_name not in all_titles:
            return (flask.render_template('negative.html', name=m_name))
        else:
            # with open('movieR.csv', 'a', newline='') as csv_file:
            #     fieldnames = ['Movie']
            #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            #     writer.writerow({'Movie': m_name})
            result_final = get_recommendations(m_name)
            titles = []
            dates = []
            tumbnails = []
            views = []
            likes = []
            dislikes = []
            urls = []
            for i in range(len(result_final)):
                titles.append(result_final.iloc[i][0])
                dates.append(result_final.iloc[i][1])
                tumbnails.append(result_final.iloc[i][2])
                views.append(result_final.iloc[i][3])
                likes.append(result_final.iloc[i][4])
                dislikes.append(result_final.iloc[i][5])
                urls.append(result_final.iloc[i][6])

            return flask.render_template('positive.html', Titles=titles, Dates=dates, Tumbnails=tumbnails,
                                         Views=views, Likes=likes, Dislikes=dislikes, Urls=urls, search_name=m_name)


if __name__ == '__main__':
    app.run()


# In[ ]:




