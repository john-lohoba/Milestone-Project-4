from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    """
    A view to render the index page
    """
    if request.user.is_authenticated:
        return redirect("backtest-list")
    
    else:
        return render(request, "home/index.html")
