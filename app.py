import random
import math
import time

import streamlit as st


# =========================================================
# 頁面設定
# =========================================================
st.set_page_config(
    page_title="小二數學趣味挑戰賽",
    page_icon="🧮",
    layout="centered"
)

QUESTIONS_PER_GAME = 20


# =========================================================
# 題庫
# =========================================================
QUESTION_BANK = {
    "簡單": [
        {
            "q": "丸丸有硬幣24個，每3個整齊疊起，可分成幾疊？",
            "options": ["6", "7", "8", "9"],
            "a": "8"
        },
        {
            "q": "把20隻雞腿每4隻放一袋，可分成幾袋？",
            "options": ["4", "5", "6", "8"],
            "a": "5"
        },
        {
            "q": "計算：56 ÷ 7 = ?",
            "options": ["6", "7", "8", "9"],
            "a": "8"
        },
            {"q": "3個蘋果夾埋20蚊，買6個要幾多錢？", "a": "40"},
        {
        },
        {
            "q": "計算：7 × 7 = ?",
            "options": ["42", "47", "49", "56"],
            "a": "49"
        },
        {
            "q": "一打雞蛋有12隻，買2打雞蛋共有多少隻？",
            "options": ["12", "14", "20", "24"],
            "a": "24"
        },
        {
            "q": "2024年是閏年，二月共有多少日？",
            "options": ["28", "29", "30", "31"],
            "a": "29"
        }
    ],

    "普通": [
        {
            "q": "計算：190 + 429 - 250 = ?",
            "options": ["359", "369", "379", "389"],
            "a": "369"
        },
        {
            "q": "計算：157 + 26 = ?",
            "options": ["173", "183", "193", "203"],
            "a": "183"
        },
        {
            "q": "計算：9 × 6 = ?",
            "options": ["45", "48", "54", "63"],
            "a": "54"
        },
        {
            "q": "計算：63 ÷ 7 = ?",
            "options": ["7", "8", "9", "10"],
            "a": "9"
        },
        {
            "q": "現在是下午3時45分，30分鐘後是幾時？",
            "options": [
                "下午4時05分",
                "下午4時15分",
                "下午4時25分",
                "下午4時30分"
            ],
            "a": "下午4時15分"
        },
        {
            "q": "小多面向西方，右轉一個直角後，她的後面是什麼方向？",
            "options": ["東", "南", "西", "北"],
            "a": "南"
        }
    ],

    "困難": [
        {
            "q": "計算：248 + 376 - 159 = ?",
            "options": ["455", "465", "475", "485"],
            "a": "465"
        },
        {
            "q": "計算：72 ÷ 8 × 6 = ?",
            "options": ["48", "54", "56", "64"],
            "a": "54"
        },
        {
            "q": "每盒有24枝鉛筆，3盒平均分給8位小朋友，每人有多少枝？",
            "options": ["6", "8", "9", "12"],
            "a": "9"
        },
        {
            "q": "電影在下午5時35分開始，50分鐘後結束。電影幾時結束？",
            "options": [
                "下午6時15分",
                "下午6時20分",
                "下午6時25分",
                "下午6時35分"
            ],
            "a": "下午6時25分"
        },
        {
            "q": "一個長方形長12厘米、闊7厘米，它的周界是多少厘米？",
            "options": ["19", "24", "38", "84"],
            "a": "38"
        },
        {
            "q": "豆豆有100元，買了一本28元的書和一盒彩筆35元，還剩多少元？",
            "options": ["27", "37", "47", "63"],
            "a": "37"
        }
    ]
}


# =========================================================
# 鼓勵說話
# =========================================================
ENCOURAGEMENTS = [
    "你今天一口氣完成了這麼多題目，真的超級厲害！",
    "看見你的專注和堅持了，你很棒！",
    "學習不只是看分數，更重要的是願意努力吸收知識。",
    "每一題你都有認真回答，真的很有責任感呢！",
    "答錯也不要緊，每次嘗試都會令你進步！"
]


DIFFICULTY_DESCRIPTIONS = {
    "簡單": "適合練習基本乘除法、閏年及簡單生活數學。",
    "普通": "包括三位數運算、乘除法、時間及方向題。",
    "困難": "包括混合運算、周界及兩步應用題。"
}


# =========================================================
# Session State 初始化
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "setup"


# =========================================================
# 輔助函數
# =========================================================
def clear_answer_widgets():
    """清除上一局留下的選擇題答案。"""
    answer_keys = [
        key
        for key in list(st.session_state.keys())
        if key.startswith("answer_")
    ]

    for key in answer_keys:
        del st.session_state[key]


def create_question_set(difficulty):
    """隨機抽取題目，並隨機排列答案選項。"""
    question_bank = QUESTION_BANK[difficulty]

    if len(question_bank) < QUESTIONS_PER_GAME:
        raise ValueError(
            f"{difficulty}題庫只有 {len(question_bank)} 題，"
            f"不足以抽取 {QUESTIONS_PER_GAME} 題。"
        )

    chosen_questions = random.sample(
        question_bank,
        QUESTIONS_PER_GAME
    )

    game_questions = []

    for item in chosen_questions:
        shuffled_options = item["options"].copy()
        random.shuffle(shuffled_options)

        game_questions.append(
            {
                "q": item["q"],
                "options": shuffled_options,
                "a": item["a"]
            }
        )

    return game_questions


def set_new_deadline():
    """為目前題目設定截止時間。"""
    if st.session_state.timer_enabled:
        st.session_state.deadline = (
            time.time()
            + st.session_state.seconds_per_question
        )
    else:
        st.session_state.deadline = None


def start_game(
    difficulty,
    timer_enabled,
    seconds_per_question
):
    """開始一局新遊戲。"""
    clear_answer_widgets()

    st.session_state.difficulty = difficulty
    st.session_state.timer_enabled = timer_enabled
    st.session_state.seconds_per_question = (
        seconds_per_question
    )

    st.session_state.selected_questions = (
        create_question_set(difficulty)
    )

    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.feedback_type = None
    st.session_state.feedback_message = ""
    st.session_state.final_encouragement = ""
    st.session_state.page = "quiz"

    set_new_deadline()


def submit_answer(
    selected_answer=None,
    timed_out=False
):
    """批改目前題目。"""
    if st.session_state.answered:
        return

    question = st.session_state.selected_questions[
        st.session_state.current_index
    ]

    # 玩家按下提交時，再檢查一次是否已經逾時
    if (
        st.session_state.timer_enabled
        and st.session_state.deadline is not None
        and time.time() >= st.session_state.deadline
    ):
        timed_out = True

    st.session_state.answered = True

    if timed_out:
        st.session_state.feedback_type = "warning"
        st.session_state.feedback_message = (
            f"⏰ 時間到！正確答案係「{question['a']}」。"
        )

    elif selected_answer == question["a"]:
        st.session_state.score += 1
        st.session_state.feedback_type = "success"
        st.session_state.feedback_message = (
            "答啱咗！好叻呀！🎉"
        )

    else:
        st.session_state.feedback_type = "error"
        st.session_state.feedback_message = (
            f"唔好灰心，正確答案係「{question['a']}」。"
            "下次繼續努力！💪"
        )


def next_question():
    """進入下一題，或者完成遊戲。"""
    total_questions = len(
        st.session_state.selected_questions
    )

    is_last_question = (
        st.session_state.current_index
        >= total_questions - 1
    )

    if is_last_question:
        st.session_state.final_encouragement = (
            random.choice(ENCOURAGEMENTS)
        )
        st.session_state.page = "result"
        return

    st.session_state.current_index += 1
    st.session_state.answered = False
    st.session_state.feedback_type = None
    st.session_state.feedback_message = ""

    set_new_deadline()


def reset_game():
    """清除遊戲資料，返回設定頁。"""
    clear_answer_widgets()

    game_keys = [
        "difficulty",
        "timer_enabled",
        "seconds_per_question",
        "selected_questions",
        "current_index",
        "score",
        "answered",
        "feedback_type",
        "feedback_message",
        "deadline",
        "final_encouragement"
    ]

    for key in game_keys:
        st.session_state.pop(key, None)

    st.session_state.page = "setup"


# =========================================================
# 頁面標題
# =========================================================
st.title("🧮 小二數學趣味挑戰賽")

st.write(
    "家長好！呢度係專為小朋友準備嘅互動溫習網頁～"
)


# =========================================================
# 遊戲設定頁
# =========================================================
if st.session_state.page == "setup":
    st.subheader("⚙️ 遊戲設定")

    difficulty = st.radio(
        "請選擇難度：",
        ["簡單", "普通", "困難"],
        horizontal=True
    )

    st.info(
        DIFFICULTY_DESCRIPTIONS[difficulty]
    )

    timer_enabled = st.toggle(
        "開啟每題倒數計時",
        value=True
    )

    if timer_enabled:
        seconds_per_question = st.slider(
            "每題作答時間：",
            min_value=10,
            max_value=60,
            value=30,
            step=5,
            format="%d 秒"
        )
    else:
        seconds_per_question = 30
        st.caption("不限時間，可以慢慢思考。")

    st.write(
        f"每次挑戰會隨機抽出 "
        f"**{QUESTIONS_PER_GAME} 題**，"
        "答案次序亦會隨機排列。"
    )

    if st.button(
        "🚀 開始挑戰",
        type="primary",
        width="stretch"
    ):
        start_game(
            difficulty=difficulty,
            timer_enabled=timer_enabled,
            seconds_per_question=seconds_per_question
        )
        st.rerun()


# =========================================================
# 答題頁
# =========================================================
elif st.session_state.page == "quiz":

    # 只在開啟計時及尚未作答時，每秒更新
    refresh_interval = (
        1
        if (
            st.session_state.timer_enabled
            and not st.session_state.answered
        )
        else None
    )

    @st.fragment(run_every=refresh_interval)
    def show_question():
        idx = st.session_state.current_index
        questions = st.session_state.selected_questions
        question = questions[idx]
        total_questions = len(questions)

        # ---------------------------------------------
        # 顯示進度及分數
        # ---------------------------------------------
        progress_value = (idx + 1) / total_questions

        st.progress(
            progress_value,
            text=f"挑戰進度：第 {idx + 1} 題"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"**第 {idx + 1} 題／"
                f"共 {total_questions} 題**"
            )

        with col2:
            st.write(
                f"目前得分："
                f"**{st.session_state.score} 分**"
            )

        # ---------------------------------------------
        # 倒數計時
        # ---------------------------------------------
        if (
            st.session_state.timer_enabled
            and not st.session_state.answered
        ):
            remaining = max(
                0,
                math.ceil(
                    st.session_state.deadline
                    - time.time()
                )
            )

            if remaining <= 5:
                st.error(
                    f"⏰ 剩餘時間：{remaining} 秒"
                )
            elif remaining <= 10:
                st.warning(
                    f"⏰ 剩餘時間：{remaining} 秒"
                )
            else:
                st.info(
                    f"⏰ 剩餘時間：{remaining} 秒"
                )

            # 時間到，自動當作答錯
            if remaining <= 0:
                submit_answer(timed_out=True)

                # 完整重新執行，鎖定答案及停止倒數
                st.rerun()

        elif not st.session_state.timer_enabled:
            st.info("⏳ 本局不限作答時間")

        # ---------------------------------------------
        # 顯示題目及選項
        # ---------------------------------------------
        st.subheader(question["q"])

        answer_key = f"answer_{idx}"

        selected_answer = st.radio(
            "請選擇答案：",
            question["options"],
            index=None,
            key=answer_key,
            disabled=st.session_state.answered
        )

        # ---------------------------------------------
        # 提交答案
        # ---------------------------------------------
        if not st.session_state.answered:
            if st.button(
                "提交答案",
                type="primary",
                width="stretch",
                key=f"submit_{idx}"
            ):
                if selected_answer is None:
                    st.warning("請先選擇一個答案。")
                else:
                    submit_answer(
                        selected_answer=selected_answer
                    )
                    st.rerun()

        # ---------------------------------------------
        # 顯示答題結果
        # ---------------------------------------------
        if st.session_state.answered:
            feedback_type = (
                st.session_state.feedback_type
            )

            message = (
                st.session_state.feedback_message
            )

            if feedback_type == "success":
                st.success(message)

            elif feedback_type == "warning":
                st.warning(message)

            else:
                st.error(message)

            if idx < total_questions - 1:
                button_text = "下一題 ➡️"
            else:
                button_text = "查看成績 🏆"

            if st.button(
                button_text,
                type="primary",
                width="stretch",
                key=f"next_{idx}"
            ):
                next_question()
                st.rerun()

    show_question()


# =========================================================
# 成績頁
# =========================================================
elif st.session_state.page == "result":
    score = st.session_state.score
    total = len(
        st.session_state.selected_questions
    )

    percentage = round(
        score / total * 100
    )

    st.balloons()

    st.success(
        f"挑戰結束！你一共答啱咗 "
        f"{score}／{total} 題！"
    )

    if score == total:
        st.subheader(
            "🏆 滿分！你係數學小天才！"
        )

    elif score >= 3:
        st.subheader(
            "🌟 成績好好，繼續努力！"
        )

    else:
        st.subheader(
            "💪 再練習多一次，一定會進步！"
        )

    st.info(
        st.session_state.final_encouragement
    )

    # ---------------------------------------------
    # 成績資料
    # ---------------------------------------------
    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric(
            label="答啱題數",
            value=f"{score}／{total}"
        )

    with metric_col2:
        st.metric(
            label="正確率",
            value=f"{percentage}%"
        )

    st.progress(
        score / total,
        text=f"正確率：{percentage}%"
    )

    st.write(
        f"挑戰難度："
        f"**{st.session_state.difficulty}**"
    )

    if st.session_state.timer_enabled:
        st.write(
            "計時設定："
            f"**每題 "
            f"{st.session_state.seconds_per_question} 秒**"
        )
    else:
        st.write(
            "計時設定：**不限時間**"
        )

    # ---------------------------------------------
    # 再玩或更改設定
    # ---------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔄 相同設定再玩",
            width="stretch"
        ):
            start_game(
                difficulty=(
                    st.session_state.difficulty
                ),
                timer_enabled=(
                    st.session_state.timer_enabled
                ),
                seconds_per_question=(
                    st.session_state.seconds_per_question
                )
            )
            st.rerun()

    with col2:
        if st.button(
            "⚙️ 更改設定",
            width="stretch"
        ):
            reset_game()
            st.rerun()


# =========================================================
# 無效頁面保護
# =========================================================
else:
    st.error("頁面狀態出現錯誤，請返回遊戲設定。")

    if st.button(
        "返回遊戲設定",
        width="stretch"
    ):
        reset_game()
        st.rerun()
