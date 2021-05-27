from django.shortcuts import render

def home(request):
    data = {}
    data['usuario'] = request.user
    return render(request, 'base/index.html', data)
