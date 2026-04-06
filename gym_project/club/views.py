from django.shortcuts import render, redirect, get_object_or_404
from .models import Subscription, Client, Service
from .forms import ClientForm
from django.db.models import Sum, Q
from datetime import date
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import os
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def index(request):
    delete_id = request.GET.get('delete')
    if delete_id:
        get_object_or_404(Client, id=delete_id).delete()
        return redirect('index')

    service_id = request.POST.get('service_id')
    new_price = request.POST.get('new_price')
    if service_id and new_price:
        service = get_object_or_404(Service, id=service_id)
        service.price = new_price
        service.save()
        return redirect('index')

    if request.method == 'POST' and not service_id:
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            selected_service = form.cleaned_data.get('service')
            Subscription.objects.create(
                client=client,
                service=selected_service,
                price_at_purchase=selected_service.price, # Заморозка цены
                start_date=date.today(),
                is_active=True
            )
            return redirect('index')
    else:
        form = ClientForm()

    search_query = request.GET.get('search', '')
    subscriptions_queryset = Subscription.objects.all()
    if search_query:
        subscriptions_queryset = subscriptions_queryset.filter(Q(client__full_name__icontains=search_query))

    subs_with_status = []
    today = date.today()
    for sub in subscriptions_queryset:
        days_passed = (today - sub.start_date).days
        sub.status_expired = days_passed > 30
        subs_with_status.append(sub)

    services = Service.objects.all()
    total_clients = Client.objects.count()
    total_revenue = Subscription.objects.aggregate(Sum('price_at_purchase'))['price_at_purchase__sum'] or 0

    context = {
        'subscriptions': subs_with_status,
        'form': form,
        'services': services,
        'total_clients': total_clients,
        'total_revenue': total_revenue,
        'search_query': search_query,
    }
    return render(request, 'club/index.html', context)


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="gym_report.pdf"'

    font_path = "C:\\Windows\\Fonts\\arial.ttf"

    pdfmetrics.registerFont(TTFont('ArialCustom', font_path))

    p = canvas.Canvas(response)

    p.setFont('ArialCustom', 14)
    p.drawString(100, 800, "Отчет по продажам клуба")

    p.setFont('ArialCustom', 10)
    y = 750
    for sub in Subscription.objects.all():
        line = f"{sub.client.full_name} | {sub.service.name} | {sub.price_at_purchase} руб."
        p.drawString(100, y, line)
        y -= 20

    p.showPage()
    p.save()
    return response