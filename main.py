import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import time
import os

# ユーザーデータベース（仮のもの）
users_db = {
    "user1": "passsworrrD1",
    "user2": "password2",
    "user3": "password3"
}

# セッションステートの初期化（ログイン状態を管理）
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ログインページ
def login_page():
    st.title("ログイン")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    
    if st.button("ログイン"):
        if username in users_db and users_db[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"ようこそ、{username}さん！")
            # ログイン後のホーム画面に進む
            home_page()
        else:
            st.error("ユーザー名またはパスワードが間違っています")

# ホームページ
def home_page():
    st.title(f"ようこそ、{st.session_state.username}さん！")
    
    data_file = f"{st.session_state.username}_daily_mood_data.csv"

    # 履歴データが存在しない場合に初期化
    if "history" not in st.session_state:
        if os.path.exists(data_file):
            st.session_state.history = pd.read_csv(data_file)
        else:
            st.session_state.history = pd.DataFrame(columns=["日付", "合計"])

    # 質問と入力フィールド
    weather = st.radio("今日の天気は？", ("晴れ", "くもり", "雨"))
    health1 = st.radio("今日の体調は？", ("良い", "悪い", "普通", "わからない"))
    health = st.radio("今日の気持ちは？", ("良い", "悪い", "普通", "わからない"))
    condition = st.multiselect("あなたの今の具体的な気持ちは？（複数選択可）", 
                               ("安心", "感謝", "興奮", "冷静", "満足", "快感", "期待", 
                                "優越感", "嫌悪", "嫉妬", "罪悪感", "劣等感", "悲しみ", "苦しみ", "怒り"))
    text = st.text_input("今の気持ちをコメントしてください")

    submit_btn = st.button("送信")
    cancel_btn = st.button("キャンセル")

    # 最新の進行状況表示（必要なら）
    latest_iteration = st.empty()
    bar = st.progress(0)

    # コメントの長さ制限
    if len(text) > 200:
        st.warning("コメントは200文字以内にしてください")

    # 送信ボタンが押されたとき
    if submit_btn:
        # 進行状況バー
        for i in range(100):
            latest_iteration.text(f"Iteration {i + 1}")
            bar.progress(i + 1)
            time.sleep(0.01)

        # 入力内容の表示
        st.write(f"天気：{weather}")
        st.write(f"体調：{health}")
        st.write(f"コンディション：{', '.join(condition)}")
        st.write(f"今の気持ち：{text}")

        # 画像の表示（天気と体調に基づいて）
        image_map = {
            ("晴れ", "良い"): ("My project/父黒.jpg", "今日はいい日だね"),
            ("雨", "悪い"): ("My project/父オレンジ.jpg", "元気出せよ"),
            ("晴れ", "悪い"): ("My project/父サイズ.jpg", "空は晴れているけど君の心は曇っているみたいだね"),
            ("雨", "良い"): ("My project/父ピース.jpg", "雨だけど気分がいいなんて、素敵だね"),
            ("普通",): ("My project/父あさちゃん.jpg", "なんでもない日が実は一番大切なんだよ"),
            ("わからない",): ("My project/父ジョンレノン.jpg", "自分の気持ちが分からないときは、俺に聴いてみな"),
            ("くもり", "良い"): ("My project/父広げる.jpg", "心はすっきり晴れているみたいだね、やるじゃないか"),
            ("くもり", "悪い"): ("My project/父あさちゃん目.jpg", "微妙な日みたいだけどちゃんとご飯を食べてえらい！")
        }

        # 画像を表示
        img_path, message = image_map.get((weather, health), image_map.get((weather,), ("", "")))
        if img_path:
            try:
                img = Image.open(img_path)
                st.subheader(message)
                st.image(img, use_column_width=True)
            except FileNotFoundError:
                st.error("画像ファイルが見つかりません")

        # スコア計算
        health1_number = {"良い": 100, "普通": 50, "悪い": -50, "わからない": 0}[health1]
        health_number = {"良い": 100, "普通": 50, "悪い": -50, "わからない": 0}[health]
        weather_number = {"晴れ": 100, "くもり": 50, "雨": 0}[weather]
        total_score = weather_number + health1_number + health_number

        # 日付を取得してデータに追加
        current_date = datetime.now().strftime("%Y-%m-%d")
        new_data = pd.DataFrame({"日付": [current_date], "合計": [total_score]})

        # 履歴データに追加（重複を避ける）
        st.session_state.history = pd.concat(
            [st.session_state.history[st.session_state.history["日付"] != current_date], new_data],
            ignore_index=True
        )

        # 履歴データをCSVファイルに保存
        st.session_state.history.to_csv(data_file, index=False)

        # グラフの表示
        st.line_chart(st.session_state.history.set_index("日付")["合計"])

        # 合計スコアの表示
        st.write(f"今日の気分スコア: {total_score}")

# ログインしていない場合、ログイン画面を表示
if not st.session_state.logged_in:
    login_page()
else:
    home_page()
