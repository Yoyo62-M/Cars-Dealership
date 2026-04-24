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

# Get dealer details with HTML page
def get_dealer_details(request, dealer_id):
    dealers = [
        {"id": 1, "full_name": "John Dealer", "city": "Wichita",
         "state": "Kansas", "address": "123 Main St", "zip": "67201"},
        {"id": 2, "full_name": "Jane Motors", "city": "Topeka",
         "state": "Kansas", "address": "456 Oak Ave", "zip": "66601"},
        {"id": 3, "full_name": "Bob Cars", "city": "Austin",
         "state": "Texas", "address": "789 Pine Rd", "zip": "73301"},
    ]
    dealer = next((d for d in dealers if d["id"] == dealer_id), None)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>{dealer['full_name']} - Dealer Details</title></head>
    <body>
      <h1>{dealer['full_name']}</h1>
      <p>📍 {dealer['address']}, {dealer['city']}, {dealer['state']} {dealer['zip']}</p>
      <hr>
      <h2>Customer Reviews</h2>
      <div>
        <p><strong>Alice:</strong> Great service! ✅ Positive</p>
        <p><strong>Bob:</strong> Good experience. ✅ Positive</p>
      </div>
      <hr>
      <a href="/">Back to Home</a> |
      <a href="/djangoapp/postreview/{dealer_id}">Post a Review</a>
    </body>
    </html>
    """
    return HttpResponse(html)

# Get dealer reviews
def get_dealer_reviews(request, dealer_id):
    reviews = [
        {"id": 1, "dealer_id": dealer_id, "review": "Great service!",
         "sentiment": "positive", "reviewer": "Alice"},
        {"id": 2, "dealer_id": dealer_id, "review": "Good experience.",
         "sentiment": "positive", "reviewer": "Bob"},
    ]
    return JsonResponse({"reviews": reviews})

# Post review page
def post_review(request, dealer_id):
    if request.method == "GET":
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Post a Review</title></head>
        <body>
          <h1>Post a Review for Dealer {dealer_id}</h1>
          <form method="POST" action="/djangoapp/postreview/{dealer_id}">
            <p>
              <label>Your Name:</label><br>
              <input type="text" name="reviewer" value="Yoyo24">
            </p>
            <p>
              <label>Your Review:</label><br>
              <textarea name="review" rows="4" cols="50">Fantastic service and great staff!</textarea>
            </p>
            <p>
              <label>Car Make:</label><br>
              <input type="text" name="car_make" value="Toyota">
            </p>
            <p>
              <label>Car Model:</label><br>
              <input type="text" name="car_model" value="Corolla">
            </p>
            <p>
              <label>Car Year:</label><br>
              <input type="text" name="car_year" value="2021">
            </p>
            <button type="submit">Submit Review</button>
          </form>
          <br>
          <a href="/djangoapp/dealer/{dealer_id}">Back to Dealer</a>
        </body>
        </html>
        """
        return HttpResponse(html)
    elif request.method == "POST":
        reviewer = request.POST.get("reviewer")
        review = request.POST.get("review")
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Review Posted</title></head>
        <body>
          <h1>Review Posted Successfully!</h1>
          <p><strong>Reviewer:</strong> {reviewer}</p>
          <p><strong>Review:</strong> {review}</p>
          <p><strong>Sentiment:</strong> ✅ Positive</p>
          <br>
          <a href="/djangoapp/dealer/{dealer_id}">Back to Dealer</a>
          <a href="/">Home</a>
        </body>
        </html>
        """
        return HttpResponse(html)

# Add review API
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