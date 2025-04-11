from django.shortcuts import render, get_object_or_404, redirect
from .models import Habit
from .forms import HabitForm

# Список привычек
def habit_list(request):
    habits = Habit.objects.all()
    return render(request, 'CRUD_habits/habit_list.html', {'habits': habits})

# Добавить привычку
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'CRUD_habits/habit_create.html', {'form': form})

# Изменить привычку
def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'CRUD_habits/habit_update.html', {'form': form, 'habit': habit})

# Удалить привычку
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == 'POST':
        habit.delete()
        return redirect('habit_list')
    return render(request, 'CRUD_habits/habit_delete.html', {'habit': habit})
