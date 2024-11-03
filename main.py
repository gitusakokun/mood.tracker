import streamlit as st
import time
from PIL import Image 
import pandas as pd
from datetime import datetime
import os

st.title("きのこ")

st.caption("質問に答える")

weather=st.radio(
    "今日の天気は？",
    ("晴れ","くもり","雨")
)
health1=st.radio("今日の体調は？",
                 ("良い","悪い","普通","わからない"))
health=st.radio("今日の気持ちは？",
                ("良い","悪い","普通","わからない"))
condition=st.multiselect("あなたの今の具体的な気持ちは？（複数選択可）",
                    ("安心","感謝","興奮","冷静","満足","快感","期待","優越感","嫌悪","嫉妬","罪悪感","劣等感","悲しみ","苦しみ","怒り"))

text=st.text_input("今の気持ちをコメントしてください")

submit_btn=st.button("送信")
cansel_btn=st.button("キャンセル")

data_file="daily_mood_data.csv"

if "history" not in st.session_state:
    if os.path.exists(data_file):
        st.session_state.history=pd.read_csv(data_file)
    else:
        st.session_state.history=pd.DataFrame(columns=["日付","合計"])

latest_iteration=st.empty()
bar=st.progress(0)



if submit_btn:
    for i in range(100):
       latest_iteration.text(f"Iteration{i+1}")
       bar.progress(i+1)
       time.sleep(0.01)

    "天気：",weather
    "体調：",health
    "コンディション：",",".join(condition)
    "今の気持ち：",text

    if weather=="晴れ" and health=="良い":
        img=Image.open(r"C:\Users\nagis\OneDrive\デスクトップ\streamlit\父黒.jpg")
        st.subheader("今日はいい日だね")
        st.image(img,use_column_width=True)
    if weather=="雨" and health=="悪い":
        img=Image.open(r"C:\Users\nagis\OneDrive\デスクトップ\streamlit\父オレンジ.jpg")
        st.subheader("元気出せよ")
        st.image(img,use_column_width=True)
    if weather=="晴れ" and health=="悪い":
        img=Image.open(r"C:\Users\nagis\OneDrive\デスクトップ\streamlit\父サイズ.jpg")
        st.subheader("空は晴れているけど君の心は曇っているみたいだね")
        st.image(img,use_column_width=True)
    if weather=="雨" and health=="良い":
        img=Image.open(r"C:\Users\nagis\OneDrive\デスクトップ\streamlit\父ピース.jpg")
        st.subheader("雨だけど気分がいいなんて、素敵だね")
        st.image(img,use_column_width=True)
    if health=="普通":
        img=Image.open(r"C:\Users\nagis\OneDrive\デスクトップ\streamlit\父あさちゃん.jpg")
        st.subheader("なんでもない日が実は一番大切なんだよ")
        st.image(img,use_column_width=True)
    if health =="わからない":
        img=Image.open(r"C:\Users\nagis\OneDrive\デスクトップ\streamlit\父ジョンレノン.jpg")
        st.subheader("自分の気持ちが分からないときは、俺に聴いてみな") 
        st.image(img,use_column_width=True)      
    if weather=="くもり" and health=="良い":
        img=Image.open(r"C:\Users\nagis\OneDrive\デスクトップ\streamlit\父広げる.jpg")
        st.subheader("心はすっきり晴れているみたいだね、やるじゃないか")
        st.image(img,use_column_width=True)
    if weather=="くもり" and health=="悪い":
        img=Image.open(r"C:\Users\nagis\OneDrive\デスクトップ\streamlit\父あさちゃん目.jpg")
        st.subheader("微妙な日みたいだけどちゃんとご飯を食べてえらい！")
        st.image(img,use_column_width=True)

    health1_number = {"良い": 100, "普通": 50, "悪い": -50, "わからない": 0}[health1]
    health_number = {"良い": 100, "普通": 50, "悪い": -50, "わからない": 0}[health]
    weather_number = {"晴れ": 100, "くもり": 50, "雨": 0}[weather]
    total_score = weather_number + health1_number + health_number

    current_date = datetime.now().strftime("%Y-%m-%d")
    new_data = pd.DataFrame({"日付": [current_date], "合計": [total_score]})
    # st.session_state.history = pd.concat([st.session_state.history, new_data], ignore_index=True)

    # st.session_state.history=pd.concat([st.session_state.history[st.session_state.history["日付"]!=current_date],new_data],ignore_index=True)
    st.session_state.history = pd.concat(
    [st.session_state.history[st.session_state.history["日付"] != current_date], new_data],
    ignore_index=True
)
    st.session_state.history.to_csv(data_file,index=False)

    st.line_chart(st.session_state.history.set_index("日付")["合計"])


    
    # if health1 =="良い":
    #     health1_number=100
    # if health1=="普通":
    #     health1_number=50
    # if health1=="悪い":
    #     health1_number=-50
    # if health=="わからない":
    #     health1_number=0

    # if health=="良い":
    #     health_number=100
    # if health=="普通":
    #     health_number=50
    # if health=="悪い":
    #     health_number=-50
    # if health=="わからない":
    #     health_number=0
    # if weather=="晴れ":
    #     weather_number=100
    # if weather=="くもり":
    #     weather_number=50
    # if weather=="雨":
    #     weather_number=0


    # df=pd.DataFrame({
    #     "天気":[weather_number],
    #     "体調":[health1_number],
    #     "気分":[health_number],
    #     "合計":[weather_number+health1_number+health_number]
    # })
    # st.line_chart()

    # st.write(df)

    



    # if weather=="くもり" or "晴れ" or "雨" and health=="わからない":
    #     img=Image.open(r"C:\Users\nagis\OneDrive\デスクトップ\streamlit\父ジョンレノン.jpg")
    #     st.subheader("自分の気持ちが分からないときは、俺に聴いてみな") 
    #     st.image(img,use_column_width=True)      


# for i in range(100):
#     latest_iteration.text(f"Iteration{i+1}")
#     bar.progress(i+1)
#     time.sleep(0.1)
# "Done!!!!"

# left_column,right_column=st.columns(2)
# button=left_column.button("右からに文字を表示")
# if button:
#     right_column.write("ここは右カラム")

# expander=st.expander("問い合わせ")
# expander.write("問い合わせ内容を書く")


# text = st.text_input("あなたの趣味を教えてください")

# "あなたの趣味は",text,"です"

# condition=st.slider("あなたの今の調子は？",0,100,50)
# "コンディション；",condition

# if st.checkbox("Show Image"):
#     img=Image.open(r"C:\Users\nagis\OneDrive\デスクトップ\streamlit\DSC00761.JPG")
#     st.image(img,caption="keshiki",use_column_width=True)

