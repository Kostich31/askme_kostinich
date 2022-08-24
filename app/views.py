import random

from django.shortcuts import render, redirect, reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from app.models import *
from app.forms import *
from django.contrib import auth

def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    question = paginate(Question.objects.newest(), request)
    tag = Tag.objects.all()
    return render(request, "index.html", {"question": question})


def hot(request):
    question = paginate(Question.objects.most_popular(), request)
    tag = Tag.objects.all()
    return render(request, 'index.html', {'questions': question, 'tags': tag})


@login_required(login_url='/login/')
def ask(request):
    if request.method == "GET":
        form = AskForm()

    if request.method == "POST":
        form = AskForm(data=request.POST)
        if form.is_valid():
            tags = form.save()
            user = User.objects.filter(user=request.user).values("id")
            question = Question.objects.create(author_id=user,
                                               title=form.cleaned_data["title"],
                                               text=form.cleaned_data["text"],
                                               date=datetime.today())
            for _tag in tags:
                question.tags.add(_tag)
                question.save()
            return redirect("question", pk=question.id)
    return render(request, "ask.html", {"form": form})


def login(request):
    redirect_to = request.GET.get('next', '/')
    error_message = None
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(redirect_to)
            else:
                error_message = "Sorry, wrong login or password"
    return render(request, 'login.html', {'form': form, 'redirect_to': redirect_to, 'error_message': error_message})


def question(request, pk):
    selected_question = Question.objects.by_id(pk).first()
    selected_answers = Answer.objects.filter(what_question=selected_question)
    content = paginate(selected_answers, request, 3)

    if request.method == "GET":
        form = AnswerForm()

    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        user = User.objects.filter(user=request.user).values("id")
        if form.is_valid():
            answer = Answer.objects.create(question_id=selected_question.id,
                                           author_id=user,
                                           text=form.cleaned_data["text"])
            return redirect(reverse("question", kwargs={"pk": selected_question.id}) + "?page="
                            + str(content.paginator.num_pages+1))

    return render(request, "question.html",
                  {"question": selected_question, "content": content, "form": form})


def signup(request):
    if request.method == "GET":
        form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                user.set_password(request.POST['password'])
                user.save()
                auth.login(request, user)
                return redirect("index")
    return render(request, "signup.html", {"form": form})


@login_required(login_url='/login/')
def settings(request):
    if request.method == "GET":
        user = request.user
        form = SettingsForm()
        if not user.is_authenticated:
            return HttpResponseForbidden()

    if request.method == "POST":
        form = SettingsForm(data=request.POST)
        if form.is_valid():
            user = request.user
            if user.is_authenticated:
                if form.cleaned_data["username"] != user.username and form.cleaned_data["username"] != "":
                    user.username = form.cleaned_data["username"]
                    user.save()
                    auth.login(request, user)
                if form.cleaned_data["email"] != user.email and form.cleaned_data["email"] != "":
                    user.email = form.cleaned_data["email"]
                    user.save()
                    auth.login(request, user)
    return render(request, "settings.html", {"form": form})


def tag(request, tag):
    question = paginate(Tag.objects.question_by_tag(tag), request)
    return render(request, 'tag.html', {'questions': question, "tag": tag})

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next', '/'))
    