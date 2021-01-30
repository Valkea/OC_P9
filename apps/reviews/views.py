from django.shortcuts import render


def main_reviews(request):
    return render(request, 'reviews/main.html')
