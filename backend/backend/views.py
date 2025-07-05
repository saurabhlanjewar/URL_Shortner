import pyshorteners
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def shorten_url(request):
    """
    Shortens a given URL using the TinyURL service.
    """
    if request.method == "POST":
        original_url = request.POST.get("url")
        if original_url:
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(original_url)
            return render(
                request,
                "shorten_url.html",
                {"short_url": short_url, "url": original_url},
            )
    return render(request, "shorten_url.html")


@login_required
def custom_shorten_url(request):
    """
    Shortens a given URL using the TinyURL service with a custom alias.
    """
    if request.method == "POST":
        original_url = request.POST.get("url")
        custom_alias = request.POST.get("custom_alias")
        if original_url and custom_alias:
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(original_url)
            short_url = f"{short_url}/{custom_alias}"
            return render(
                request,
                "custom_shorten_url.html",
                {"short_url": short_url, "url": original_url},
            )
    return render(request, "custom_shorten_url.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("shorten_url")  # Redirect to your home page or desired URL
        else:
            # Handle invalid login
            return render(
                request, "login.html", {"error_message": "Invalid credentials"}
            )
    return render(request, "login.html")
