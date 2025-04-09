from rest_framework import serializers
from .models import Habit
from .validators import (validate_duration, validate_pleasant_habit, validate_related_habit)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        instance = Habit(**data)
        validate_duration(instance)
        validate_related_habit(instance)
        validate_pleasant_habit(instance)
        return data
