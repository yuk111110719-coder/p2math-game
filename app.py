import math
import random
import streamlit as st

# 題庫設定
if "question_bank" not in st.session_state:
    st.session_state.question_bank = [
        {"q": "丸丸有硬幣24個，每3個整齊疊起，可分成幾疊？", "a": "8"},
        {"q": "把20隻雞腿每4隻放一袋，可分成幾袋？", "a": "5"},
        {"q": "計算：190 + 429 - 250 = ?", "a": "369"},
        {"q": "計算：56 ÷ 7 = ?", "a": "8"},
        {"q": "家琪面向西方，他右轉一個直角後，他的後面是什麼方？", "a": "南"},
        {"q": "今年是閏年，二月共有多少日？", "a": "29"},
        {"q": "現在是3時59分，1分鐘後是幾時？", "a": "4"},
        {"q": "計算：7 x 7 = ?", "a": "49"},
        {"q": "一打雞蛋有12隻，買2打雞蛋共有多少隻？", "a": "24"},
        {"q": "計算：157 + 26 = ?", "a": "183"}
    ]
    st.session_state.selected_questions = random.sample(st.session_state.question_bank, 5)
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.game_over = False

encouragements = [
    "你今天一口氣完成了這麼多題目，真的超級厲害！",
    "看見你的專注和堅持了，你很棒!",
    "學習不只是看分數，更是看你有否努力吸收知識。",
    "每一題你都有回答，這證明了你平時的用功，真的很有責任感呢！"
]

st.title("🧮 小二數學趣味挑戰賽")
st.write("家長好！呢度係專為小朋友準備嘅互動溫習網頁～")

if not st.session_state.game_over:
    idx = st.session_state.current_index
    q_item = st.session_state.selected_questions[idx]
    
    st.subheader(f"第 {idx + 1} 題 / 共 5 題")
    st.markdown(f"**{q_item['q']}**")
    
    # 答題表單
    with st.form(f"form_{idx}"):
        user_ans = st.text_input("請輸入你的答案：").strip()
        submitted = st.form_submit_button("提交答案")
        
        if submitted:
            if user_ans == q_item['a']:
                st.success("答啱咗！好叻女呀！🎉")
                st.session_state.score += 1
            else:
                st.error(f"唔好灰心，正確答案係 {q_item['a']}，下次繼續努力！💪")
            
            # 進入下一題或結束
            if st.session_state.current_index < len(st.session_state.selected_questions) - 1:
                st.session_state.current_index += 1
                st.rerun()
            else:
                st.session_state.game_over = True
                st.rerun()
else:
    st.balloons()
    st.success(f"挑戰結束！你一共答啱咗 {st.session_state.score} / 5 題！")
    st.info(random.choice(encouragements))
    if st.button("再玩一次"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
