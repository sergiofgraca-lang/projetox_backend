from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Visita


# 🔥 FUNÇÃO para pegar IP real (Railway / proxy)
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    
    return request.META.get('REMOTE_ADDR')


# 🔥 API (usada pelo React)
from django.shortcuts import render
from django.http import JsonResponse
from .models import Visita
from django.utils import timezone
from datetime import timedelta


def contar_visitas(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # evita múltiplas visitas do mesmo IP em 1h
    uma_hora_atras = timezone.now() - timedelta(hours=1)

    if not Visita.objects.filter(ip=ip, data__gte=uma_hora_atras).exists():
        Visita.objects.create(ip=ip)

    total = Visita.objects.count()

    return JsonResponse({
        "total": total
    })


# 🔥 PÁGINA HTML (painel bonito)
def painel_analytics(request):
    total = Visita.objects.count()

    agora = timezone.now()
    ontem = agora - timedelta(days=1)

    ultimas_24h = Visita.objects.filter(data__gte=ontem).count()

    unicos = Visita.objects.values('ip').distinct().count()

    context = {
        "total": total,
        "ultimas_24h": ultimas_24h,
        "unicos": unicos
    }

    return render(request, "analytics/painel.html", context)


# 🔥 Página simples (dashboard básico)
def pagina_visitas(request):
    # pega IP real (Railway / produção)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # 🔥 salva visita
    Visita.objects.create(ip=ip)

    # 🔥 total atualizado
    total = Visita.objects.count()

    return render(request, "dashboard.html", {
        "total": total
    })