from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Labas, pasauli, cia mano pirmasis Django apsas!!')

