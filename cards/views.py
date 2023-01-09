from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.utils import timezone
from .models import BonusCard, Purchase
from django.views.generic.detail import DetailView
import datetime as dt


class CardDetail(DetailView):
    model = BonusCard
    template_name = 'cards/card_detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'card'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        context['all_purchase'] = Purchase.objects.filter(card__pk=pk)
        return context

    def post(self, request, *args, **kwargs):
        if "delete" in request.POST:
            self.object = self.get_object()
            self.object.delete()
            return redirect('all')
        elif "activate" in request.POST:
            self.object = self.get_object()
            self.object.status = 'Activated'
            self.object.save()
            return redirect('all')
        elif "deactivate" in request.POST:
            self.object = self.get_object()
            self.object.status = 'Not activated'
            self.object.save()
            return redirect('all')


def Check_is_active(request):
    objs = BonusCard.objects.filter(expiry__lt=timezone.now())
    for obj in objs:
        obj.status = 'Disabled'
        obj.save()
    all = list(BonusCard.objects.all())
    return render(request, "cards/all.html", {'title': 'All cards', 'all_cards': all})


def is_valid_queryparam(param):
    return param != '' and param is not None


def SearchCard(request):
    cards = BonusCard.objects.all()
    search_query = request.GET.get('search', '')
    number = request.GET.get('number')
    pk = request.GET.get('pk')
    date_time = request.GET.get('date_time')
    expiry = request.GET.get('expiry')
    status = request.GET.get('status')
    context = {}
    context['status'] = ['Activated','Disabled','Not activated']

    if is_valid_queryparam(status) and status != 'Выбрать...':
        cards = cards.filter(status=status)

    if search_query:
        if expiry == 'on':
            context['expiry'] = cards.filter(expiry__icontains=search_query)

        if number == 'on':
            context['number'] = cards.filter(number__icontains=search_query)

        if pk == 'on':
            context['pk'] = cards.filter(pk__icontains=search_query)

        if date_time == 'on':
            context['date_time'] = cards.filter(date_time__icontains=search_query)

    return render(request,'cards/search.html',context=context)


def GenerateCard(request):
    context = {}
    context['expiry'] = {"1 год":dt.timedelta(days=365), "6 месяцев": dt.timedelta(days=182), "1 месяц": dt.timedelta(days=31)}
    expiry = request.GET.get('expiry')
    number = request.GET.get('number')
    count = request.GET.get('count')
    if is_valid_queryparam(number) and number.isdigit and len(number) == 16:
        if is_valid_queryparam(expiry) and expiry != 'Выбрать...':
            if count.isdigit():
                for i in range(int(count)):
                    BonusCard.objects.create(
                        number=number,
                        expiry= timezone.now() + context["expiry"][expiry],
                        sum_of_bonus= 0,
                        status= 'Not activated'
                    )
                context['warning'] = 'Карты сгенерированы'
            else:
                context['warning'] = 'Введите корректное число'
        else:
            context['warning'] = 'Выберите срок окончания активности'
    else:
        context['warning'] = 'Серия должна состоять из 16 цифр'
    return render(request,'cards/generate.html',context=context)
