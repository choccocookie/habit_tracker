from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)

class Habit(models.Model):
    PERIOD_CHOICES = (
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    #title = models.Charfield(max_lenght=100, verbose_name="Название привычки")
    #description = models.TextField(blank=True, verbose_name="Описание привычки")
    place = models.CharField(max_length=255, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name="Связанная привычка",
                                      help_text="Указывать только для полезных привычек")
    periodicity = models.PositiveIntegerField(default=1, verbose_name="Периодичность (в днях)")
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение",
                                 help_text="Указывать только для полезных привычек")
    execution_time = models.PositiveIntegerField(default=2,
                                                 verbose_name="Время на выполнение (в минутах)",
                                                 help_text="Не должно превышать 120 секунд (2 минуты)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["time"]



class TelegramUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=100, unique=True)


