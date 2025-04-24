from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.exceptions import PermissionDenied
from .paginators import Five


class HabitCreateAPIView(CreateAPIView):
    """Создание новой привычки"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Привязываем текущего пользователя к привычке
        serializer.save(user=self.request.user)


class HabitListAPIView(ListAPIView):
    """Список привычек текущего пользователя"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Five

    def get_queryset(self):
        # Показываем только свои привычки и публичные
        return Habit.objects.filter(user=self.request.user) | Habit.objects.filter(is_public=True)


class HabitRetriveAPIView(RetrieveAPIView):
    """Получение одной привычки пользователя"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        habit = super().get_object()
        if habit.user != self.request.user and not habit.is_public:
            raise PermissionDenied("Вы не можете просматривать эту привычку")
        return habit


class HabitUpdateAPIView(UpdateAPIView):
    """Обновление одной привычки"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        habit = super().get_object()
        if habit.user != self.request.user:
            raise PermissionDenied("""Вы можете менять только свои привычки""")
        return habit


class HabitDestroyAPIView(DestroyAPIView):
    """Удаление привычки"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        habit = super().get_object()
        if habit.user != self.request.user:
            raise PermissionDenied("""Вы можете удалять только свои привычки""")
        return habit
