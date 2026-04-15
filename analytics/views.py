from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Visita


# 🔥 API (usada pelo React)
def contar_visitas(request):
    ip = request.META.get('REMOTE_ADDR')

    # salva cada visita
    Visita.objects.create(ip=ip)

    total = Visita.objects.count()

    ontem = datetime.now() - timedelta(days=1)
    ultimas_24h = Visita.objects.filter(data__gte=ontem).count()

    unicos = Visita.objects.values('ip').distinct().count()

    return JsonResponse({
        "total": total,
        "ultimas_24h": ultimas_24h,
        "unicos": unicos
    })


# 🔥 PÁGINA HTML (painel)
def painel_analytics(request):
    total = Visita.objects.count()

    ontem = datetime.now() - timedelta(days=1)
    ultimas_24h = Visita.objects.filter(data__gte=ontem).count()

    unicos = Visita.objects.values('ip').distinct().count()

    context = {
        "total": total,
        "ultimas_24h": ultimas_24h,
        "unicos": unicos
    }

    return render(request, "analytics/painel.html", context)