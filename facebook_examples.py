from __future__ import division

import datetime
import json

import dateutil
import facebook
import matplotlib.pyplot as plt
import numpy as np
import requests
from prettytable import PrettyTable
from textblob import TextBlob

from credentials import FACEBOOK_ACCESS_TOKEN

graph = facebook.GraphAPI(access_token=FACEBOOK_ACCESS_TOKEN, version=3.0)


def serialize(object):
    # restituisce la rappresentazione JSON di un oggetto
    return json.dumps(object, indent=1)


def place_search():
    # Ricerca i places vicino 1 Hacker Way in Menlo Park, California.
    places = graph.search(type='place',
                          center='37.4845306,-122.1498183',
                          fields='name,location')
    for place in places['data']:
        print('%s %s' % (place['name'].encode('utf8'), place['location'].get('zip')))


def get_posts():
    # definisco l'oggetto da ricercare: puo' essere un id o il nome di una pagina ad esempio
    user = 'BillGates'
    # recupero l'oggetto utilizzando le API
    profile = graph.get_object(user)
    # Recupero i post associati al profilo recuperato
    posts = graph.get_connections(profile['id'], 'posts')
    print(serialize(posts))


def getPostWithPagination():
    # definisco l'oggetto da ricercare: puo' essere un id o il nome di una pagina ad esempio
    user = 'BillGates'
    # seleziono solo i campi da visualizzare
    fields = 'id,category,link,username,talking_about_count'
    # richiedo l'oggetto alle API
    profile = graph.get_object(user, fields=fields)
    # Stampo l'oggetto in formato JSON
    print(serialize(profile))
    # Recupero i post
    posts = graph.get_connections(profile['id'], 'posts')
    # Continuo ad iterare sino a quando ci sono pagine
    while True:
        try:
            for post in posts['data']:
                print(serialize(post))
                print(serialize(graph.get_connections(post['id'], 'comments')))
            # recupero i nuovi post utilizzando i link contenuti nell'oggetto restituito
            posts = requests.get(posts['paging']['next']).json()
            # quando posts['paging'] non ha nessuna chiave 'next'
            # viene lanciata l'eccezzione KeyError e significa che non
            # ci son piu' pagine da iterare
        except KeyError:
            break


def get_posts_data(query, count=100):
    # seleziono solo i campi da visualizzare
    fields = 'id,category,link,username,talking_about_count'
    # richiedo l'oggetto alle API
    profile = graph.get_object(query, fields=fields)
    # Recupero i post
    posts = graph.get_connections(profile['id'], 'posts')
    post_list = []
    # Continuo ad iterare sino a quando ci sono pagine
    while len(post_list) < count:
        try:
            for post in posts['data']:
                if 'message' in post and len(post_list) < count:
                    post_list.append(post)
            # recupero i nuovi post utilizzando i link contenuti nell'oggetto restituito
            posts = requests.get(posts['paging']['next']).json()
            # quando posts['paging'] non ha nessuna chiave 'next'
            # viene lanciata l'eccezzione KeyError e significa che non
            # ci son piu' pagine da iterare
        except KeyError:
            break
    return post_list


def get_posts_data_by_date(query, since, until, count=500):
    # seleziono solo i campi da visualizzare
    # richiedo l'oggetto alle API
    # Recupero i post
    posts = graph.get_object(
        "%s/posts" % query,
        since=since,
        until=until,
        limit=100
    )
    post_list = []
    # Continuo ad iterare sino a quando ci sono pagine
    while len(post_list) < count:
        try:
            for post in posts['data']:
                if 'message' in post and len(post_list) < count:
                    post_list.append(post)
            # recupero i nuovi post utilizzando i link contenuti nell'oggetto restituito
            posts = requests.get(posts['paging']['next']).json()
            # quando posts['paging'] non ha nessuna chiave 'next'
            # viene lanciata l'eccezzione KeyError e significa che non
            # ci son piu' pagine da iterare
        except KeyError:
            break
    return post_list


def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


def comparative_sentiment(
        entity1="CocaColaUnitedStates",
        entity2="PepsiMaxUSA",
        count=100):
    # recupero il testo dei posts
    entity1_posts = get_posts_data(entity1, count=count)
    entity2_posts = get_posts_data(entity2, count=count)
    print(entity2_posts[0])
    # estraggo solo il testo del post
    entity1Messages = [post['message'] for post in entity1_posts]
    entity2Messages = [post['message'] for post in entity2_posts]
    # calcolo il sentiment per i singoli messaggi
    entity1Sentiment = [get_sentiment(message) for message in entity1Messages]
    entity2Sentiment = [get_sentiment(message) for message in entity2Messages]
    # imposto la tabella
    pretty_table = PrettyTable(field_names=['Metric', entity1, entity2])
    # numero di posts
    pretty_table.add_row([
        '# Posts',
        len(entity1Sentiment),
        len(entity2Sentiment)
    ])
    # sentiment medio
    pretty_table.add_row([
        'Sentiment AVG',
        '%0.2f' % np.mean(entity1Sentiment),
        '%0.2f' % np.mean(entity2Sentiment)
    ])
    pretty_table.add_row([
        'Sentiment AVG No Neutral',
        "%.2f" % np.mean(filter(lambda x: x != 0, entity1Sentiment)),
        "%.2f" % np.mean(filter(lambda x: x != 0, entity2Sentiment))
    ])
    # calcolo la percentuale di commenti neutrali/positivi/negativi filtrando i valori dalla lista dei sentiment
    pretty_table.add_row([
        'Neutral',
        '%0.2f%%' % (len(filter(lambda x: x == 0.0, entity1Sentiment)) / count * 100),
        '%0.2f%%' % (len(filter(lambda x: x == 0.0, entity2Sentiment)) / count * 100)
    ])
    pretty_table.add_row([
        'Positive',
        '%0.2f%%' % (len(filter(lambda x: x > 0.0, entity1Sentiment)) / count * 100),
        '%0.2f%%' % (len(filter(lambda x: x > 0.0, entity2Sentiment)) / count * 100)
    ])
    pretty_table.add_row([
        'Negative',
        '%0.2f%%' % (len(filter(lambda x: x < 0.0, entity1Sentiment)) / count * 100),
        '%0.2f%%' % (len(filter(lambda x: x < 0.0, entity2Sentiment)) / count * 100)
    ])
    pretty_table.align['Metric'] = 'l'
    print(pretty_table)
    # Faccio il boxplot dei risultati
    labels = [entity1, entity2]
    plt.figure()
    plt.boxplot(
        [entity1Sentiment, entity2Sentiment],  # passo le due serie di dati
        labels=labels
    )
    plt.show()
    entity1_dates = [
        dateutil.parser.parse(post['created_time'])
        for post in entity1_posts
    ]
    entity2_dates = [
        dateutil.parser.parse(post['created_time'])
        for post in entity2_posts
    ]
    plt.figure()
    plt.plot(entity1_dates, entity1Sentiment)
    plt.plot(entity2_dates, entity2Sentiment)
    plt.legend([entity1, entity2])
    plt.show()


def comparative_sentiment_over_time(
        entity1="donaldtrump",
        entity2="hillaryclinton",
        since='2016-01-01',
        until='2016-02-01',
        count=100):
    # recupero i post nel periodo desiderato
    entity1_posts = get_posts_data_by_date(entity1, since, until, count)
    entity2_posts = get_posts_data_by_date(entity2, since, until, count)
    # estraggo solo il testo del post
    entity1_messages = [post['message'] for post in entity1_posts]
    entity2_messages = [post['message'] for post in entity2_posts]
    # calcolo il sentiment per i singoli messaggi
    entity1_sentiment = [get_sentiment(message) for message in entity1_messages]
    entity2_sentiment = [get_sentiment(message) for message in entity2_messages]
    # Estraggo le date dai posts
    entity1_dates = [
        dateutil.parser.parse(post['created_time'])
        for post in entity1_posts
    ]
    print(entity1_dates)
    entity2_dates = [
        dateutil.parser.parse(post['created_time'])
        for post in entity2_posts
    ]
    # faccio il plot dei risultati
    plt.figure()
    plt.plot(entity1_dates, entity1_sentiment)
    plt.plot(entity2_dates, entity2_sentiment)
    plt.legend([entity1, entity2])
    plt.show()


def group_posts_sentiment_by_day(posts):
    messages_per_day = {}
    for post in posts:
        date_parsed = dateutil.parser.parse(post['created_time']).strftime('%Y-%m-%d')
        sentiment = TextBlob(post['message']).sentiment.polarity
        if date_parsed in messages_per_day.keys():
            messages_per_day[date_parsed].append(sentiment)
        else:
            messages_per_day[date_parsed] = [sentiment]
    return messages_per_day


def comparative_sentiment_avg_per_day(
        entity1="donaldtrump",
        entity2="hillaryclinton",
        since='2016-01-01',
        until='2016-06-01',
        count=100):
    # recupero i post nel periodo desiderato
    entity1_posts = get_posts_data_by_date(entity1, since, until, count)
    entity2_posts = get_posts_data_by_date(entity2, since, until, count)
    # Estraggo le date dai posts
    entity1_sentiment_per_day = group_posts_sentiment_by_day(entity1_posts)
    entity2_sentiment_per_day = group_posts_sentiment_by_day(entity2_posts)
    entity_dates = sorted(
        list(set(entity1_sentiment_per_day.keys()).intersection(set(entity2_sentiment_per_day.keys()))))
    entity1_sentiment = [np.mean(entity1_sentiment_per_day[date])
                         for date in entity_dates]
    entity2_sentiment = [np.mean(entity2_sentiment_per_day[date])
                         for date in entity_dates
                         if date in entity2_sentiment_per_day.keys()]

    # # faccio il plot dei risultati
    plt.figure()
    plt.plot(entity_dates, entity1_sentiment)
    plt.plot(entity_dates, entity2_sentiment)
    plt.legend([entity1, entity2])
    plt.xticks(entity_dates, entity_dates, rotation='45')
    plt.show()


if __name__ == '__main__':
    comparative_sentiment('donaldtrump', 'hillaryclinton')
    comparative_sentiment_avg_per_day(
        'donaldtrump',
        'hillaryclinton',
        since='1 january 2016',
        until='1 march 2016',
        count=1000
    )
