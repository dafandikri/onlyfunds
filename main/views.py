from django.shortcuts import render, redirect, reverse
from main.forms import ItemEntryForm
from main.models import ItemEntry
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@login_required(login_url='/login')
def show_main(request):

    context = {
        'name': request.user.username,
        'class': 'PBP C',
        'npm': '2306244993',
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def create_item_entry(request):
    form = ItemEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        item_entry = form.save(commit=False)
        item_entry.user = request.user
        item_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_item_entry.html", context)

def show_xml(request):
    data = ItemEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = ItemEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = ItemEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = ItemEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_item(request, id):
    # Get item entry berdasarkan id
    item = ItemEntry.objects.get(pk = id)

    # Set item entry sebagai instance dari form
    form = ItemEntryForm(request.POST or None, instance=item)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_item.html", context)

def delete_item(request, id):
    # Get item berdasarkan id
    item = ItemEntry.objects.get(pk = id)
    # Hapus item
    item.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def add_item_entry_ajax(request):
    name = strip_tags(request.POST.get("name")) # strip HTML tags!
    description = strip_tags(request.POST.get("description")) # strip HTML tags!
    price = request.POST.get("price")
    bank = strip_tags(request.POST.get("bank")) # strip HTML tags!
    user = request.user

    new_item = ItemEntry(
        name=name, description=description, price=price, bank=bank, user=user
    )
    new_item.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
def create_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_item = ItemEntry.objects.create(
            user=request.user,
            name=data["name"],
            description=data["description"],
            price=int(data["price"]),
            bank=data["bank"]
        )
        new_item.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)