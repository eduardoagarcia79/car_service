from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Brand, Car, Service_Detail

# Create your views here.

def index(request):
    return render (request, 'index.html')

def new_user(request): 
    if request.method == "POST":
        errors = User.objects.basic_validator_new(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            default_hash = bcrypt.hashpw('12345678'.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'], 
                email_address=request.POST['email'],
                phone=request.POST['phone'], 
                password = default_hash
            )
            request.session['userid'] = new_user.id
            return redirect('/details')
    return redirect('/')

def login(request):
    if request.method == "POST": 
        errors = User.objects.basic_validator_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.filter(email_address=request.POST['email'])
            if user:
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['userid'] = logged_user.id
                    return redirect('/details')
            return redirect("/")
    return redirect('/')

def registration(request, service_id):
    if 'userid' in request.session:
        if request.method == "POST":
            errors = User.objects.basic_validator_pwd(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/confirmation/{service_id}')
            else:
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                update_user = User.objects.get(id=request.session['userid'])
                update_user.password = pw_hash
                update_user.save()
                return redirect('/')
        return redirect('/')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect("/")

def details(request):
    if 'userid' in request.session:
        user = User.objects.get(id=request.session['userid'])
        context = {
            "user": user,
            "brands": Brand.objects.all(),
            "cars": Car.objects.filter(owner=user.id)
        }
        return render (request, 'details.html', context)
    return redirect('/')

def service_new_car(request):
    if 'userid' in request.session:
        if request.method == "POST":
            errors = Service_Detail.objects.basic_validator_service(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/details')
            else: 
                owner = User.objects.get(id=request.session['userid'])
                car_brand = Brand.objects.filter(name=request.POST['brand'])
                new_car = Car.objects.create (
                    brand = car_brand[0],
                    year = request.POST["year"],
                    mileage = request.POST["mileage"],
                    owner = owner
                )
                date = request.POST["service_date"]
                time = request.POST["service_time"]
                service_date = date + " " + time
                new_service = Service_Detail.objects.create (
                    car = new_car,
                    service_date = service_date, 
                )
                service_id = new_service.id
                return redirect(f'/confirmation/{service_id}')
        return redirect('/details')
    return redirect('/')

def service_existing_car(request, car_id):
    if 'userid' in request.session:
        if request.method == "POST":
            errors = Service_Detail.objects.basic_validator_service(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/details')
            else: 
                car_brand = Brand.objects.filter(name=request.POST['brand'])
                update_car = Car.objects.get(id=car_id)
                update_car.brand = car_brand[0]
                update_car.year = request.POST['year']
                update_car.mileage = request.POST['mileage']
                update_car.save()
                date = request.POST["service_date"]
                time = request.POST["service_time"]
                service_date = date + " " + time
                new_service = Service_Detail.objects.create (
                    car = update_car,
                    service_date = service_date, 
                )
                service_id = new_service.id
                return redirect(f'/confirmation/{service_id}')
        return redirect('/details')
    return redirect('/')

def confirmation(request, service_id):
    if 'userid' in request.session:
        user = User.objects.get(id=request.session['userid'])
        context = {
            "user": user,
            "service": Service_Detail.objects.get(id=service_id)
        }
        return render (request, 'confirmation.html', context)
    return redirect('/')

def delete(request, car_id):
    if 'userid' in request.session:
        car_to_delete = Car.objects.get(id=car_id)
        car_to_delete.delete()
        return redirect('/details')
    return redirect('/')