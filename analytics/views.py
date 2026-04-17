from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Visita


# 🔥 Função para pegar IP real (Railway / proxy)
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    
    return request.META.get('REMOTE_ADDR')


# 🔥 API (usada pelo React → ESSA É A ÚNICA QUE CONTA VISITA)
def contar_visitas(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

    # 🔥 bloqueio leve (apenas bots óbvios)
    if 'bot' in user_agent or 'spider' in user_agent:
        return JsonResponse({"status": "bot ignorado"})

    # pega IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # 🔥 limite simples (evita spam)
    from django.utils import timezone
    from datetime import timedelta

    agora = timezone.now()
    limite = agora - timedelta(minutes=5)

    if not Visita.objects.filter(ip=ip, data__gte=limite).exists():
        Visita.objects.create(ip=ip)

    total = Visita.objects.count()

    return JsonResponse({
        "total": total
    })

# 🔥 Painel completo (analytics)
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


# 🔥 Dashboard simples (NÃO CONTA VISITA)
def pagina_visitas(request):
    total = Visita.objects.count()

    return render(request, "dashboard.html", {
        "total": total
    })