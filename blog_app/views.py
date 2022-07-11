from django.shortcuts import render
import os
if os.path.isfile("env.py"):
    import env
# Create your views here.

def index(request):
    return render(request, 'index.html')
