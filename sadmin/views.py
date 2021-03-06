from django.db.models import Sum
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views import View
from .models import Surveyor, Stock, Sell, Notification, Cost
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from .utils import today,current_month,current_year

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
        day = today()
        month = current_month()
        year = current_year()
        total_user = Surveyor.objects.all().count()
        total_stock = Stock.objects.all().filter(is_delete=False).aggregate(Sum('quantity'))['quantity__sum']
        total_sell = Sell.objects.all().filter(is_delete=False).aggregate(Sum('quantity'))['quantity__sum']
        if total_stock is None:
            total_stock = 0
        if total_sell is None:
            total_sell = 0
        stock = int(total_stock - total_sell)

        daily_stock = Stock.objects.all().filter(created_date=day).aggregate(Sum('quantity'))['quantity__sum']
        if daily_stock is None:
            daily_stock = 0
        monthly_stock = Stock.objects.all().filter(created_date__month=month).aggregate(Sum('quantity'))['quantity__sum']
        if monthly_stock is None:
            monthly_stock = 0
        yearly_stock = Stock.objects.all().filter(created_date__year=year).aggregate(Sum('quantity'))['quantity__sum']
        if yearly_stock is None:
            yearly_stock = 0
        daily_sell = Sell.objects.all().filter(created_date=day).aggregate(Sum('quantity'))['quantity__sum']
        if daily_sell is None:
            daily_sell = 0
        monthly_sell = Sell.objects.all().filter(created_date__month=month).aggregate(Sum('quantity'))['quantity__sum']
        if monthly_sell is None:
            monthly_sell = 0
        yearly_sell = Sell.objects.all().filter(created_date__year=year).aggregate(Sum('quantity'))['quantity__sum']
        if yearly_sell is None:
            yearly_sell = 0

        context={
            "day":day,
            "month":month,
            "year":year,
            "isact_home":"active",
            "total_user":total_user,
            "title": "Dashboard",
            "total_stock":total_stock,
            "total_sell":total_sell,
            "daily_stock":daily_stock,
            "monthly_stock": monthly_stock,
            "yearly_stock": yearly_stock,
            "daily_sell": daily_sell,
            "monthly_sell": monthly_sell,
            "yearly_sell": yearly_sell,
            'stock':stock,




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
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            designation = request.POST.get("designation")
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
            user_obj = Surveyor(user=user,address=address,profile_picture=profile_picture,email=email,
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
        user_name = request.user
        obj = Stock(product_name=product_name,quantity=quantity,unit_price=unit_price,user=user_name)
        notification_message = ('New Stock Notification from user. please check stock.\nproduct name :'+product_name + '\nQuantity:' + quantity + '\nUnit Price :' + unit_price)

        noti_obj = Notification(notification_message=notification_message)
        noti_obj.save()
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
        total_stock = Stock.objects.all().filter(is_delete=False).aggregate(Sum('quantity'))['quantity__sum']
        total_sell = Sell.objects.all().filter(is_delete=False).aggregate(Sum('quantity'))['quantity__sum']
        if total_stock is None:
            total_stock = 0
        if total_sell is None:
            total_sell = 0
        stock = int (total_stock - total_sell)
        context={
            "isact_addnewsells":"active",
            "stock":stock
        }
        return render(request, "sell/add_new_sells.html", context)

    def post(self,request):
        total_stock = Stock.objects.all().filter(is_delete=False).aggregate(Sum('quantity'))['quantity__sum']
        total_sell = Sell.objects.all().filter(is_delete=False).aggregate(Sum('quantity'))['quantity__sum']
        if total_stock is None:
            total_stock = 0
        if total_sell is None:
            total_sell = 0
        stock = int (total_stock - total_sell)
        product_name = request.POST.get("product_name")
        buy_price = request.POST.get("buy_price")
        quantity = request.POST.get("quantity")
        sell_price = request.POST.get("sell_price")
        note = request.POST.get("note")
        user = request.user
        current_quantity = int(quantity)
        if current_quantity > stock:
            messages.warning(request, "Your current stock quantity is low please input the correct value")
            return redirect('add_new_sells')
        else:
            obj = Sell(product_name=product_name,note=note,quantity=quantity,buy_price=buy_price,user=user,sell_price=sell_price)
            notification_message = ('Sell Notification from user. please check Sell.\nproduct name :' + product_name + '\nQuantity:' + quantity + '\nSell Price :' + sell_price +'\nNote:' + note )
            noti_obj = Notification(notification_message=notification_message)
            noti_obj.save()

            obj.save()
            messages.success(request, "Sells Added Successfully ")
            return redirect('sell_list')


def sell_details(request, id):
    obj = get_object_or_404(Sell, id=id)
    context={
        "obj":obj
    }
    return render(request, "sell/sell_view.html", context)


def notification_list(request):
    noti_obj = Notification.objects.all()[::-1]
    context={
        "notification":noti_obj,
        "isact_notifications": "active"
    }
    return render(request, 'notification/notification_list.html', context)


def notification_remove(request, id):
    obj = get_object_or_404(Notification, id=id)
    obj.delete()
    return redirect('notification_list')


def cost_list(request):
    cost_obj = Cost.objects.all()[::-1]
    context={
        "isact_cost":"active",
        "cost":cost_obj
    }
    return render(request, "cost/cost_list.html", context)


def add_new_cost(request):
    context = {
        "isact_cost": "active",
    }
    if request.method == "POST":
        name = request.POST.get("name")
        purpose = request.POST.get("purpose")
        amount = request.POST.get("amount")
        amount_obj = Cost(created_by=name, purpose=purpose,amount=amount)
        amount_obj.save()
        messages.success(request, "Cost item created successfully !!")
        return redirect('cost_list')
    return render(request, "cost/add_new_cost.html", context)


def cost_update(request, id):
    obj = get_object_or_404(Cost, id=id)
    context={
        "obj":obj
    }
    if request.method == "POST":
        obj.name = request.POST.get("name")
        obj.purpose = request.POST.get("purpose")
        obj.amount = request.POST.get("amount")
        obj.save()
        messages.success(request, "Cost item update successfully !!")
        return redirect('cost_list')

    return render(request, "cost/cost_update.html", context)


def cost_remove(request, id):
    obj = get_object_or_404(Cost, id=id)
    obj.delete()
    messages.success(request, "Cost Item Delete Successfully !!")
    return redirect('cost_list')