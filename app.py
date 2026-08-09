import random
import math
import streamlit as st

# 初始化題庫（包含難度分類）
if "question_bank" not in st.session_state:
    st.session_state.question_bank = [
        {"q": "丸丸有硬幣24個，每3個整齊疊起，可分成幾疊？", "a": "8", "difficulty": "中等"},
        {"q": "把20隻雞腿每4隻放一袋，可分成幾袋？", "a": "5", "difficulty": "簡單"},
        {"q": "190 + 429 - 250 = ?", "a": "369", "difficulty": "困難"},
        {"q": "56 ÷ 7 = ?", "a": "8", "difficulty": "簡單"},
        {"q": "家琪面向西方，他右轉一個直角後，他的前面是什麼方？", "a": "北", "difficulty": "中等","options": ["東", "南", "西", "北"]},
        {"q": "現在是3時59分，1分鐘後是幾時？（只需輸入數字）", "a": "4", "difficulty": "簡單"},
        {"q": "7 x 7 = ?", "a": "49", "difficulty": "簡單"},
        {"q": "一打雞蛋有12隻，買2打雞蛋共有多少隻？", "a": "24", "difficulty": "簡單"},
        {"q": "157 + 26 = ?", "a": "183", "difficulty": "中等"},
        {"q": "一本故事書有85頁，小華看了38頁，仲有幾多頁未睇？", "a": "47", "difficulty": "中等"},
        {"q": "學校有5行學生，每行有8人，總共有幾多名學生？", "a": "40", "difficulty": "簡單"},
        {"q": "豆豆有50蚊，買筆用咗15蚊，買筆記簿用咗12蚊，仲淨低幾多蚊？", "a": "23", "difficulty": "困難"},
        {"q": "時鐘嘅長針係指住數字12，短針指住數字4，依家係幾點？（只需輸入數字）", "a": "4", "difficulty": "簡單"},
        {"q": "82 - (25 + 17) = ?", "a": "40", "difficulty": "困難"},
        {"q": "一個正方形有幾多條邊？", "a": "4", "difficulty": "簡單"},
        {"q": "把36粒糖果平分給6個人，每人可以分到幾粒？", "a": "6", "difficulty": "簡單"},
        {"q": "星期三嘅後日係星期幾？", "a": "星期五", "difficulty": "中等","options": ["星期一", "星期五", "星期六", "星期日"]},
        {"q": "9 x 8 - 12 = ?", "a": "60", "difficulty": "困難"},
        {"q": "停車場入面原本有15部車，7部車剛離開，之後又有9部駛進停車場，現在有幾多部車？", "a": "17", "difficulty": "困難"},
        {"q": "5 x 3 = ?", "a": "15", "difficulty": "簡單"},
        {"q": "8 + 9 = ?", "a": "17", "difficulty": "簡單"},
        {"q": "12 - 4 = ?", "a": "8", "difficulty": "簡單"},
        {"q": "100 + 200 = ?", "a": "300", "difficulty": "簡單"},
        {"q": "一星期有多少天？", "a": "7", "difficulty": "簡單"},
        {"q": "4 x 2 = ?", "a": "8", "difficulty": "簡單"},
        {"q": "平年的一年共有多少天？", "a": "365", "difficulty": "簡單"},
        {"q": "1米等於多少厘米？", "a": "100", "difficulty": "簡單"},
        {"q": "三角形有幾多隻角？", "a": "3", "difficulty": "簡單"},
        {"q": "20 ÷ 4 = ?", "a": "5", "difficulty": "簡單"},
        {"q": "媽媽有10元，買了5元的糖果，還餘多少元？", "a": "5", "difficulty": "簡單"},
        {"q": "6 x 7 = ?", "a": "42", "difficulty": "簡單"},
        {"q": "一天有多少小時？", "a": "24", "difficulty": "簡單"},
        {"q": "3 x 9 = ?", "a": "27", "difficulty": "簡單"},
        {"q": "把24枝鉛筆平均分給3個人，每人得幾枝？", "a": "8", "difficulty": "簡單"},
        {"q": "15 + 15 = ?", "a": "30", "difficulty": "簡單"},
        {"q": "40 - 18 = ?", "a": "22", "difficulty": "簡單"},
        {"q": "8 x 8 = ?", "a": "64", "difficulty": "簡單"},
        {"q": "時鐘上的短針代表什麼？", "a": "時針", "difficulty": "中等","options": ["時針", "分針", "秒針"]},
        {"q": "9 x 0 = ?", "a": "0", "difficulty": "簡單"},
        {"q": "50 + 50 = ?", "a": "100", "difficulty": "簡單"},
        {"q": "一打雞蛋有幾隻？", "a": "12", "difficulty": "簡單"},
        {"q": "2 x 6 = ?", "a": "12", "difficulty": "簡單"},
        {"q": "12 x 1 = ?", "a": "12", "difficulty": "簡單"},
        {"q": "豆豆原本有11粒朱古力，分左俾爸爸2粒，分左俾媽媽2粒，分左俾姐姐2粒，她仲有幾多粒?", "a": "5", "difficulty": "簡單"},
        {"q": "星期二的前一日係星期幾？", "a": "星期一", "difficulty": "中等","options": ["日", "一", "三", "四"]},
        {"q": "4 x 5 + 10 = ?", "a": "30", "difficulty": "中等"},
        {"q": "一碟餃子有6隻，買了4碟共有多少隻？", "a": "24", "difficulty": "中等"},
        {"q": "如果今天是7月1日，一星期後是幾月幾日？", "a": "7月8日", "difficulty": "中等"},
        {"q": "現在是3時15分，1小時後是幾時幾分？", "a": "4時15分", "difficulty": "中等"},
        {"q": "一個橙售5元，買6個橙共付多少元？", "a": "30", "difficulty": "中等"},
        {"q": "四角柱體共有多少個面？", "a": "6", "difficulty": "中等"},
        {"q": "把45粒糖平均分給9個人，每人分到多少粒？", "a": "5", "difficulty": "中等"},
        {"q": "8 x 3 - 5 = ?", "a": "19", "difficulty": "中等"},
        {"q": "150 + 250 = ?", "a": "400", "difficulty": "中等"},
        {"q": "梓謙有20元，買一個8元的麵包，還餘多少元？", "a": "12", "difficulty": "中等"},
        {"q": "鐘面顯示11:45，20分鐘後是幾時幾分？", "a": "12時05分", "difficulty": "中等"},
        {"q": "10是2的多少倍？", "a": "5", "difficulty": "中等"},
        {"q": "一個長方形有幾條「對」邊？", "a": "2", "difficulty": "中等"},
        {"q": "300 + 400 - 100 = ?", "a": "600", "difficulty": "中等"},
        {"q": "如果☆+☆= 18，☆ = ?", "a": "9", "difficulty": "中等"},
        {"q": "25 ÷ 5 = ?", "a": "5", "difficulty": "中等"},
        {"q": "一束花有4朵紅花和5朵黃花，8束共有多少朵花？", "a": "72", "difficulty": "困難"},
        {"q": "一盒魚蛋、燒賣中，有5粒魚蛋和3粒燒賣，買4盒，共有多少粒燒賣？", "a": "12", "difficulty": "困難"},
        {"q": "現在是早上9時，下午2時，中間經過了多少小時？", "a": "5", "difficulty": "中等"},
        {"q": "2米50厘米即是多少厘米？", "a": "250", "difficulty": "中等"},
        {"q": "42除以7是多少？", "a": "6", "difficulty": "中等"},
        {"q": "一年裡，有多少個月大的月份？", "a": "7", "difficulty": "中等"},
        {"q": "7 x 4 = ?", "a": "28", "difficulty": "中等"},
        {"q": "爸爸有50元，買了兩本各12元的書，餘下多少元？", "a": "26", "difficulty": "中等"},
        {"q": "如果今天是星期一，3天後是星期幾？", "a": "星期四", "difficulty": "中等","options": ["二", "三", "四", "五"]},
        {"q": "56 ÷ 8 = ?", "a": "7", "difficulty": "中等"},
        {"q": "4個5相加的結果是多少？", "a": "20", "difficulty": "中等"},
        {"q": "什麼圖形的角比直角小？", "a": "銳角", "difficulty": "困難"},
        {"q": "9 x 8 + 18 = ?", "a": "90", "difficulty": "困難"},
        {"q": "梓朗買了3碟大甜圈，每碟6個，每個3元，共付多少元？", "a": "54", "difficulty": "困難"},
        {"q": "農場有5隻羊，雞的數目是羊的4倍，雞共有多少隻腳？", "a": "40", "difficulty": "困難"},
        {"q": "一個足球售135元，哥哥買了兩個，付出300元，找回多少元？", "a": "30", "difficulty": "困難"},
        {"q": "書架上有145本中文書，英文書比中文書多135本，歷史書比英文書少112本，歷史書有多少本？", "a": "168", "difficulty": "困難"},
        {"q": "小珊有62元，買魚蛋用了11元，買飲品用了7元，剩下多少元？", "a": "44", "difficulty": "困難"},
        {"q": "190 + 429 - 250 = ?", "a": "369", "difficulty": "困難"},
        {"q": "如果今天是4月28日，今日開始一連五天假期，假期的最後一天是幾月幾日？", "a": "5月2日", "difficulty": "困難","options": ["4月30日", "4月31日", "5月1日", "5月2日"]},
        {"q": "以下那一個是奇數，用2、8、12、5組成？", "a": "5", "difficulty": "困難"},
        {"q": "189 - 210 + 444 = ?", "a": "423", "difficulty": "困難"},
        {"q": "有60粒珠，每8粒串成一條手鏈，可串成多少條？餘下幾粒？", "a": "7條餘4粒", "difficulty": "困難","options": ["7條", "7條2粒", "7條4粒", "8條"]},
        {"q": "蛋糕店有345個蛋糕，賣出120個，又賣出102個，還餘多少個？", "a": "123", "difficulty": "困難"},
        {"q": "哥哥由9:05看電影，看到11:15，這場電影長多少小時多少分鐘？", "a": "2小時10分鐘", "difficulty": "困難","options": ["1小時30分鐘", "2小時5分鐘", "2小時10分鐘", "2小時45分鐘"]},
        {"q": "230 - 125 - 50 = ?", "a": "55", "difficulty": "困難"},
        {"q": "媽媽買了8件壽司每件5元，又買了5串蝦串，每串6元，共付多少元？", "a": "70", "difficulty": "困難"},
        {"q": "子傑有38張大相片，每頁相簿貼6張，需要多少頁相簿？", "a": "7", "difficulty": "困難"},
        {"q": "如果一個數除以7等於12，這個數是多少？", "a": "84", "difficulty": "困難"},
        {"q": "爸爸在上午9時上班，工作7小時30分後下班，下班時間是幾時幾分？", "a": "下午4時30分", "difficulty": "困難","options": ["下午2時30分", "下午3時30分", "下午4時", "下午4時30分"]},
        {"q": "56 ÷ 7 x 4 = ?", "a": "32", "difficulty": "困難"},
        {"q": "我有120元，弟弟有80元，合資買一個150元的蛋糕，餘下多少元？", "a": "50", "difficulty": "困難"},
        {"q": "一個四角錐體有多少個面？", "a": "5", "difficulty": "困難"},
        {"q": "(15 + 22) x 2 = ?", "a": "74", "difficulty": "困難"},
        {"q": "樂樂有40元，每天坐巴士來回學校，每程6元，最多可坐多少天？", "a": "3", "difficulty": "困難"},
        {"q": "時鐘顯示的時間比現在慢了10分鐘，如果現在是12:08，鐘面顯示什麼時間？", "a": "11:58", "difficulty": "困難","options": ["11:48", "11:56", "11:58", "12:02"]},
        {"q": "88 + 12 = 100，那麼 100 - 88 = ?", "a": "12", "difficulty": "中等"},
        {"q": "一個三位數，百位是6，十位是2，個位是7，讀作什麼？", "a": "六百二十七", "difficulty": "困難","options": ["六二七", "六百七十二", "七百二十六", "六百二十七"]},
        {"q": "4 x 4 x 4 = ?", "a": "64", "difficulty": "困難"},
        {"q": "Sam哥哥有100元，每本練習簿20元，最多可買多少本？", "a": "5", "difficulty": "簡單"},
        {"q": "(110 + 89 + 102) ÷ 3 = ?", "a": "101", "difficulty": "困難"},
        {"q": "一個長方形長度是10米，闊度是5米，周界是多少厘米？", "a": "3000", "difficulty": "困難"}
    ]

def create_question_set(difficulty, question_count):
    if difficulty == "全部":
        pool = st.session_state.question_bank
    else:
        pool = [q for q in st.session_state.question_bank if q.get("difficulty") == difficulty]
    
    if not pool:
        pool = st.session_state.question_bank
        
    target_count = min(question_count, len(pool))
    selected = random.sample(pool, target_count)
    return selected

def start_game(difficulty, timer_enabled, seconds_per_question, question_count):
    st.session_state.difficulty = difficulty
    st.session_state.timer_enabled = timer_enabled
    st.session_state.seconds_per_question = seconds_per_question
    st.session_state.question_count = question_count
    st.session_state.selected_questions = create_question_set(difficulty, question_count)
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.wrong_questions = []
    st.session_state.game_started = True
    st.session_state.game_over = False

# 初始化遊戲狀態
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "wrong_questions" not in st.session_state:
    st.session_state.wrong_questions = []

encouragements = [
    "你今天一口氣完成了這麼多題目，真的超級厲害！",
    "看見你的專注和堅持了，你很棒！",
    "學習不只是看分數，更是看你有否努力吸收知識。",
    "每一題你都有回答，這證明了你平時的用功，真的很有責任感呢！",
    "每一道題目都是一個學習的機會，你願意認真去想、去寫，就是一個百分之百的進步。"
]

# 根據遊戲是否開始來顯示畫面
if not st.session_state.game_started:
    # 顯示鸚鵡課堂圖片（位於標題上方）
    try:
        st.image("parrot_classroom.jpeg", use_container_width=True)
    except Exception:
        st.warning("（提示：找不到圖片檔案 `parrot_classroom.jpg`，請確保圖片檔與程式碼放在同一資料夾內！）")

    st.title("🧮 小二數學趣味挑戰賽")
    st.write("小朋友你好！歡迎黎到小二數學訓練營，設定下方選項後便開始挑戰啦！")

    st.subheader("⚙️ 挑戰設定")
    difficulty = st.selectbox("選擇難度級別：", ["全部", "簡單", "中等", "困難"])
    question_count = st.selectbox("選擇題目數量：", [10, 20, 30, 40], index=1)
    timer_enabled = st.checkbox("開啟限時計時器", value=False)
    seconds_per_question = st.slider("每題作答秒數：", 5, 30, 15)
    
    if st.button("🚀 開始挑戰", type="primary"):
        start_game(difficulty, timer_enabled, seconds_per_question, question_count)
        st.rerun()

else:
    if not st.session_state.game_over:
        total_questions = len(st.session_state.selected_questions)
        idx = st.session_state.current_index
        q_item = st.session_state.selected_questions[idx]
        
        st.subheader(f"第 {idx + 1} 題 / 共 {total_questions} 題 (難度：{q_item.get('difficulty', '綜合')})")
        st.markdown(f"**{q_item['q']}**")
        
      with st.form(f"form_{idx}"):
            # 檢查這題是否有設定選項
            if "options" in q_item and q_item["options"]:
                # 如果有選項，使用單選題
                user_ans = st.radio("請選擇正確答案：", q_item["options"], key=f"ans_radio_{idx}")
            else:
                # 如果沒有選項，維持原本的文字輸入
                user_ans = st.text_input("請輸入你的答案：", key=f"ans_text_{idx}").strip()
            
            submitted = st.form_submit_button("提交答案")
            
            if submitted:
                if user_ans == q_item['a']:
                    st.success("答啱咗！好叻女呀！🎉")
                    st.session_state.score += 1
                else:
                    st.error(f"唔好灰心，正確答案係 {q_item['a']}，下次繼續努力！💪")
                    if q_item not in st.session_state.wrong_questions:
                        st.session_state.wrong_questions.append(q_item)
                
                if st.session_state.current_index < total_questions - 1:
                    st.session_state.current_index += 1
                    st.rerun()
                else:
                    st.session_state.game_over = True
                    st.rerun()
    else:
        total_questions = len(st.session_state.selected_questions)
        score = st.session_state.score
        percentage = (score / total_questions) if total_questions > 0 else 0
        
        st.balloons()
        st.success(f"挑戰結束！你一共答啱咗 {score} / {total_questions} 題！")
        st.info(random.choice(encouragements))
        
        # 判斷是否達到 7 成（70%）以上
        if percentage >= 0.7:
            st.markdown("---")
            st.markdown("### 🎓 恭喜你達標 7 成以上！觀看小學士鸚鵡的慶祝影片：")
            try:
                st.video("parrot_celebration.mp4")
            except Exception:
                st.warning("（提示：找不到影片檔案 `parrot_celebration.mp4`，請確保影片檔與程式碼放在同一資料夾內！）")
        
        # 顯示錯題重溫與重新挑戰專區
        if st.session_state.wrong_questions:
            st.markdown("---")
            st.subheader("📝 錯題重溫與重新挑戰")
            st.write("這裏有你剛剛答錯的題目，再給自己一次學習和思考的機會，重新挑戰看看吧！💪")
            
            with st.form("retry_form"):
                retry_answers = {}
                for i, w_q in enumerate(st.session_state.wrong_questions):
                    st.markdown(f"**題目 {i+1}：** {w_q['q']}")
                    st.caption("💡 學習提示：請再讀一次題目，檢查計算過程或換算單位，試試看正確答案應該是多少？")
                    retry_answers[i] = st.text_input(f"重新輸入答案 #{i+1}", key=f"retry_input_{i}").strip()
                
                retry_submitted = st.form_submit_button("提交重試答案")
                
                if retry_submitted:
                    all_fixed = True
                    for i, w_q in enumerate(st.session_state.wrong_questions):
                        if retry_answers[i] == w_q['a']:
                            st.success(f"題目 {i+1} 訂正成功！太棒了！🎉")
                        else:
                            st.error(f"題目 {i+1} 答案仍不正確。正確答案應為：**{w_q['a']}**，下次加油！")
                            all_fixed = False
                    
                    if all_fixed:
                        st.balloons()
                        st.success("太厲害了！你把所有的錯題都成功訂正了！🌟")
        
        st.markdown("---")
        if st.button("🔄 重新設定並再次挑戰"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
            
