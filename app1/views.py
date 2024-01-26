from django.shortcuts import render,redirect
from .models import *
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

def login(request):
    if request.method == "POST":
        user = Admin.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['user_id']=logged_user.id
                    request.session['username']=logged_user.fname
                    if logged_user.type=='admin':
                        request.session['type']='admin'
                    elif logged_user.type=='user':
                        request.session['type']='user'
                    return redirect('/main')
            else:
                return redirect ('/')

        else:
            return redirect ('/')
    else:
        return render(request,'login.html')
    
def registration(request):
    if request.method == "POST":
        errors = Admin.objects.basic_validator1(request.POST)
        if len(errors) > 0 :
            return redirect('/')
        else:
            this_setting=Cost.objects.filter(id=1)
            if this_setting:
                this_setting=this_setting[0]
                if this_setting.admin_code==request.POST['code']:
                    hash1= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
                    registered_user = Admin.objects.create(
                        fname=request.POST['fname'],
                        lname=request.POST['lname'],
                        email=request.POST['email'],
                        password=hash1,
                        type='admin'
                        )
                    messages.success(request, "Registered successfully")
                    request.session['user_id']=registered_user.id
                    request.session['username']=registered_user.fname
                    request.session['type']='admin'
                    return redirect('/main')
                elif this_setting.user_code==request.POST['code']:
                    hash1= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
                    registered_user = Admin.objects.create(
                        fname=request.POST['fname'],
                        lname=request.POST['lname'],
                        email=request.POST['email'],
                        password=hash1,
                        type='user'
                        )
                    messages.success(request, "Registered successfully")
                    request.session['user_id']=registered_user.id
                    request.session['username']=registered_user.fname
                    request.session['type']='user'
                    return redirect('/main')
                else:
                    return redirect('/')
            else:
                this_setting=Cost.objects.create()
                return redirect('/')
    else:
        return render(request,'login.html')

def change_admin_setting(request):
    if 'type' in request.session and request.session['type']=='admin':
        this_setting=Cost.objects.filter(id=1)
        if this_setting:
            this_setting=this_setting[0]
            this_setting.monthly_fee=request.POST['monthly_fee']
            this_setting.daily_fee=request.POST['daily_fee']
            this_setting.admin_code=request.POST['admin_code']
            this_setting.user_code=request.POST['user_code']
            this_setting.save()
            return redirect('/main')
        else:
            return redirect('/')
    else:
        return redirect('/')
def main(request):
    if 'type' in request.session:
        number=0
        active=0
        empty=0
        for member in Member.objects.all():
            if not member.is_payed() or member.is_expired():
                number+=1
        for member in Member.objects.all():
            if member.is_expired()== False:
                active+=1
        for item in Item.objects.all():
            if item.is_empty():
                empty+=1
        this_user=Admin.objects.get(id=request.session['user_id'])
        context={
        'count':number,
        'member_count':Member.objects.all(),
        'active':active,
        'allitem':Item.objects.all(),
        'empty':empty,
        'setting':Cost.objects.get(id=1),
        'user':this_user
        }
        return render(request,'main.html',context)
    else:
        return redirect('/')
def add_member(request):
    if 'type' in request.session:
        if request.method == "POST":
            this_admin=Admin.objects.get(id=request.session['user_id'])
            this_member = Member.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                mobile=request.POST['mobile'],
                membership_type=request.POST['acc_type'],
                payed_amount=request.POST['payed_amount'],
                added_by=this_admin,
                address=request.POST['address'],
                )
            if len(request.FILES) != 0:
                this_member.avatar=request.FILES['img']
            if len(request.POST['date_start'])==0:
                this_member.start_membership_date=timezone.now()
            else:
                this_member.start_membership_date=request.POST['date_start']
            if len(request.POST['date_end'])==0:
                if request.POST['acc_type']=='شهري':
                    this_member.end_membership_date=timezone.now()
                    this_member.end_membership_date=this_member.end_membership_date+relativedelta(months=1)
                else:
                    this_member.end_membership_date=timezone.now()
            else:
                this_member.end_membership_date=request.POST['date_end'],
            this_member.save()
            messages.success(request, "Registered successfully")
            return redirect('/main')
        else:
            number=0
            for member in Member.objects.all():
                if not member.is_payed() or member.is_expired():
                    number+=1
            context={
            'count':number
            }
            return render(request,'add_new_member.html',context)
    else:
        return redirect('/')
def member_profile(request,id):
    if 'type' in request.session:
        number=0
        for member in Member.objects.all():
            if not member.is_payed() or member.is_expired():
                number+=1
        this_member=Member.objects.get(id=int(id))
        context={
            'member':this_member,
            'count':number
        }
        return render(request,'member_profile.html',context)
    else:
        return redirect('/')

def member_list(request):
    if 'type' in request.session and request.session['type']=='admin':
        number=0
        for member in Member.objects.all():
            print(member.is_payed)
            if not member.is_payed() or member.is_expired():
                number+=1
        context={
            'all_member':Member.objects.all(),
            'count':number
        }
        return render(request,'member_list.html',context)
    else:
        return redirect('/')
def note(request):
    if 'type' in request.session:
        number=0
        for member in Member.objects.all():
            if not member.is_payed() or member.is_expired():
                number+=1
        context={
            'allmember':Member.objects.all(),
            'count':number
        }
        return render(request,'note.html',context)
    else:
        return redirect('/')
def view_items(request):
    if 'type' in request.session:
        number=0
        for member in Member.objects.all():
            if not member.is_payed() or member.is_expired():
                number+=1
        context={
            'count':number,
            'all_item':Item.objects.all()
        }
        return render(request,'view_items.html',context)
    else:
        return redirect('/')
def add_items(request):
    if 'type' in request.session:
        if request.method=='POST':
            this_admin=Admin.objects.get(id=request.session['user_id'])
            this_product=Item.objects.create(
            title=request.POST['title'],
            total_quantity=request.POST['total_quantity'],
            available_quantity=request.POST['total_quantity'],
            price=request.POST['price'],
            added_by=this_admin
            )
            if len(request.FILES)!=0:
                this_product.item_image=request.FILES['item_image']
                this_product.save()
            return redirect('/main')
        else:
            number=0
            for member in Member.objects.all():
                if not member.is_payed() or member.is_expired():
                    number+=1
            context={
                'count':number
            }
            return render(request,'add_items.html',context)
    else:
        return redirect('/')
def delete(request,id):
    if 'type' in request.session:
        this_member=Member.objects.get(id=int(id))
        this_member.delete()
        return redirect('/main')
    else:
        return redirect('/')
def update_member(request,id):
    if 'type' in request.session:
        this_member=Member.objects.get(id=int(id))
        this_member.fname=request.POST['fname']
        this_member.lname=request.POST['lname']
        this_member.mobile=request.POST['mobile']
        this_member.membership_type=request.POST['membership_type']
        if len(request.POST['start_membership_date'])>0:
            this_member.start_membership_date=request.POST['start_membership_date']
        if len(request.POST['end_membership_date'])>0:
            this_member.end_membership_date=request.POST['end_membership_date']
        this_member.payed_amount=request.POST['payed_amount']
        this_member.address=request.POST['address']
        if 'img' in request.FILES:
            this_member.avatar=request.FILES['img']
        this_member.save()
        return redirect('/main')    
    else:
        return redirect('/')
def update_member_pic(request,id):
    if 'type' in request.session:
        this_member=Member.objects.get(id=int(id))
        this_member.avatar=request.FILES['img']
        this_member.save()
        return redirect('/main')
    else:
        return redirect('/')
def renew_membership(request,id):
    if 'type' in request.session:
        this_member=Member.objects.get(id=int(id))
        this_member.start_membership_date=timezone.now()
        this_member.payed_amount=request.POST['payed_amount']
        if this_member.membership_type=='شهري':
            this_member.end_membership_date=this_member.start_membership_date+relativedelta(months=1)
        else:
            this_member.end_membership_date=timezone.now()
        this_member.save()
        return redirect('/main')
    else:
        return redirect('/')
def add_remove_item(request,operation,id):
    if 'type' in request.session:
        this_item=Item.objects.get(id=int(id))
        if int(operation)==1:
            this_item.total_quantity+=1
            this_item.available_quantity=this_item.total_quantity-this_item.sold_quantity
            this_item.save()
            return redirect('/view_items')

        if int(operation)==0:
            this_item.sold_quantity+=1
            this_item.available_quantity=this_item.total_quantity-this_item.sold_quantity
            this_item.save()
            return redirect('/view_items')
    else:
        return redirect('/')
def item_profile(request,id):
    if 'type' in request.session:
        if request.method=='POST':
            this_item=Item.objects.get(id=int(id))
            this_item.title=request.POST['title']
            this_item.total_quantity=request.POST['total_quantity']
            this_item.available_quantity=request.POST['available_quantity']
            this_item.sold_quantity=request.POST['sold_quantity']
            this_item.price=request.POST['price']
            this_item.save()
            if len(request.FILES)!=0:
                this_item.item_image=request.FILES['item_image']
                this_item.save()
            return redirect('/view_items')
        else:

            number=0
            for member in Member.objects.all():
                if not member.is_payed() or member.is_expired():
                    number+=1
            this_item=Item.objects.get(id=int(id))
            context={
                'item':this_item,
                'count':number
            }
            return render(request,'item_profile.html',context)
    else:
        return redirect('/')
    
def search(request):
    search = Member.objects.filter(fname__contains=request.POST['search_ajax1'])
    if search:
        context={
            'member':search.all(),
        }
    return render(request,'search_ajax.html',context)

def delete_item(request,id):
    if 'type' in request.session:
        this_item=Item.objects.get(id=int(id))
        this_item.delete()
        return redirect('/view_items')
    else:
        return redirect('/')
def logout(request):
    if 'type' in request.session:
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')