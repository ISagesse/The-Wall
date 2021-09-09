from django.contrib.messages.api import error
from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def welcome(request):
    if 'userid' not in request.session:
        context = {
            'login': False,
            'messages': Message.objects.all(),
            'comments': Comment.objects.all()
        }
        return render(request, "wall.html", context)
    context = {
        'login': True,
        'user': User.objects.get(id=request.session['userid']),
        'messages': Message.objects.all(),
        'comments': Comment.objects.all()
    }
    return render(request, "wall.html", context)

def register(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/geting_started')
    else:
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        new_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(
                first_name = f_name,
                last_name = l_name,
                email = email,
                password = new_password
            )
        request.session['userid'] = user.id
        return redirect('/')

def login(request):
    user_email = User.objects.filter(email = request.POST['email'])
    if user_email:
        logged_user = user_email[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("/")
        else:
            messages.error(request, "Incorrect password")
            return redirect("/geting_started")
    else:
        messages.error(request, "Incorrect email")
        return redirect("/geting_started")

def logout(request):
    request.session.clear()
    return redirect('/')

def create_message(request):
    if 'userid' not in request.session:
        return redirect('/geting_started')

    this_user = User.objects.get(id=request.session['userid'])
    Message.objects.create(
        message = request.POST["message"],
        user = this_user
    )
    return redirect('/')

def create_comment(request):
    if 'userid' not in request.session:
        return redirect('/geting_started')

    this_user = User.objects.get(id=request.session['userid'])
    this_message = Message.objects.get(id=request.POST['message_id'])
    Comment.objects.create(
        comment = request.POST["comment"],
        user = this_user,
        message = this_message
    )
    return redirect('/')
