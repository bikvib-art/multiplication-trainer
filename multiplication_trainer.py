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
if 'show_next' not in st.session_state:
    st.session_state.show_next = False

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
    st.session_state.show_next = False

def check_answer():
    """Проверяет ответ пользователя"""
    user_input = st.session_state.user_answer.strip()
    
    if not user_input:
        st.session_state.message = "⚠️ Введите ответ!"
        return
    
    try:
        user_answer = int(user_input)
        correct_answer = st.session_state.current_problem['correct_answer']
        
        if user_answer == correct_answer:
            st.session_state.score += 1
            st.session_state.problems_solved += 1
            st.session_state.message = "✅ Правильно! Молодец!"
            st.session_state.show_next = True
        else:
            st.session_state.message = "❌ К сожалению, ты ошибся! Попробуй еще раз"
            
    except ValueError:
        st.session_state.message = "⚠️ Введите число!"

def start_game():
    """Начинает новую игру"""
    st.session_state.game_active = True
    st.session_state.score = 0
    st.session_state.problems_solved = 0
    generate_problem()

def continue_game():
    """Продолжает игру"""
    if st.session_state.problems_solved < 20:
        generate_problem()
    else:
        end_game()

def end_game():
    """Завершает игру"""
    st.session_state.game_active = False
    st.session_state.current_problem = None

# Основной интерфейс
st.title("🧮 Тренажер умножения и деления")

if not st.session_state.game_active:
    # Стартовый экран
    st.markdown("Добро пожаловать в тренажер по умножению и делению!")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("✅ Да - начать тренировку", use_container_width=True, type="primary"):
            start_game()
            st.rerun()
    with col2:
        if st.button("❌ Нет - выйти", use_container_width=True, type="secondary"):
            st.markdown("Ты молодец! Спасибо, что тренируешься регулярно :)")
            st.stop()

else:
    # Игровой интерфейс
    # Статистика
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Решено примеров", f"{st.session_state.problems_solved}/20")
    with col2:
        st.metric("Правильных ответов", st.session_state.score)
    with col3:
        accuracy = (st.session_state.score / st.session_state.problems_solved * 100) if st.session_state.problems_solved > 0 else 0
        st.metric("Точность", f"{accuracy:.0f}%")
    
    st.markdown("---")
    
    # Текущая задача
    if st.session_state.current_problem:
        st.markdown(f"## {st.session_state.current_problem['text']}")
        
        # Поле для ввода ответа
        user_input = st.text_input(
            "Твой ответ:",
            value=st.session_state.user_answer,
            key="user_answer",
            placeholder="Введите число...",
            label_visibility="collapsed"
        )
        
        # Кнопка проверки
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔍 Проверить ответ", use_container_width=True, type="primary"):
                check_answer()
                st.rerun()
        
        with col2:
            if st.button("🔄 Новый пример", use_container_width=True):
                generate_problem()
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
        if st.session_state.show_next:
            if st.button("➡️ Следующий пример", use_container_width=True):
                continue_game()
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
            if st.button("🏁 Завершить", use_container_width=True, type="secondary"):
                end_game()
                st.rerun()

    st.markdown("---")
    if st.button("⏹️ Прервать тренировку", type="secondary"):
        end_game()
        st.rerun()
