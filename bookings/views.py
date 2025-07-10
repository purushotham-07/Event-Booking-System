from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import json
import hmac
import hashlib
import razorpay

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import AboutCollege, AboutPreviousVitopia, Event, Wishlist, BookedEvent

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('welcome')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def welcome(request):
    return render(request, 'welcome.html')


def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    total_price = sum(item.event.ticket_price for item in wishlist_items)
    return render(request, "wishlist.html", {
        "wishlist_items": wishlist_items,
        "total_price": total_price,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


@login_required
def add_to_wishlist(request, item_id):
    if request.method == "POST":
        event = get_object_or_404(Event, id=item_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, event=event)
        if created:
            return JsonResponse({"status": "success", "message": "Item added to wishlist!"})
        else:
            return JsonResponse({"status": "info", "message": "Item already in wishlist!"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    wishlist_item.delete()
    wishlist_items = Wishlist.objects.filter(user=request.user)
    total_price = sum(item.event.ticket_price for item in wishlist_items)
    return JsonResponse({"status": "success", "total_price": total_price})


@login_required
def create_order(request):
    if request.method == "POST":
        user = request.user
        wishlist_items = Wishlist.objects.filter(user=user)
        if not wishlist_items.exists():
            return JsonResponse({"status": "error", "message": "Wishlist is empty."}, status=400)
        total_amount = float(sum(item.event.ticket_price for item in wishlist_items)) * 100
        try:
            order = razorpay_client.order.create({
                "amount": total_amount,
                "currency": "INR",
                "payment_capture": "1"
            })
            return JsonResponse({
                "status": "success",
                "order_id": order["id"],
                "amount": total_amount
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")

            generated_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode(),
                f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                hashlib.sha256
            ).hexdigest()

            if generated_signature == razorpay_signature:
                user = request.user
                wishlist_items = Wishlist.objects.filter(user=user)
                for item in wishlist_items:
                    BookedEvent.objects.create(user=user, event=item.event, payment_id=razorpay_payment_id)
                wishlist_items.delete()

                send_mail(
                    "Event Booking Confirmation",
                    f"Hello {user.username},\n\nYour events have been booked successfully!\n\nThank you!",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "failed", "message": "Invalid signature"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required
def payment_success(request):
    return render(request, "success.html")


def about_college(request):
    about_college = AboutCollege.objects.first()
    return render(request, 'about_college.html', {'about_college': about_college})


def about_previous_vitopia(request):
    about_previous = AboutPreviousVitopia.objects.first()
    return render(request, 'about_previous.html', {'about_previous': about_previous})
