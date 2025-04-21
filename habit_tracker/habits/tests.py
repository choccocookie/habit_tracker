from django.test import TestCase
from django.core.exceptions import ValidationError
from Users.models import User
from habits.models import Habit


class HabitModelTest(TestCase):

    def setUp(self):
        """Создание пользователя и базовых данных для тестов"""
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            phone='1234567890',
            сity='Test City',
            telegram_chat_id='testchatid'
        )

        # Привычка с валидными данными
        self.habit_data = {
            "user": self.user,
            "place": "Дома",
            "time": "08:00",
            "action": "Читать книгу",
            "is_pleasant": True,
            "periodicity": 1,
            "execution_time": 1,
            "is_public": True
        }

    def test_create_valid_habit(self):
        """Тест на создание валидной привычки"""
        habit = Habit.objects.create(**self.habit_data)
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.place, "Дома")
        self.assertEqual(habit.time.strftime("%H:%M"), "08:00")
        self.assertEqual(habit.action, "Читать книгу")
        self.assertTrue(habit.is_pleasant)
        self.assertEqual(habit.periodicity, 1)
        self.assertEqual(habit.execution_time, 1)
        self.assertTrue(habit.is_public)

    def test_pleasant_habit_with_related_habit(self):
        """Тест на то, что приятная привычка не может иметь связанную привычку"""
        habit1 = Habit.objects.create(**self.habit_data)
        habit2 = Habit.objects.create(**self.habit_data, is_pleasant=True, related_habit=habit1)

        with self.assertRaises(ValidationError):
            habit2.full_clean()  # Вызовет ошибку, так как это приятная привычка

    def test_non_pleasant_habit_with_related_habit_and_reward(self):
        """Тест на то, что полезная привычка не может иметь и вознаграждение, и связанную привычку"""
        habit1 = Habit.objects.create(**self.habit_data)
        habit2 = Habit.objects.create(**self.habit_data, is_pleasant=False, reward="Reward", related_habit=habit1)

        with self.assertRaises(ValidationError):
            habit2.full_clean()  # Ошибка, так как полезная привычка не может иметь и вознаграждение, и связанную привычку

    def test_execution_time_validation(self):
        """Тест на валидацию времени выполнения привычки (не более 2 минут)"""
        habit = Habit.objects.create(**self.habit_data, execution_time=3)

        with self.assertRaises(ValidationError):
            habit.full_clean()  # Ошибка, так как execution_time не может быть больше 2 минут

    def test_periodicity_validation(self):
        """Тест на валидацию периодичности привычки (не менее 1 дня)"""
        habit = Habit.objects.create(**self.habit_data, periodicity=0)

        with self.assertRaises(ValidationError):
            habit.full_clean()  # Ошибка, так как periodicity не может быть меньше 1

    def test_related_habit_validation_for_non_pleasant(self):
        """Тест на валидацию для полезной привычки, у которой может быть связанная привычка"""
        habit1 = Habit.objects.create(**self.habit_data)
        habit2 = Habit.objects.create(**self.habit_data, is_pleasant=False, related_habit=habit1)
        self.assertEqual(habit2.related_habit, habit1)  # Всё работает нормально для полезных привычек

    def test_habit_str_method(self):
        """Тест на строковое представление привычки"""
        habit = Habit.objects.create(**self.habit_data)
        self.assertEqual(str(habit), "Читать книгу в 08:00 Дома")  # Проверка правильности строки
