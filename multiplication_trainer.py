import streamlit as st
import random

st.set_page_config(
    page_title="Тренажер умножения и деления",
    page_icon="🧮",
    layout="centered"
)

# Инициализация состояния сессии
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'problems_solved' not in st.session_state:
    st.session_state.problems_solved = 0
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ""
if 'message' not in st.session_state:
    st.session_state.message = ""
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'problem_key' not in st.session_state:
    st.session_state.problem_key = 0
if 'show_cat' not in st.session_state:
    st.session_state.show_cat = False

def generate_problem():
    """Генерирует новую задачу"""
    operations = ['умножение', 'деление']
    operation = random.choice(operations)
    
    if operation == 'умножение':
        first_number = random.randint(0, 10)
        second_number = random.randint(0, 10)
        correct_answer = first_number * second_number
        problem_text = f"{first_number} × {second_number} = ?"
        
    else:  # деление
        # Гарантируем целочисленное деление
        second_number = random.randint(1, 10)
        result = random.randint(0, 10)
        first_number = second_number * result
        
        correct_answer = result
        problem_text = f"{first_number} : {second_number} = ?"
    
    st.session_state.current_problem = {
        'text': problem_text,
        'correct_answer': correct_answer,
        'operation': operation
    }
    st.session_state.user_answer = ""
    st.session_state.message = ""
    st.session_state.show_success = False
    st.session_state.problem_key += 1  # Изменяем ключ для сброса поля ввода

def check_answer():
    """Проверяет ответ пользователя"""
    user_input = st.session_state.get(f"user_answer_{st.session_state.problem_key}", "").strip()
    
    if not user_input:
        st.session_state.message = "⚠️ Ты не ответила :("
        return
    
    try:
        user_answer = int(user_input)
        correct_answer = st.session_state.current_problem['correct_answer']
        
        if user_answer == correct_answer:
            st.session_state.score += 1
            st.session_state.problems_solved += 1
            st.session_state.message = "✅ Правильно! Молодец!"
            st.session_state.show_success = True
            
        else:
            st.session_state.message = "❌ К сожалению, ты ошиблась! Попробуй еще раз"
            
    except ValueError:
        st.session_state.message = "⚠️ Нужно указать число"

def start_game():
    """Начинает новую игру"""
    st.session_state.game_active = True
    st.session_state.score = 0
    st.session_state.problems_solved = 0
    st.session_state.problem_key = 0
    st.session_state.show_cat = False
    generate_problem()

def end_game():
    """Завершает игру"""
    st.session_state.game_active = False
    st.session_state.current_problem = None
    st.session_state.message = ""
    st.session_state.show_success = False

def show_cat_page():
    """Показывает страницу с котиком"""
    st.session_state.game_active = False
    st.session_state.show_cat = True

def return_to_start():
    """Возвращает на стартовую страницу"""
    st.session_state.game_active = False
    st.session_state.show_cat = False

# Проверяем, нужно ли показывать страницу с котиком
if st.session_state.show_cat:
    st.title("🐱 Мяу! Спасибо за тренировку!")
    
    # Добавляем изображение котика (используем URL с изображением кота)
    st.image("https://cataas.com/cat/cute", caption="Вот тебе котик за старания! 😊", use_container_width=True)
    
    st.markdown("---")
    
    if st.button("↩️ Вернуться к тренажеру", use_container_width=True, type="primary"):
        return_to_start()
        st.rerun()
    
    st.stop()

# Основной интерфейс
st.title("🧮 Тренажер умножения и деления")

if not st.session_state.game_active and not st.session_state.show_cat:
    # Стартовый экран
    st.markdown("Добро пожаловать в тренажер по умножению и делению!")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("✅ Начать тренировку", use_container_width=True, type="primary"):
            start_game()
            st.rerun()
    with col2:
        if st.button("❌ Выйти", use_container_width=True, type="secondary"):
            show_cat_page()
            st.rerun()

else:
    # Игровой интерфейс
    # Простой счетчик вместо таблицы статистики
    st.write(f"**Решено примеров: {st.session_state.problems_solved}/20**")
    
    st.markdown("---")
    
    # Текущая задача
    if st.session_state.current_problem:
        st.markdown(f"## {st.session_state.current_problem['text']}")
        
        # Поле для ввода ответа с уникальным ключом
        user_input = st.text_input(
            "Твой ответ:",
            value="",
            key=f"user_answer_{st.session_state.problem_key}",
            placeholder="Введи ответ...",
            label_visibility="collapsed"
        )
        
        # Кнопка проверки
        if st.button("🔍 Проверить ответ", use_container_width=True, type="primary"):
            check_answer()
            st.rerun()
        
        # Сообщение о результате
        if st.session_state.message:
            if "✅" in st.session_state.message:
                st.success(st.session_state.message)
            elif "❌" in st.session_state.message:
                st.error(st.session_state.message)
            else:
                st.warning(st.session_state.message)
        
        # Кнопка следующего примера (после правильного ответа)
        if st.session_state.show_success:
            if st.button("➡️ Следующий пример", use_container_width=True, type="primary"):
                if st.session_state.problems_solved < 20:
                    generate_problem()
                    st.rerun()
                else:
                    # Завершаем игру после 20 примеров
                    end_game()
                    st.rerun()
    
    # Завершение тренировки
    if st.session_state.problems_solved >= 20:
        st.balloons()
        st.success("🎉 Ты отлично справляешься! 20 примеров решено!")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Начать заново", use_container_width=True, type="primary"):
                start_game()
                st.rerun()
        with col2:
            if st.button("🐱 Посмотреть котика", use_container_width=True, type="secondary"):
                show_cat_page()
                st.rerun()

    st.markdown("---")
    if st.button("⏹️ Прервать тренировку", type="secondary"):
        show_cat_page()
        st.rerun()

