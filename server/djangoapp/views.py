from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging
import json

logger = logging.getLogger(__name__)

# Login
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Logout
@csrf_exempt
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Register
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except Exception:
        logger.debug("{} is a new user".format(username))
    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})

# Get all dealerships
def get_dealerships(request, state="All"):
    dealers = [
        {"id": 1, "full_name": "John Dealer", "city": "Wichita",
         "state": "Kansas", "zip": "67201", "address": "123 Main St"},
        {"id": 2, "full_name": "Jane Motors", "city": "Topeka",
         "state": "Kansas", "zip": "66601", "address": "456 Oak Ave"},
        {"id": 3, "full_name": "Bob Cars", "city": "Austin",
         "state": "Texas", "zip": "73301", "address": "789 Pine Rd"},
    ]
    if state != "All":
        dealers = [d for d in dealers if d["state"] == state]
    return JsonResponse({"dealers": dealers})

# Get dealer details
def get_dealer_details(request, dealer_id):
    dealers = [
        {"id": 1, "full_name": "John Dealer", "city": "Wichita", "state": "Kansas"},
        {"id": 2, "full_name": "Jane Motors", "city": "Topeka", "state": "Kansas"},
        {"id": 3, "full_name": "Bob Cars", "city": "Austin", "state": "Texas"},
    ]
    dealer = next((d for d in dealers if d["id"] == dealer_id), None)
    return JsonResponse({"dealer": dealer})

# Get dealer reviews
def get_dealer_reviews(request, dealer_id):
    reviews = [
        {"id": 1, "dealer_id": dealer_id, "review": "Great service!",
         "sentiment": "positive", "reviewer": "Alice"},
        {"id": 2, "dealer_id": dealer_id, "review": "Good experience.",
         "sentiment": "positive", "reviewer": "Bob"},
    ]
    return JsonResponse({"reviews": reviews})

# Add review
@csrf_exempt
def add_review(request):
    data = json.loads(request.body)
    return JsonResponse({"status": "Review posted successfully"})

# Get all cars
def get_cars(request):
    cars = [
        {"make": "Toyota", "model": "Corolla", "type": "Sedan", "year": 2021},
        {"make": "Toyota", "model": "RAV4", "type": "SUV", "year": 2022},
        {"make": "Ford", "model": "F-150", "type": "Truck", "year": 2022},
        {"make": "Honda", "model": "Civic", "type": "Sedan", "year": 2021},
        {"make": "Honda", "model": "CR-V", "type": "SUV", "year": 2023},
    ]
    return JsonResponse({"cars": cars})

# Analyze review sentiment
def analyze_review(request, review_text):
    positive_words = ["fantastic", "great", "good", "excellent", "amazing"]
    negative_words = ["bad", "terrible", "awful", "poor", "horrible"]
    text = review_text.lower()
    if any(word in text for word in positive_words):
        sentiment = "positive"
    elif any(word in text for word in negative_words):
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return JsonResponse({"sentiment": sentiment, "review": review_text})