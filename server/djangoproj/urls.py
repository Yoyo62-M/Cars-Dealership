from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def home(request):
    user = request.user
    if user.is_authenticated:
        username = user.username
        user_info = f"<p>Welcome, <strong>{username}</strong> | <a href='/djangoapp/logout'>Logout</a></p>"
        review_link = "<a href='/djangoapp/reviews/dealer/1'>Review Dealer</a>"
    else:
        user_info = "<p><a href='/admin/'>Login</a></p>"
        review_link = "<a href='/admin/'>Login to Review</a>"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Car Dealership</title>
    </head>
    <body>
      {user_info}
      <h1>Welcome to Best Cars Dealership</h1>
      <nav>
        <a href="/">Home</a> |
        <a href="/djangoapp/get_dealers/">All Dealers</a> |
        <a href="/djangoapp/get_dealers/Kansas">Dealers in Kansas</a> |
        {review_link}
      </nav>
      <h2>Our Dealers</h2>
      <ul>
        <li><a href="/djangoapp/dealer/1">John Dealer - Wichita, Kansas</a></li>
        <li><a href="/djangoapp/dealer/2">Jane Motors - Topeka, Kansas</a></li>
        <li><a href="/djangoapp/dealer/3">Bob Cars - Austin, Texas</a></li>
      </ul>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('', home),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)