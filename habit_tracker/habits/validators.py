from rest_framework.exceptions import ValidationError


def validate_pleasant_habit(instance):
    """
    Приятная привычка не может иметь вознаграждение или связанную привычку.
    """
    if instance.is_pleasant and (instance.reward or instance.related_habit):
        raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

def validate_related_habit(instance):
    """
    У полезной привычки может быть либо вознаграждение, либо приятная связанная привычка.
    """
    if not instance.is_pleasant and instance.reward and instance.related_habit:
        raise ValidationError("У полезной привычки не может быть и вознаграждения, и связанной приятной привычки одновременно.")

def validate_duration(instance):
    """
    Проверка, что выполнение привычки занимает не больше двух минут.
    """
    if instance.execution_time > 2:
        raise ValidationError("Время на выполнение привычки не должно превышать 2 минуты.")


def validate_related_habit_is_pleasant(instance):
    """
    Связанная привычка должна быть приятной.
    """
    if instance.related_habit and not instance.related_habit.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной.")

def validate_periodicity(instance):
    """
    Периодичность привычки не может быть реже одного раза в 7 дней.
    """
    if instance.periodicity > 7:
        raise ValidationError("Периодичность привычки не может быть реже одного раза в 7 дней.")