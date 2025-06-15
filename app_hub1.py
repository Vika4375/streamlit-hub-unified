import streamlit as st
import random
import json
from datetime import datetime

st.set_page_config(page_title="🛠️ Streamlit Hub", page_icon="🏠")

# Навігація
st.sidebar.title("Вибери розділ")
section = st.sidebar.radio("", ["🎲 Вгадай число", "🔤 Вгадай слово", "💌 Компліментатор", "📚 Генератор історій"])

# Функція для збереження результатів у JSON
def save_result(filename, data):
    try:
        arr = json.load(open(filename, encoding="utf-8"))
    except:
        arr = []
    arr.append(data)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(arr, f, ensure_ascii=False, indent=2)

# 1 — Вагадай число
if section == "🎲 Вгадай число":
    st.header("Вгадай число (1–100)")
    if 'num_secret' not in st.session_state:
        st.session_state.num_secret = random.randint(1,100)
        st.session_state.num_attempts = 0
    guess = st.number_input("Введи число", 1, 100, key="num_input")
    if st.button("Вгадати", key="guess_num"):
        st.session_state.num_attempts += 1
        if guess < st.session_state.num_secret:
            st.warning("🔼 Більше")
        elif guess > st.session_state.num_secret:
            st.warning("🔽 Менше")
        else:
            st.success(f"🎉 Вітаю! Ти вгадав за {st.session_state.num_attempts} спроб.")
            save_result("game_results.json", {
                "game": "число", "tries": st.session_state.num_attempts,
                "ok": True, "time": datetime.now().isoformat()
            })
            st.session_state.num_secret = random.randint(1,100)
            st.session_state.num_attempts = 0

# 2 — Вгадай слово
elif section == "🔤 Вгадай слово":
    st.header("Вгадай слово")
    words = ["яблуко","банан","ківі","апельсин","слива"]
    if 'word_secret' not in st.session_state:
        st.session_state.word_secret = random.choice(words)
        st.session_state.word_attempts = 0
    inp = st.text_input("Введи слово", key="word_input")
    if st.button("Спробувати", key="guess_word"):
        st.session_state.word_attempts += 1
        if inp.lower() == st.session_state.word_secret:
            st.success(f"Ура! Вгадала за {st.session_state.word_attempts}")
            save_result("game_results.json", {
                "game": "слово", "tries": st.session_state.word_attempts,
                "ok": True, "time": datetime.now().isoformat()
            })
            st.session_state.word_secret = random.choice(words)
            st.session_state.word_attempts = 0
        else:
            st.error("Ні, спробуй інше!")

# 3 — Компліментатор
elif section == "💌 Компліментатор":
    st.header("Компліментатор")
    names = ["Віка","Оля","Іван","Макс"]
    adj = ["чудова","талановита","неймовірна","весела","розумна"]
    comp = ["як сонце","як зірка","як магніт","як натхнення"]
    if st.button("Дай комплімент"):
        nm = random.choice(names)
        a = random.choice(adj)
        c = random.choice(comp)
        st.success(f"{nm}, ти {a} — {c} ✨")
        save_result("game_results.json", {
            "game": "комплімент", "ok": True,
            "time": datetime.now().isoformat()
        })

# 4 — Генератор історій
elif section == "📚 Генератор історій":
    st.header("Історія на замовлення")
    noun = st.text_input("Ім'я персонажа")
    place = st.text_input("Місце (ліс, місто тощо)")
    if st.button("Створи історію"):
        if noun and place:
            story = f"Одного разу {noun} знайшов скарб у {place}. З того дня життя змінилося..."
            st.write(story)
            save_result("generated_stories.json", {
                "character": noun, "place": place,
                "story": story, "time": datetime.now().isoformat()
            })
        else:
            st.warning("Заповни обидва поля!")

# Додатково — перегляд збережених результатів
st.sidebar.markdown("---")
if st.sidebar.checkbox("📁 Переглянути збережене"):
    st.sidebar.write("📝 Результати гри:")
    try:
        st.sidebar.json(json.load(open("game_results.json", encoding="utf-8")))
    except:
        st.sidebar.write("Поки що порожньо.")
    st.sidebar.write("📖 Історії:")
    try:
        st.sidebar.json(json.load(open("generated_stories.json", encoding="utf-8")))
    except:
        st.sidebar.write("Поки що порожньо.")
