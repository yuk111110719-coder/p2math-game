import random
import math
import streamlit as st

# 初始化題庫（包含難度分類）
if "question_bank" not in st.session_state:
    st.session_state.question_bank = [
        {"q": "丸丸有硬幣24個，每3個整齊疊起，可分成幾疊？", "a": "8", "difficulty": "中等"},
        {"q": "把20隻雞腿每4隻放一袋，可分成幾袋？", "a": "5", "difficulty": "簡單"},
        {"q": "計算：190 + 429 - 250 = ?", "a": "369", "difficulty": "困難"},
        {"q": "計算：56 ÷ 7 = ?", "a": "8", "difficulty": "簡單"},
        {"q": "家琪面向西方，他右轉一個直角後，他的後面是什麼方？", "a": "南", "difficulty": "中等"},
        {"q": "今年是閏年，二月共有多少日？", "a": "29", "difficulty": "中等"},
        {"q": "現在是3時59分，1分鐘後是幾時？（只需輸入數字）", "a": "4", "difficulty": "簡單"},
        {"q": "計算：7 x 7 = ?", "a": "49", "difficulty": "簡單"},
        {"q": "一打雞蛋有12隻，買2打雞蛋共有多少隻？", "a": "24", "difficulty": "簡單"},
        {"q": "計算：157 + 26 = ?", "a": "183", "difficulty": "中等"},
        {"q": "一本故事書有85頁，小華看了38頁，仲有幾多頁未睇？", "a": "47", "difficulty": "中等"},
        {"q": "學校有5行學生，每行有8人，總共有幾多名學生？", "a": "40", "difficulty": "簡單"},
        {"q": "豆豆有50蚊，買筆用咗15蚊，買筆記簿用咗12蚊，仲淨低幾多蚊？", "a": "23", "difficulty": "困難"},
        {"q": "時鐘嘅長針係指住數字12，短針指住數字4，依家係幾點？（只需輸入數字）", "a": "4", "difficulty": "簡單"},
        {"q": "計算：82 - (25 + 17) = ?", "a": "40", "difficulty": "困難"},
        {"q": "一個正方形有幾多條邊？", "a": "4", "difficulty": "簡單"},
        {"q": "把36粒糖果平分給6個人，每人可以分到幾粒？", "a": "6", "difficulty": "簡單"},
        {"q": "星期三嘅後日係星期幾？（請輸入中文，如：星期五）", "a": "星期五", "difficulty": "中等"},
        {"q": "計算：9 x 8 - 12 = ?", "a": "60", "difficulty": "困難"},
        {"q": "停車場入面原本有15架車，走咗7架，之後又開入嚟9架，依家有幾多架車？", "a": "17", "difficulty": "困難"}
    ]

def create_question_set(difficulty):
    # 根據難度篩選題庫
    if difficulty == "全部":
        pool = st.session_state.question_bank
    else:
        pool = [q for q in st.session_state.question_bank if q.get("difficulty") == difficulty]
    
    # 若該難度沒有題目，回退到全部題庫
    if not pool:
        pool = st.session_state.question_bank
        
    # 安全防呆：取目標數量與實際題庫數的較小值，避免 ValueError 崩潰
    target_count = min(20, len(pool))
    
    selected = random.sample(pool, target_count)
    
    # 為每一題隨機打亂答案選項（若有選項需求）
    return selected

def start_game(difficulty, timer_enabled, seconds_per_question):
    st.session_state.difficulty = difficulty
    st.session_state.timer_enabled = timer_enabled
    st.session_state.seconds_per_question = seconds_per_question
    st.session_state.selected_questions = create_question_set(difficulty)
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.game_started = True
    st.session_state.game_over = False

# 初始化遊戲狀態
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False

encouragements = [
    "你今天一口氣完成了這麼多題目，真的超級厲害！",
    "看見你的專注和堅持了，你很棒！",
    "學習不只是看分數，更是看你有否努力吸收知識。",
    "每一題你都有回答，這證明了你平時的用功，真的很有責任感呢！",
    "每一道題目都是一個學習的機會，你願意認真去想、去寫，就是一個百分之百的進步。"
]

st.title("🧮 小二數學趣味挑戰賽")
st.write("家長好！歡迎黎到小二數學訓練營，請設定下方選項後開始挑戰！")

if not st.session_state.game_started:
    st.subheader("⚙️ 挑戰設定")
    difficulty = st.selectbox("選擇難度級別：", ["全部", "簡單", "中等", "困難"])
    timer_enabled = st.checkbox("開啟限時計時器", value=False)
    seconds_per_question = st.slider("每題作答秒數：", 5, 30, 15)
    
    if st.button("🚀 開始挑戰", type="primary"):
        start_game(difficulty, timer_enabled, seconds_per_question)
        st.rerun()

else:
    if not st.session_state.game_over:
        total_questions = len(st.session_state.selected_questions)
        idx = st.session_state.current_index
        q_item = st.session_state.selected_questions[idx]
        
        st.subheader(f"第 {idx + 1} 題 / 共 {total_questions} 題 (難度：{q_item.get('difficulty', '綜合')})")
        st.markdown(f"**{q_item['q']}**")
        
        with st.form(f"form_{idx}"):
            user_ans = st.text_input("請輸入你的答案：").strip()
            submitted = st.form_submit_button("提交答案")
            
            if submitted:
                if user_ans == q_item['a']:
                    st.success("答啱咗！好叻女呀！🎉")
                    st.session_state.score += 1
                else:
                    st.error(f"唔好灰心，正確答案係 {q_item['a']}，下次繼續努力！💪")
                
                if st.session_state.current_index < total_questions - 1:
                    st.session_state.current_index += 1
                    st.rerun()
                else:
                    st.session_state.game_over = True
                    st.rerun()
    else:
        total_questions = len(st.session_state.selected_questions)
        st.balloons()
        st.success(f"挑戰結束！你一共答啱咗 {st.session_state.score} / {total_questions} 題！")
        st.info(random.choice(encouragements))
        
        if st.button("🔄 重新設定並再次挑戰"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
