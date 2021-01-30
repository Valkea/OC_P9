from django.shortcuts import render


def main_user_graph(request):
    return render(request, 'user_graph/main.html')
