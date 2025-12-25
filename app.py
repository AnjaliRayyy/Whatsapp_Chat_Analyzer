import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    # layout="wide"
)

# ================= DARK MODE CSS =================
st.markdown("""
<style>
.stApp {
    background-color: #0B141A;
    color: #E9EDEF;
    font-family: 'Segoe UI', sans-serif;
}

section[data-testid="stSidebar"] {
    background-color: #111B21;
}

section[data-testid="stSidebar"] * {
    color: #E9EDEF !important;
}

h1, h2, h3 {
    color: #E9EDEF !important;
}

.stButton > button {
    background-color: #25D366;
    color: #111B21;
    border-radius: 25px;
    padding: 0.6em 1.6em;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #1DA851;
}

.stat-card {
    background-color: #1F2C33;
    color: #E9EDEF;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0px 6px 15px rgba(0,0,0,0.6);
}

.stat-card h1 {
    color: #25D366 !important;
}

.stat-card h3 {
    color: #AEBAC1 !important;
}

[data-testid="stDataFrame"] {
    background-color: #1F2C33;
    color: #E9EDEF;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<h1 style='text-align:center;'>💬 WhatsApp Chat Analyzer</h1>
<p style='text-align:center; color:#AEBAC1;'>
Analyze your WhatsApp conversations visually
</p>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.title("📂 Upload Chat File")
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat file (.txt)")

if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("👤 Select User", user_list)

    if st.sidebar.button("🚀 Analyze"):

        # ================= STATS =================
        st.title("📊 Top Statistics")
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f"<div class='stat-card'><h3>Total Messages</h3><h1>{num_messages}</h1></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-card'><h3>Total Words</h3><h1>{num_words}</h1></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-card'><h3>Media Shared</h3><h1>{num_media}</h1></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='stat-card'><h3>Links Shared</h3><h1>{num_links}</h1></div>", unsafe_allow_html=True)

        # ================= MONTHLY TIMELINE =================
        st.title("📅 Monthly Timeline")
        timeline = helper.monthly_stats(selected_user, df)

        left, center, right = st.columns([1, 2, 1])
        with center:
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(timeline['time'], timeline['message'], color='#25D366')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # ================= DAILY TIMELINE =================
        st.title("🗓 Daily Timeline")
        daily = helper.daily_stats(selected_user, df)

        left, center, right = st.columns([1, 2, 1])
        with center:
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(daily['date'], daily['message'], color='#25D366')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # ================= ACTIVITY MAP =================
        st.title("📈 Most Active Week Days")
        activity = helper.activity_map_helper(selected_user, df)

        left, center, right = st.columns([1, 2, 1])
        with center:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(activity['date'], activity['count'], color='#25D366')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # ================= MOST ACTIVE USERS =================
        if selected_user == 'Overall':
            st.title("🔥 Most Active Users")
            x, active_df = helper.most_active_users(df)

            left, center, right = st.columns([1, 2, 1])
            with center:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(x.index, x.values, color='#25D366')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            st.dataframe(active_df.rename(columns={'percent':'members','counts':'percent'}))

        # ================= WORD CLOUD =================
        st.title("☁ Word Cloud")
        wc = helper.create_wordcloud(selected_user, df)

        left, center, right = st.columns([1, 2, 1])
        with center:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.imshow(wc)
            ax.axis("off")
            st.pyplot(fig)

        # ================= MOST FREQUENT WORDS =================
        st.title("📝 Most Frequent Words")
        freq_df = helper.most_frequent_words(selected_user, df)

        left, center, right = st.columns([1, 2, 1])
        with center:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(freq_df[0], freq_df[1], color='#25D366')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        # ================= EMOJI ANALYSIS =================
        st.title("😂 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        emoji_df.rename(columns={0:'emoji',1:'counts'}, inplace=True)
        c1, c2 = st.columns(2)
        with c1:
            st.dataframe(emoji_df)

        with c2:
            label = emoji_df.head(10)['emoji']
            y = emoji_df.head(10)['counts']
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(
               y,
                labels=label,
                autopct='%1.1f%%',
                startangle=140
            )
            st.pyplot(fig)
