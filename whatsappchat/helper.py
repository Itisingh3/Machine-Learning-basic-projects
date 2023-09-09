# file that helps to return answers

from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):
    # if overall nhi hain it means hume particular user ka data chahiye.then
    if selected_user != 'Overall':
        # masking of the selected user and store in df ex. df[df['user]=='Iti Singh] then store it in df
        df = df[df['user'] == selected_user]
    # fetch the number of messages of that df ex. Iti Singh.shape gives (1294, 4),  here 1294 at oth position gives total number of messages;
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages and it means photos , videos etc.
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    # message mein find_urls karke sare url identify kar lenge aur extract kar lenge and phir links mein add kar denge.
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    # return all the answers that you have calculated.
    return num_messages,len(words),num_media_messages,len(links)



# finding most busy users
def most_busy_users(df):
    # # top 5 busy users by counting the values . i.e total messages of a particular using value_counts
    x = df['user'].value_counts().head()
    # formula for finding percentage i.e (value_counts/total_messages)*100 and round uptli 2 decimal points.
    # rename the user to percent. 
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df




# word cloud
def create_wordcloud(selected_user,df):

    # stop_hinglish file mein woh wrods hai jo hindi and english ka mixture hai. aur yeh file google se download kiya hai 
    # r refers to reading mode.
    f = open('stop_hinglish.txt', 'r')
    # stop_words variable mein f ko read karke rakh liya
    stop_words = f.read()

     
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
     
    # temp mein woh sare words ayenge jo group notification and media ommited nhi hai.
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    # function to stop words
    # # stop words--> used in sentence formation and does not have existence itself
    def remove_stop_words(message):
        y = []
        # every words converts into lowercase and then checked .
        for word in message.lower().split():
            # if word  is not  in stop_words ie. stop_hinglish file then append into y array
            if word not in stop_words:
                y.append(word)
                # wapas sentence form karke bhej denge
        return " ".join(y)
    
    # wordcloud ek image generate karega 
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    # temp['message'] = temp['message'].apply(remove_stop_words)
    # image generate karega and words ko split kar dega aur df_wc mein store karke return lar dega
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
    




def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    # # counter on words list and select top 20
    # # convert intodata frame
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    emojis = []
    for message in df['message']:
        # if message mein  EMOJI_DATA se match hota hai to usse emojis mein append kar do
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    # emojis ko counter function mein bhej kar uska length count karke . and sare emojis count karke most common batana hai.
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df





def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # timeline mein year month_num month columns banakar count karna hai message ko aur serial wise diplay karna hainindex kause karke
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    # # shape[0] means indexes
    for i in range(timeline.shape[0]):
        #     month-year ko display karna hai
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    # new column name time
    timeline['time'] = time

    return timeline








def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # only_date is new column and we have to count message dt extract karke
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


# this function tells har week mein users sabse jyada kab active rehte hailike monday,tuesday etc.
def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # day_name column contains Monday to saturday names etc
    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # day_month column contains jan to december names etc
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # pivot table mein indexing day_name par ki gayi hai and columns mein period rhega value msg hai jisse count karna hai and jha par koimsg nhi hai wha 0 hai.
    # ex. period 00-1 1-2 2-3 3-4 4-5 5-6 etc
    #  day_name monday tuesday etc
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap