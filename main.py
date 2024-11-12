import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

# ユーザー認証データベース
users_db = {
    "user1": "passsworrrD1",
    "user2": "password2",
    "user3": "password3"
}

# セッション状態の初期化
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.history = pd.DataFrame(columns=["日付", "天気", "体調", "気持ち", "コンディション", "コメント"])

def login_page():
    st.title("ログイン")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    
    if st.button("ログイン"):
        if username in users_db and users_db[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"ようこそ、{username}さん！")
        else:
            st.error("ユーザー名またはパスワードが間違っています")

def home_page():
    st.title(f"ようこそ、{st.session_state.username}さん！")
    
    data_file = f"{st.session_state.username}_daily_mood_data.csv"
    
    # 履歴データが保存されているかチェック
    if os.path.exists(data_file):
        st.session_state.history = pd.read_csv(data_file)

    # 質問を表示
    weather = st.radio("今日の天気は？", ("晴れ", "くもり", "雨"))
    health = st.radio("今日の体調は？", ("良い", "悪い", "普通", "わからない"))
    mood = st.radio("今日の気持ちは？", ("良い", "悪い", "普通", "わからない"))
    condition = st.multiselect("あなたの今の具体的な気持ちは？（複数選択可）", 
                               ("安心", "感謝", "興奮", "冷静", "満足", "快感", "期待", "優越感", 
                                "嫌悪", "嫉妬", "罪悪感", "劣等感", "悲しみ", "苦しみ", "怒り"))
    text = st.text_input("今の気持ちをコメントしてください")
    
    submit_btn = st.button("送信")
    
    if submit_btn:
        # 送信ボタンが押された時、データを履歴に追加
        current_date = datetime.now().strftime("%Y-%m-%d")
        new_data = pd.DataFrame({
            "日付": [current_date],
            "天気": [weather],
            "体調": [health],
            "気持ち": [mood],
            "コンディション": [",".join(condition)],
            "コメント": [text]
        })
        
        st.session_state.history = pd.concat([st.session_state.history, new_data], ignore_index=True)
        
        # 履歴をCSVに保存
        st.session_state.history.to_csv(data_file, index=False)

        # 個別データの表示
        st.subheader("入力内容:")
        st.write(f"天気: {weather}")
        st.write(f"体調: {health}")
        st.write(f"気持ち: {mood}")
        st.write(f"コンディション: {', '.join(condition)}")
        st.write(f"コメント: {text}")

        # 点数化のマッピング
        health_map = {"良い": 2, "普通": 1, "悪い": 0, "わからない": np.nan}
        weather_map = {"晴れ": 2, "くもり": 1, "雨": 0}
        mood_map = {"良い": 2, "普通": 1, "悪い": 0, "わからない": np.nan}

        # 各項目を点数化
        st.session_state.history['体調点数'] = st.session_state.history['体調'].map(health_map)
        st.session_state.history['天気点数'] = st.session_state.history['天気'].map(weather_map)
        st.session_state.history['気持ち点数'] = st.session_state.history['気持ち'].map(mood_map)

        # プロットを作成
        fig, ax = plt.subplots(figsize=(10, 6))

        # 体調、天気、気持ちをそれぞれ異なる色でプロット
        ax.plot(st.session_state.history['日付'], st.session_state.history['体調点数'], label='体調', color='tab:blue', marker='o')
        ax.plot(st.session_state.history['日付'], st.session_state.history['天気点数'], label='天気', color='tab:orange', marker='s')
        ax.plot(st.session_state.history['日付'], st.session_state.history['気持ち点数'], label='気持ち', color='tab:green', marker='^')

        # ラベルとタイトル
        ax.set_xlabel('日付')
        ax.set_ylabel('点数')
        ax.set_title('日付ごとの体調、天気、気持ちの推移')
        ax.legend()

        # 日付ラベルが重ならないように回転
        plt.xticks(rotation=45)

        # グラフを表示
        st.pyplot(fig)

if not st.session_state.logged_in:
    login_page()
else:
    home_page()
