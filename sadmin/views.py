from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views import View
from.models import Surveyor,Stock,Sell
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

# Create your views here.


def userlogin(request):
    if request.user.is_authenticated:
        return redirect('admin_home')
    else:
        if request.method == "POST":
            user = request.POST.get('user', )
            password = request.POST.get('pass', )
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('admin_home')
            else:
                messages.add_message(request, messages.ERROR, 'Username or password mismatch!')
    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect('login')


def admin_home(request):
    if request.user.is_authenticated:
        total_data_collector = Surveyor.objects.all().count()
        context={
            "isact_home":"active",
            "total_data_collector":total_data_collector,
            "title": "Dashboard",

        }
        return render(request, "admin_home.html", context)
    else:
        return redirect('login')



def surveyor_list(request, filter):
    if request.user.is_authenticated:
        user_obj = None
        if filter == 'None':
            user_obj = Surveyor.objects.all()[::-1]
        elif filter == 'active':
            user_obj = Surveyor.objects.all().filter(status=1)[::-1]
        elif filter == 'inactive':
            user_obj = Surveyor.objects.all().filter(status=2)[::-1]
        elif filter == 'rejected':
            user_obj = Surveyor.objects.all().filter(status=3)[::-1]

        context ={
            "isact_surveyorlist": "active",
            "user": user_obj,
            "title": "Data Collector List"
        }
        return render(request, "surveyor/surveyor_list.html", context)
    else:
        return redirect('login')


def view_surveyor(request, id):
    if request.user.is_authenticated:
        user_obj = Surveyor.objects.get(id=id)

        context= {
            "user": user_obj,
            "isact_surveyorlist": "active",
            "title": "Data Collector Details"
        }
        return render(request, "surveyor/view_surveyor.html", context)
    else:
        return redirect('login')


def update_surveyor(request, id):
    if request.user.is_authenticated:
        user_obj = get_object_or_404(Surveyor, id=id)
        if request.method == "POST":
            user_obj.address = request.POST.get("address")
            user_obj.profile_picture = request.POST.get("profile_picture")
            user_obj.country = request.POST.get("country")
            user_obj.division = request.POST.get("division")
            user_obj.district = request.POST.get("district")
            user_obj.sub_district = request.POST.get("sub_district")
            user_obj.email = request.POST.get("email")
            user_obj.graduation_subject = request.POST.get("graduation_subject")
            user_obj.university = request.POST.get("university")
            user_obj.Skills = request.POST.get("Skills")
            user_obj.area = request.POST.get("area")
            user_obj.phone = request.POST.get("phone")
            user_obj.description = request.POST.get("description")
            user_obj.designation = request.POST.get("designation")
            user_obj.experience = request.POST.get("experience")
            user_obj.role = request.POST.get("role")
            user_obj.status = request.POST.get("status")
            user_obj.save()
            messages.success(request, "User Update Successfully !!")
            return redirect('update_surveyor', id=id)

        context ={
            "user": user_obj,
            "isact_surveyorlist": "active",
            "title": "Update Data Collector"
        }
        return render(request, "surveyor/surveyor_update.html", context)
    else:
        return redirect('login')


def remove_surveyor(request, id):
    obj = get_object_or_404(Surveyor, id=id)
    obj.delete()
    messages.success(request, "Requested User Delete Successfully !!")
    return redirect('surveyor_list', 'None')


def register_surveyor(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fname = request.POST.get('fname', )
            lname = request.POST.get('lname', )
            uname = request.POST.get('uname', )
            password = request.POST.get('password', )
            address = request.POST.get("address")
            profile_picture = request.FILES.get("profile_picture")
            country = request.POST.get("country")
            division = request.POST.get("division")
            district = request.POST.get("district")
            sub_district = request.POST.get("sub_district")
            email = request.POST.get("email")
            area = request.POST.get("area")
            phone = request.POST.get("phone")
            designation = request.POST.get("designation")
            experience = request.POST.get("experience")
            description = request.POST.get("description")
            graduation_subject = request.POST.get("graduation_subject")
            university = request.POST.get("university")
            user = User.objects.all().filter(username=uname)
            if user :
                messages.success(request, "User Already Exits")
                return redirect('register_surveyor')
            else :
                auth_info={
                    'first_name': fname,
                    'last_name': lname,
                    'username': uname,
                    'password': make_password(password),
                }
                user = User(**auth_info)
                user.save()
            user_obj = Surveyor(experience=experience,university=university,description=description,graduation_subject=graduation_subject,user=user,address=address,profile_picture=profile_picture,country=country,division=division,
                                district=district,sub_district=sub_district,email=email,area=area,
                                phone=phone,designation=designation)
            user_obj.save()
            messages.success(request, "Data Collector Create Successfully !!")
        context = {
            "isact_registersurveyor": "active",
            "title": "Register Data Collector"
        }
        return render(request, "surveyor/register_surveyor.html", context)
    else:
        return redirect('login')


def stock_list(request):
    obj = Stock.objects.all().filter(is_delete=False)
    context={
        "obj": obj,
        "isact_stocklist":"active"
    }
    return render(request, "stock/stock_list.html",context)


def stock_remove(request, id):
    obj = get_object_or_404(Stock, id=id)
    obj.is_delete = True
    obj.save()
    messages.success(request, "Stock Remove successfully!!")
    return redirect('stock_list')


class AddNewStock(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context={
            "isact_addnewstock":"active"
        }
        return render(request, "stock/add_new_stock.html", context)

    def post(self,request):
        product_name = request.POST.get("product_name")
        quantity = request.POST.get("quantity")
        unit_price = request.POST.get("unit_price")
        user = request.user
        obj = Stock(product_name=product_name,quantity=quantity,unit_price=unit_price,user=user)
        obj.save()
        messages.success(request, "Stock Added Successfully ")
        return redirect('stock_list')



class Update(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, id):
        obj = get_object_or_404(Stock, id=id)
        obj.product_name = request.POST.get("product_name")
        obj.quantity = request.POST.get("quantity")
        obj.unit_price = request.POST.get("unit_price")
        obj.save()
        messages.success(request, "Stock Update Successfully ")
        return redirect('stock_list')


def sell_list(request):
    obj = Sell.objects.all().filter(is_delete=False)[::-1]
    context={
        "obj":obj,
        "isact_sellslist":"active"
    }
    return render(request, "sell/sell_list.html", context)


def sell_remove(request, id):
    obj = get_object_or_404(Sell, id=id)
    obj.is_delete = True
    obj.save()
    messages.success(request, "Sell Remove successfully!!")
    return redirect('sell_list')


class AddNewSells(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context={
            "isact_addnewsells":"active"
        }
        return render(request, "sell/add_new_sells.html", context)

    def post(self,request):
        product_name = request.POST.get("product_name")
        buy_price = request.POST.get("buy_price")
        quantity = request.POST.get("quantity")
        sell_price = request.POST.get("sell_price")
        user = request.user
        obj = Sell(product_name=product_name,quantity=quantity,buy_price=buy_price,user=user,sell_price=sell_price)
        obj.save()
        messages.success(request, "Sells Added Successfully ")
        return redirect('sell_list')