# main like index.html
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
# call the function def preprossor into preroccesor.py so that it present data in form of data frame
import preprocessor,helper

# st have a method sidebar and it have function titile which put the argument int the left side.
st.sidebar.title("Whatsapp Chat Analyzer")

# go to the documentation of streamlit and copy the code of uploading files 
# store the file into uploaded_file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # if not none then store the calue in bytes_Data
    bytes_data = uploaded_file.getvalue()
    # decode the bytes_Data into utf-8 form and store
    data = bytes_data.decode("utf-8")
    # check is converted or not
    # st.text(data);
    # preprocessor file have preprocess(data) function and store that data frame into df.
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    # fetch unique users from column 'user' then convert into tolist() and store in user_list 
    user_list = df['user'].unique().tolist()
    # remove group notification
    user_list.remove('group_notification')
    user_list.sort()
    # 0th position par overall hai . uske baad slect kar sakte hai
    user_list.insert(0,"Overall")
    # sidebar mein selectbox chahiye aur usein user_list variable ko pass kar diya in order to know the number of users in chat
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    # show analysis button jab true hoga tabhi nanalysis karenge
    if st.sidebar.button("Show Analysis"):
        # helper function takes ARGUMENT OF selected user and df.
        st.title('Total Statistics')
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        # Set of four columns and this containe total secnario of chat.
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)


        # 2nd para
        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            # most_busy_users function have df as a parameter.
            x,new_df = helper.most_busy_users(df)
            # store graph in ax . plt have a function name subplots which plot the graph.
            fig, ax = plt.subplots()
            # two columns 1st-> graph and 2nd have analysis in percentage.
            col1, col2 = st.columns(2)
            # 
            with col1:
                # we want to plot the bar graph and takes parameter as index and values. and color of bars is red. 
                ax.bar(x.index, x.values,color='red')
                # x wale line mein index ko vertical rotate karaya hai.
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            # every users messages and percentage of messages.
            with col2:
                st.dataframe(new_df)


        # WordCloud
        # set title for  word cloud
        st.title("Wordcloud")
        # function call kar rhe aur value ko df_wc mein store kar rhe and helper function return image.
        df_wc = helper.create_wordcloud(selected_user,df)
        # hume subplots plot karna hain
        fig,ax = plt.subplots()
        # ax par image ko show karna hai 
        ax.imshow(df_wc)
        # and figure ko maine pyplot main pass kar diya.
        st.pyplot(fig)


        # most common words
        # intially:  most_common_df = helper.most_common_words(selected_user,df)
        # st.dataframe(most_common_df) 
        # above code is for data frame
        # below code is for graph
        most_common_df = helper.most_common_words(selected_user,df)
        # subplot mein figure and axis
        fig,ax = plt.subplots()
        # 0: message words , 1: par number of words ie. morning : 1234
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            # 0: emoji and 1: frequency , 0.2f is percentage
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)


        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        # x axis ->time , y axis ->message
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        # x axis : only_date , y axis: message
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



         # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        # sns have have function heatmap jiki wajah se visa figure bana hai .itna unique
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
