import shutil

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import *
from django.contrib.auth.models import User
from .models import *
import os
import cv2
import datetime
from PIL import Image
from django.http import HttpResponse, JsonResponse


# Create your views here.
def adminview(request):
    return render(request, 'adminview.html')


def authenticateadmin(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('adminhome')
    if user is None:
        messages.add_message(request, messages.ERROR, "Invalid Credentials")
        return redirect('adminview')


def adminhome(request):
    context = {'customers': Users.objects.all()}
    return render(request, 'adminhome.html', context=context)


def logoutadmin(request):
    logout(request)
    return redirect('adminview')


def addcustomer(request):
    name = request.POST['cusname']
    mail = request.POST['cusemail']
    state = request.POST['cusstate']
    userid = request.POST['cusid']
    context = {
        "name": name,
        "mail": mail,
        "state": state,
        "userid": userid,
        "usr": Users.objects.all()
    }
    return render(request, 'adminhome.html', context=context)


def deletecustomer(request, customerpk=None):
    customer = get_object_or_404(Users, id=customerpk)
    customer.delete()
    return redirect('adminhome')


def error_404_view(request, exception):
    return render(request, 'Error.html')


def index(request):
    statecount = dict()
    states = []
    usr = Users.objects.all()
    for u in usr:
        states.append(u.state)
    for i in states:
        #print(i)
        if i in statecount:
            statecount[i] += 1
        else:
            statecount[i] = 1

    context = {
        'userstate': states,
        "states": statecount
    }
    return render(request, 'index.html', context=context)


def signings(request):
    return render(request, 'signup.html')


def usersignin(request):
    return render(request, 'login.html')


def usersignup(request):
    return render(request, 'signup.html')


def signup(request):
    name = request.POST['firstname'] + ' ' + request.POST['lastname']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    gender = request.POST['gender']
    contact = request.POST['contact']
    country = request.POST['country']
    state = request.POST['state']
    pin = request.POST['pin']
    image = request.FILES['image']
    if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR, "UserID is taken")
        return redirect('usersignup')
    User.objects.create_user(username=username, password=password).save()
    lastObj = len(User.objects.all())-1
    Users(userid=User.objects.all()[int(lastObj)].id, name=name, username=username, email=email, password=password,
          gender=gender, contact=contact, country=country,
          state=state, pincode=pin, image=image).save()
    path = 'C:\\Users\\jhili\\python_project\\expirydate\\static\\users'
    os.chdir(path)
    foldername = username
    os.mkdir(foldername)
    path2 = path+'\\'+foldername
    os.chdir(path2)
    os.mkdir('products')
    messages.add_message(request, messages.ERROR, "Account created")
    return redirect('userlogin')


def userlogout(request):
    logout(request)
    return redirect('userlogin')


def authenticateuser(request):
    username = request.POST['userlog']
    password = request.POST['passlog']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('userhome')
    if user is None:
        messages.add_message(request, messages.ERROR, "Invalid Credentials")
        return redirect('userlogin')


def userhome(request):
    username = request.user.username
    path = r'C:\Users\jhili\python_project\expirydate\static\users\{}\products'.format(username)
    pathpart = '{}/products/'.format(username)
    file_list = os.listdir(path)
    #li = [x.split('.')[0] for x in file_list]
    #print(li)
    context = {
        'username': username,
        'ownInfo': Users.objects.all(),
        'productInfo': ProductDB.objects.all(),
        'list_product': file_list,
        'pathpart': pathpart
    }
    return render(request, 'userhome.html', context=context)


def deleteuser(request, useridpk=None):
    ownaccnt = get_object_or_404(Users, id=useridpk)
    ownaccnt.delete()
    return redirect('index')


def edituser(request, customerpk=None):
    username = request.user.username
    context = {
        'username': username,
        'ownInfo': Users.objects.get(id=customerpk)
    }
    return render(request, 'updateuser.html', context=context)


def editting(request, customerpk=None):
    info = Users.objects.get(id=customerpk)
    email = request.POST['email']
    contact = request.POST['contact']
    country = request.POST['country']
    state = request.POST['state']
    pin = request.POST['pin']
    info.email = email
    info.contact = contact
    info.country = country
    info.state = state
    info.pincode = pin
    info.save()
    messages.add_message(request, messages.ERROR, "Account updated")
    return redirect('userhome')


def takingphoto(request):
    username = request.user.username
    lastObj = len(ProductDB.objects.all()) - 1
    product = ProductDB.objects.all()[int(lastObj)].pname
    timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    cam = cv2.VideoCapture(0,  cv2.CAP_DSHOW)
    directory = r'C:\Users\jhili\python_project\expirydate\static\users\{}\products'.format(username)
    dest_folder = r'C:\Users\jhili\python_project\expirydate\static\users\alls'
    #cv2.namedWindow("Product Captured")

    img_counter = 0
    while True:
        ret, frame = cam.read()
        os.chdir(directory)
        if not ret:
            print("Failed to capture it. Try again.")
            break

        cv2.imshow("Capture Products' Image", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing the window")
            return render(request, 'userhome.html')
        elif k % 256 == 32:
            img_name = "{}_{}_{}_{}.png".format(username, product, timestr, img_counter)
            cv2.imwrite(img_name, frame)
            os.chdir(dest_folder)
            cv2.imwrite(img_name, frame)
            print("Picture taken")
            img_counter += 1

    cam.release()
    cam.detroyAllWindows()


def productentry(request):
    uname = request.POST['uname']
    pname = request.POST['prodname']
    pdate = request.POST['proddate']
    x = pdate.split("T")
    #print(x)
    date = x[0]
    datetimes = date + " " + x[1]
    #print(datetimes)
    pdate = datetime.datetime.strptime(datetimes, '%Y-%m-%d %H:%M')
    #pdate = datetime.date.today()
    #d1 = pdate.strftime("%Y-%m-%d")
    ProductDB(uname=uname, pname=pname, pdate=pdate, sharing=0).save()
    return redirect('userhome')


def deleteproduct(request, productidpk=None):
    prod = get_object_or_404(ProductDB, id=productidpk)
    prod.delete()
    return redirect('userhome')


def shareproduct(request, productidpk=None):
    prod = ProductDB.objects.get(id=productidpk)
    prod.sharing = 1
    prod.save()
    return redirect('userhome')


def notification(request):
    username = request.user.username
    nottexts = Contacting.objects.all()
    useraccnt = Users.objects.all()
    context = {
        'username': username,
        'nottexts': nottexts,
        'useraccnt': useraccnt,
    }
    return render(request, 'notification.html', context=context)


def feed(request):
    username = request.user.username
    dest_folder = r'C:\Users\jhili\python_project\expirydate\static\users\alls'
    destpart = 'alls/'
    allprod_list = os.listdir(dest_folder)
    #print(allprod_list)
    context = {
        'username': username,
        'ownInfo': Users.objects.all(),
        'productInfo': ProductDB.objects.all(),
        'allprod_list': allprod_list,
        'destpart': destpart,
    }
    return render(request, 'feed.html', context=context)


def contact(request, contactto=None):
    username = request.user.username
    tosend = contactto
    toinfo = Users.objects.all()
    context = {
        'username': username,
        'tosend': tosend,
        'toinfo': toinfo,
    }
    return render(request, 'texting.html', context=context)


def storemsg(request, contactto=None):
    tosend = contactto
    totext = request.POST['totext']
    bysend = request.user.username
    timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Contacting(sender=bysend, receiver=tosend, attime=timestr, message=totext).save()
    messages.add_message(request, messages.ERROR, "Message has sent")
    return redirect('feed')


def notifytext(request):
    pass