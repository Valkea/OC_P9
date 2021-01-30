from django.shortcuts import render


def main_auth(request):
    return render(request, 'auth/main.html')
