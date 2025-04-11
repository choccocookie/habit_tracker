
import requests
from django.conf import settings
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Application
import os
from datetime import datetime
from habit_tracker.habits.models import Habit

TELEGRAM_TOKEN = "7641127950:AAFt4ri4sSx33XvrdTGSRs5qWsEl1nSHI2k"


async def add_habit(update: Update, context: CallbackContext):
    # Получаем информацию о привычке и времени
    user = update.message.from_user
    message = update.message.text.split(' ')  # Разделим на привычку и время

    habit_name = message[1]  # Имя привычки
    time_str = message[2]  # Время (например, 14:30)

    # Преобразуем время в объект Time
    time = datetime.strptime(time_str, '%H:%M').time()

    # Создаем привычку в базе данных
    Habit.objects.create(user=user, action=habit_name, time=time, place="Home")

    # Ответ пользователю
    await update.message.reply_text(f"Привычка '{habit_name}' добавлена на {time_str}")




def send_telegram_message(chat_id: str, message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()


# Запуск бота
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("add_habit", add_habit))
    application.run_polling()

if __name__ == '__main__':
    main()

