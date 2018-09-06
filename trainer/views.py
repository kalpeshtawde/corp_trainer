from django.http import HttpResponse

def index(request):
    return HttpResponse("<H1>Corporate Trainer</H1>")

def name(request):
    return HttpResponse("<H1>Corporate Trainer: Kalpesh Tawde</H1>")