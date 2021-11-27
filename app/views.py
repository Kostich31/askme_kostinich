import random

from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from random import sample, choice
from app.models import *



answers = [
    {
        'id': idx_ans,
        'title': f'Answer number {idx_ans}',
        'text': f'Some text for question #{idx_ans}'
    } for idx_ans in range(5)
]

list_all_tags = ['Perl', 'Python', 'TechnoPark', 'MYSQL', 'django', 'Mail.ru', 'Shuvaeva', 'Firefox']


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    question = paginate(Question.objects.newest(), request)
    tag = Tag.objects.all()
    return render(request, 'index.html', {'questions': question, 'tags': tag})


def hot(request):
    question = paginate(Question.objects.most_popular(), request)
    tag = Tag.objects.all()
    return render(request, 'index.html', {'questions': question, 'tags': tag})


def ask(request):
    return render(request, 'ask.html', {})


def login(request):
    return render(request, 'login.html', {})


def question(request, pk):
     question = Question.objects.by_id(pk).first()
     tag = Tag.objects.all()[0:2]
     answers = question.answers.all()
     content = paginate(answers, request,5)
     return render(request, "question.html", {"question": question, "answers": content,
                                              "tags": tag})


def signup(request):
    return render(request, 'signup.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def tag(request, tag):
    question = paginate(Tag.objects.question_by_tag(tag), request)
    return render(request, 'tag.html', {'questions': question, "tag": tag})
    