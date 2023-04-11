from django.shortcuts import render
from django.http import HttpResponse

import publica

def Bienvenidos_RN(request):
    return render(request,'publica/index.html', {"titulo":"Reservas Naturales"}) 

