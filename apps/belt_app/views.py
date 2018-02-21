from django.shortcuts import render, redirect
from models import *
from django.contrib import messages
from datetime import *

def index(request):
    return render(request, 'belt_app/index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(name=request.POST['name'], username=request.POST['username'], password=password)
        id = User.objects.get(username=request.POST['username']).id
        request.session['id'] = id
        request.session['name'] = User.objects.get(id=id).name
        return redirect('/success')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tags, error in errors.iteritems():
            messages.error(request, error, extra_tags=tags)
        return redirect('/')
    else:
        id = User.objects.get(username=request.POST['username']).id
        request.session['id'] = id
        request.session['name'] = User.objects.get(id=id).name
        return redirect('/success')

def success(request):
    u = User.objects.get(id=request.session['id'])
    user_travels = []
    for travel in Travel.objects.all():
        if travel in u.travels.all():
            user_travels.append(travel)

    data = {
        'users': User.objects.exclude(id=request.session['id']),
        'travels': Travel.objects.all(),
        'user_travels': user_travels
    }
    return render(request, 'belt_app/success.html', data)

def add(request):
    return render(request, 'belt_app/add.html')

def add_process(request, id):
    if 'destination' in request.POST and "description" in request.POST and "dateFrom" in request.POST and "dateTo" in request.POST:
        create = True
        print request.POST['dateFrom']
        if len(request.POST['dateFrom']) != 0 and len(request.POST['dateTo']) != 0:
            if datetime.strptime(request.POST['dateFrom'], '%Y-%m-%d').date() > datetime.strptime(request.POST['dateTo'], '%Y-%m-%d').date():
                messages.error(request, "Travel Date To should not be before the Travel Date From")
                create = False
            if datetime.strptime(request.POST['dateFrom'], '%Y-%m-%d').date() < datetime.today().date() or datetime.strptime(request.POST['dateTo'], '%Y-%m-%d').date() < datetime.today().date():
                messages.error(request, "Travel dates should be future-dated")
        if len(request.POST['destination']) == 0 or len(request.POST['description']) == 0 or len(request.POST['dateFrom']) == 0 or len(request.POST['dateTo']) == 0:
            messages.error(request, "No empty entries")
            create = False
    if create:
        t = Travel.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date=request.POST['dateFrom'], end_date=request.POST['dateTo'], user_id=request.session['id'])
        u = User.objects.get(id=id)
        u.travels.add(t)
        return redirect('/success')
    else: 
        return redirect('/add')
    


def travel(request, id):
    travel = Travel.objects.get(id=id)
    data = {
        "travel": Travel.objects.get(id=id),
        "user": User.objects.get(id=travel.user_id),
        "other_users": travel.users.all(),
        "creator": User.objects.get(id=travel.user_id).name

    }
    return render(request, 'belt_app/travel.html', data)

def join(request, id):
    u = User.objects.get(id=request.session['id'])
    t = Travel.objects.get(id=id)
    u.travels.add(t)

    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')