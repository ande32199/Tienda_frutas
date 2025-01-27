from django.shortcuts import render
from django.http import JsonResponse
from .models import Fruta

def obtener_frutas(request):
    frutas = Fruta.objects.all().values('id', 'nombre', 'precio', 'cantidad')
    return JsonResponse(list(frutas), safe=False)
