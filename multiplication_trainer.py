import streamlit as st
import random


def check_answer(expression, correct_answer):
  print(f'{expression} = ', end='')
  user_answer = int(input())
  while user_answer != correct_answer:
    print('К сожалению, ты ошибся! Попробуй еще раз')
    print(f'{expression} = ', end='')
    user_answer = int(input())
  print('Правильно!')


def game():
  for try_count in range(20):
    operations = ['умножение', 'деление']
    operation = random.choice(operations)
    if operation == 'умножение':
      first_number = random.randint(0, 10)
      second_number = random.randint(0, 10)
      check_answer(f'{first_number} * {second_number}',
                   first_number * second_number)
    elif operation == 'деление':
      first_number = random.randint(0, 10)
      second_number = random.randint(1, 10)
      first_number *= second_number
      check_answer(f'{first_number} : {second_number}',
                   first_number / second_number)
  print('Ты отлично справляешься!')


print('Добро пожаловать в тренажер по умножению и делению!')
start = input('Хочешь начать тренировку? Да - нажми 1, Нет - нажми 2')
while start == '1':
  game()
  start = input('Хочешь продолжить? Да - нажми 1, Нет - нажми 2')
else:
  print('Ты молодец! Спасибо, что тренируешься регулярно :)')
