from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    '''homepage of learning_logs app'''
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    '''return list of topics'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    '''return one topic and all including entries'''
    topic = Topic.objects.get(id=topic_id)
    # проверка принадлежности темы текущему пользователю
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''define new topic'''
    if request.method != 'POST':
        # данные не отправились, создаётся пустая форма
        form = TopicForm()
    else:
        # отправлены данные POST, обработать данные
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    # Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    '''add new entry on the topic'''
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # данные не отправились, создаётся пустая форма
        form = EntryForm()
    else:
        # отправлены данные POST, обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    # Вывести пустую или недействительную форму
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    '''edit existing entry'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # проверка принадлежности темы текущему пользователю
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Исходный запрос, форма заполняется данными текущей записи
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST, обработка данных
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
