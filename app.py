import math
import random
import time

import streamlit as st

from question_bank import QUESTION_BANK


# =========================================================
# 頁面設定
# =========================================================
st.set_page_config(
    page_title="小二數學趣味挑戰賽",
    page_icon="🧮",
    layout="centered"
)


ENCOURAGEMENTS = [
    "你完成了整個挑戰，真的很厲害！",
    "看見你的專注和堅持了，你很棒！",
    "答錯不要緊，每次嘗試都會令你進步！",
    "學習不只是看分數，願意努力同樣值得欣賞！",
    "你認真完成每一題，真的很有責任感！"
]


DIFFICULTY_DESCRIPTIONS = {
    "簡單": "基本乘除法、加減法、時間、方向及生活數學。",
    "中級": "混合運算、有餘數除法、時間及兩步應用題。",
    "困難": "多步運算、跨時段計算、月曆、方向及綜合應用題。"
}


# =========================================================
# Session State初始化
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "setup"


# =========================================================
# 遊戲函數
# =========================================================
def clear_answer_widgets():
    """清除上一局的答案元件。"""
    prefixes = ("answer_", "submit_", "next_")

    keys_to_delete = [
        key
        for key in list(st.session_state.keys())
        if key.startswith(prefixes)
    ]

    for key in keys_to_delete:
        del st.session_state[key]


def create_question_set(difficulty, question_count):
    """抽取題目並隨機排列選項。"""
    source_questions = QUESTION_BANK[difficulty]

    selected = random.sample(
        source_questions,
        question_count
    )

    game_questions = []

    for item in selected:
        options = item["options"].copy()
        random.shuffle(options)

        game_questions.append({
            "q": item["q"],
            "options": options,
            "a": item["a"]
        })

    return game_questions


def set_new_deadline():
    """設定目前題目的截止時間。"""
    if st.session_state.timer_enabled:
        st.session_state.deadline = (
            time.time()
            + st.session_state.seconds_per_question
        )
    else:
        st.session_state.deadline = None


def start_game(
    difficulty,
    question_count,
    timer_enabled,
    seconds_per_question
):
    """開始新遊戲。"""
    clear_answer_widgets()

    st.session_state.difficulty = difficulty
    st.session_state.question_count = question_count
    st.session_state.timer_enabled = timer_enabled
    st.session_state.seconds_per_question = (
        seconds_per_question
    )

    st.session_state.selected_questions = (
        create_question_set(
            difficulty,
            question_count
        )
    )

    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.feedback_type = None
    st.session_state.feedback_message = ""
    st.session_state.answer_records = []
    st.session_state.final_encouragement = ""
    st.session_state.page = "quiz"

    set_new_deadline()


def submit_answer(
    selected_answer=None,
    timed_out=False
):
    """批改答案。"""
    if st.session_state.answered:
        return

    question = st.session_state.selected_questions[
        st.session_state.current_index
    ]

    # 玩家按提交時，再次檢查是否已逾時
    if (
        st.session_state.timer_enabled
        and st.session_state.deadline is not None
        and time.time() >= st.session_state.deadline
    ):
        timed_out = True

    st.session_state.answered = True

    if timed_out:
        is_correct = False
        result = "逾時"

        st.session_state.feedback_type = "warning"
        st.session_state.feedback_message = (
            f"⏰ 時間到！正確答案係「{question['a']}」。"
        )

    elif selected_answer == question["a"]:
        is_correct = True
        result = "正確"

        st.session_state.score += 1
        st.session_state.feedback_type = "success"
        st.session_state.feedback_message = (
            "答啱咗！好叻呀！🎉"
        )

    else:
        is_correct = False
        result = "錯誤"

        st.session_state.feedback_type = "error"
        st.session_state.feedback_message = (
            f"唔好灰心，正確答案係「{question['a']}」。"
            "下次繼續努力！💪"
        )

    st.session_state.answer_records.append({
        "question": question["q"],
        "selected_answer": (
            selected_answer
            if selected_answer is not None
            else "沒有作答"
        ),
        "correct_answer": question["a"],
        "is_correct": is_correct,
        "result": result
    })


def next_question():
    """前往下一題或成績頁。"""
    total = len(
        st.session_state.selected_questions
    )

    is_last_question = (
        st.session_state.current_index >= total - 1
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
    """返回遊戲設定頁。"""
    clear_answer_widgets()

    game_keys = [
        "difficulty",
        "question_count",
        "timer_enabled",
        "seconds_per_question",
        "selected_questions",
        "current_index",
        "score",
        "answered",
        "feedback_type",
        "feedback_message",
        "answer_records",
        "deadline",
        "final_encouragement"
    ]

    for key in game_keys:
        st.session_state.pop(key, None)

    st.session_state.page = "setup"


# =========================================================
# 標題
# =========================================================
st.title("🧮 小二數學趣味挑戰賽")

st.write(
    "專為小二學生準備嘅互動數學溫習遊戲～"
)


# =========================================================
# 遊戲設定頁
# =========================================================
if st.session_state.page == "setup":
    st.subheader("⚙️ 遊戲設定")

    difficulty = st.radio(
        "請選擇難度：",
        ["簡單", "中級", "困難"],
        horizontal=True
    )

    st.info(
        DIFFICULTY_DESCRIPTIONS[difficulty]
    )

    question_count = st.slider(
        "每次挑戰題數：",
        min_value=5,
        max_value=50,
        value=10,
        step=5
    )

    timer_enabled = st.toggle(
        "開啟每題倒數計時",
        value=True
    )

    if timer_enabled:
        seconds_per_question = st.slider(
            "每題作答時間：",
            min_value=10,
            max_value=120,
            value=30,
            step=5,
            format="%d 秒"
        )
    else:
        seconds_per_question = 30
        st.caption("本局不限作答時間。")

    st.write(
        f"「{difficulty}」題庫共有 "
        f"**{len(QUESTION_BANK[difficulty])}題**。"
    )

    st.write(
        f"本次挑戰會隨機抽出 "
        f"**{question_count}題**，"
        "答案次序亦會隨機排列。"
    )

    if st.button(
        "🚀 開始挑戰",
        type="primary",
        use_container_width=True
    ):
        start_game(
            difficulty=difficulty,
            question_count=question_count,
            timer_enabled=timer_enabled,
            seconds_per_question=seconds_per_question
        )
        st.rerun()


# =========================================================
# 答題頁
# =========================================================
elif st.session_state.page == "quiz":

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
        total = len(questions)

        progress_value = (idx + 1) / total

        st.progress(
            progress_value,
            text=f"挑戰進度：第 {idx + 1} 題／共 {total} 題"
        )

        information_col1, information_col2 = (
            st.columns(2)
        )

        with information_col1:
            st.write(
                f"難度："
                f"**{st.session_state.difficulty}**"
            )

        with information_col2:
            st.write(
                f"目前得分："
                f"**{st.session_state.score}分**"
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
                    f"⏰ 剩餘時間：{remaining}秒"
                )
            elif remaining <= 10:
                st.warning(
                    f"⏰ 剩餘時間：{remaining}秒"
                )
            else:
                st.info(
                    f"⏰ 剩餘時間：{remaining}秒"
                )

            if remaining <= 0:
                submit_answer(timed_out=True)
                st.rerun()

        elif not st.session_state.timer_enabled:
            st.info("⏳ 本局不限作答時間")

        # ---------------------------------------------
        # 顯示題目
        # ---------------------------------------------
        st.subheader(
            f"第 {idx + 1} 題"
        )

        st.markdown(
            f"### {question['q']}"
        )

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
                use_container_width=True,
                key=f"submit_{idx}"
            ):
                if selected_answer is None:
                    st.warning(
                        "請先選擇一個答案。"
                    )
                else:
                    submit_answer(
                        selected_answer=selected_answer
                    )
                    st.rerun()

        # ---------------------------------------------
        # 答題結果
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

            if idx < total - 1:
                button_text = "下一題 ➡️"
            else:
                button_text = "查看成績 🏆"

            if st.button(
                button_text,
                type="primary",
                use_container_width=True,
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
        f"{score}／{total}題！"
    )

    if percentage == 100:
        st.subheader(
            "🏆 滿分！你係數學小天才！"
        )
    elif percentage >= 80:
        st.subheader(
            "🌟 成績非常好！"
        )
    elif percentage >= 60:
        st.subheader(
            "👍 表現不錯，繼續努力！"
        )
    else:
        st.subheader(
            "💪 再練習多一次，一定會進步！"
        )

    st.info(
        st.session_state.final_encouragement
    )

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric(
            "答啱題數",
            f"{score}／{total}"
        )

    with metric_col2:
        st.metric(
            "正確率",
            f"{percentage}%"
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
            f"計時設定："
            f"**每題 "
            f"{st.session_state.seconds_per_question}秒**"
        )
    else:
        st.write(
            "計時設定：**不限時間**"
        )

    # ---------------------------------------------
    # 答題紀錄
    # ---------------------------------------------
    with st.expander(
        "📝 查看答題紀錄",
        expanded=False
    ):
        for number, record in enumerate(
            st.session_state.answer_records,
            start=1
        ):
            if record["is_correct"]:
                icon = "✅"
            elif record["result"] == "逾時":
                icon = "⏰"
            else:
                icon = "❌"

            st.markdown(
                f"#### {icon} 第{number}題"
            )

            st.write(
                record["question"]
            )

            st.write(
                f"你的答案："
                f"**{record['selected_answer']}**"
            )

            st.write(
                f"正確答案："
                f"**{record['correct_answer']}**"
            )

            if number < len(
                st.session_state.answer_records
            ):
                st.divider()

    # ---------------------------------------------
    # 再玩一次
    # ---------------------------------------------
    button_col1, button_col2 = st.columns(2)

    with button_col1:
        if st.button(
            "🔄 相同設定再玩",
            use_container_width=True
        ):
            start_game(
                difficulty=(
                    st.session_state.difficulty
                ),
                question_count=(
                    st.session_state.question_count
                ),
                timer_enabled=(
                    st.session_state.timer_enabled
                ),
                seconds_per_question=(
                    st.session_state.seconds_per_question
                )
            )
            st.rerun()

    with button_col2:
        if st.button(
            "⚙️ 更改設定",
            use_container_width=True
        ):
            reset_game()
            st.rerun()


# =========================================================
# 無效頁面保護
# =========================================================
else:
    st.error(
        "頁面狀態出現錯誤，請返回遊戲設定。"
    )

    if st.button(
        "返回遊戲設定",
        use_container_width=True
    ):
        reset_game()
        st.rerun()
