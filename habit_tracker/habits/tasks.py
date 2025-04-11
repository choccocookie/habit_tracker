from celery import shared_task
from django.utils import timezone
from .models import Habit
from .services.telegram_service import send_telegram_message
from django.conf import settings

TELEGRAM_TOKEN = settings.TELEGRAM_BOT_TOKEN

@shared_task
def send_habit_reminder():
    now = timezone.now().time()  # получаем текущее время
    habits = Habit.objects.filter(time__lte=now, completed=False)  # находим привычки, для которых время пришло

    for habit in habits:
        # Отправляем сообщение пользователю
        message = f"Напоминание: Выполни привычку: {habit.action} в {habit.place}."
        send_telegram_message(habit.user.telegram_chat_id, message)

        # Можно обновить статус привычки (если необходимо)
        habit.completed = True
        habit.save()

