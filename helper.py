import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
extractor = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]

    # Total no. of messages
    num_messages=df['user'].shape[0]

    # No. of words
    words=[]
    for message in df['message']:
        words.extend(message.split())

   # Total media files
    num_media_msg=df[df['message'] == '<Media omitted>\n'].shape[0]

    # total links
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    return num_messages,len(words),num_media_msg,len(links)

def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/len(df))*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]

    wc=WordCloud(max_font_size=100,width=500,height=500,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_frequent_words(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]
    else:
        df=df[df['user']!='group_notification']

    df=df[df['message'] != '<Media omitted>\n']

    f=open('stop_hinglish.txt','r')
    stop_words=f.read()

    words=[]
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_stats(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]

    timeline=df.groupby(['year','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_stats(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]

    daily_timeline=df.groupby(['date']).count()['message'].reset_index()
    return daily_timeline

def activity_map_helper(selected_user,df):
    if selected_user != "Overall":
        df=df[df['user']==selected_user]

    weekly_timeline=df['date'].dt.day_name().value_counts().reset_index()
    return weekly_timeline
