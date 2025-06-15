import streamlit as st
import random
import json
import pandas as pd
from datetime import datetime

# --- Стилізація
def set_custom_page_style():
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            background-color: #f0f4ff;
            font-family: 'Segoe UI', sans-serif;
        }
        .main {
            background: linear-gradient(145deg, #fefefe, #e1e9ff);
            border-radius: 10px;
            padding: 2rem;
        }
        h1 {
            color: #4b4bff;
            text-align: center;
        }
        .stButton > button {
            background-color: #4b4bff;
            color: white;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Конфігурація сторінки
st.set_page_config(
    page_title="💫 Streamlit Hub",
    page_icon="✨",
    layout="wide"
)
set_custom_page_style()

# --- Назва
st.title("💫 Мій супер Streamlit-застосунок")
st.markdown("### 👩‍💻 Створено з ❤️ на Python + Streamlit")

# --- Меню
st.sidebar.title("📚 Меню")
menu = st.sidebar.radio("Оберіть розділ:", [
    "🎮 Вгадай слово",
    "📔 Щоденник",
    "📚 Генератор історій (🔜)",
    "🧠 Вікторина (🔜)",
    "📊 Аналітика (🔜)"
])

# --- 1. Гра
if menu == "🎮 Вгадай слово":
    st.header("🎯 Гра: Вгадай слово")
    words = ["яблуко", "банан", "слива", "лимон", "груша"]
    if "secret_word" not in st.session_state:
        st.session_state.secret_word = random.choice(words)
        st.session_state.guesses = []
        st.session_state.finished = False

    if st.button("🔄 Нова гра"):
        st.session_state.secret_word = random.choice(words)
        st.session_state.guesses = []
        st.session_state.finished = False

    guess = st.text_input("Введи слово:").strip().lower()
    if st.button("🔍 Вгадати") and not st.session_state.finished:
        if guess:
            st.session_state.guesses.append(guess)
            if guess == st.session_state.secret_word:
                st.success(f"🎉 Вгадав(-ла) з {len(st.session_state.guesses)} спроби!")
                st.session_state.finished = True
                result = {
                    "слово": guess,
                    "здогадки": st.session_state.guesses,
                    "результат": "виграв",
                    "час": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            elif len(st.session_state.guesses) >= 5:
                st.error(f"💀 Програв(-ла). Слово: {st.session_state.secret_word}")
                st.session_state.finished = True
                result = {
                    "слово": st.session_state.secret_word,
                    "здогадки": st.session_state.guesses,
                    "результат": "програв",
                    "час": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                st.warning("❌ Ні, спробуй ще!")

            if st.session_state.finished:
                with open("game_results.json", "a", encoding="utf-8") as f:
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")

    if st.session_state.guesses:
        st.markdown("📜 **Твої здогадки:**")
        st.code(", ".join(st.session_state.guesses))

# --- 2. Щоденник
elif menu == "📔 Щоденник":
    st.header("📔 Мій щоденник")
    note = st.text_area("📝 Ваша нотатка", height=150)
    if st.button("💾 Зберегти нотатку"):
        if note.strip():
            entry = {
                "дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "текст": note.strip()
            }
            with open("notes.json", "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            st.success("✅ Запис збережено!")
        else:
            st.warning("Нотатка не може бути порожньою.")

    try:
        with open("notes.json", "r", encoding="utf-8") as f:
            entries = [json.loads(line) for line in f]
        st.subheader("📋 Останні 5 нотаток:")
        for n in reversed(entries[-5:]):
            st.markdown(f"**🕒 {n['дата']}**")
            st.info(n['текст'])
            st.markdown("---")
    except:
        st.info("Жодної нотатки ще не створено.")

# --- 3. Генератор історій
elif menu == "📚 Генератор історій (🔜)":
    st.header("📚 Генератор фантастичних історій")

    st.sidebar.subheader("🧑‍🎨 Додай свої варіанти:")
    chars = st.sidebar.text_area("Хто?", "програміст, кіт, учень").split(",")
    actions = st.sidebar.text_area("Що робив(-ла)?", "знайшов скарб, загубився, створив ШІ").split(",")
    places = st.sidebar.text_area("Де?", "у метро, в лісі, на уроці Python").split(",")

    def generate():
        return f"📘 Одного разу {random.choice(chars).strip()} {random.choice(actions).strip()} {random.choice(places).strip()}."

    if st.button("✨ Створити історію"):
        story = generate()
        st.success(story)

        result = {
            "дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "історії": [story]
        }
        with open("generated_stories.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

# --- 4. Вікторина
elif menu == "🧠 Вікторина (🔜)":
    st.header("🧠 Міні-вікторина")

    questions = [
        {"питання": "Яка команда виводить текст у Python?", "варіанти": ["show()", "echo()", "print()"], "правильна": "print()"},
        {"питання": "Яка функція визначає довжину?", "варіанти": ["size()", "len()", "length()"], "правильна": "len()"}
    ]

    if "q_idx" not in st.session_state:
        st.session_state.q_idx = 0
        st.session_state.balls = 0

    if st.session_state.q_idx < len(questions):
        q = questions[st.session_state.q_idx]
        st.subheader(f"Питання {st.session_state.q_idx + 1} з {len(questions)}")
        answer = st.radio(q["питання"], q["варіанти"], key=f"q{st.session_state.q_idx}")
        if st.button("✅ Відповісти"):
            if answer == q["правильна"]:
                st.success("✅ Вірно!")
                st.session_state.balls += 1
            else:
                st.error(f"❌ Правильна відповідь: {q['правильна']}")
            st.session_state.q_idx += 1
            st.experimental_rerun()
    else:
        st.balloons()
        st.success(f"🏁 Готово! Результат: {st.session_state.balls} з {len(questions)}")
        if st.button("🔁 Почати спочатку"):
            del st.session_state.q_idx
            del st.session_state.balls
            st.experimental_rerun()

# --- 5. Аналітика
elif menu == "📊 Аналітика (🔜)":
    st.header("📊 Аналітична панель")

    try:
        with open("game_results.json", "r", encoding="utf-8") as f:
            game_data = [json.loads(line) for line in f]
        df = pd.DataFrame(game_data)
        df["спроб"] = df["здогадки"].apply(len)
        st.write("🎯 Ігор:", len(df))
        st.write("✅ Виграшів:", (df["результат"] == "виграв").sum())
        st.write("❌ Програшів:", (df["результат"] == "програв").sum())
        st.write("📊 Середнє спроб:", round(df["спроб"].mean(), 2))
        st.bar_chart(df["результат"].value_counts())
    except:
        st.warning("Файл з іграми не знайдено.")

    try:
        with open("generated_stories.json", "r", encoding="utf-8") as f:
            stories = [json.loads(line) for line in f]
        df2 = pd.DataFrame(stories)
        df2["день"] = df2["дата"].str[:10]
        st.line_chart(df2["день"].value_counts().sort_index())
    except:
        st.warning("Файл з історіями не знайдено.")
