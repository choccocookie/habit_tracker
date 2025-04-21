from rest_framework import serializers
from .models import Habit
from .validators import (validate_duration, validate_pleasant_habit, validate_related_habit,
                         validate_related_habit_is_pleasant, validate_periodicity)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ('user',)

    def validate(self, data):
        instance = Habit(**data, user=self.context['request'].user)
        validate_duration(instance)
        validate_related_habit(instance)
        validate_pleasant_habit(instance)
        validate_related_habit_is_pleasant(instance)
        validate_periodicity(instance)
        return data
