from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Alimony, MustPayReceipt
from .forms import AddAlimonyForm
from django.db.models import Sum


class AlimonyList(ListView):
    model = Alimony
    template_name = 'report/alimony-list.html'
    context_object_name = 'alimony'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['total'] = Alimony.objects.annotate(total=Sum('must_pay__mustpayreceipt__last_payment'))
        summ = MustPayReceipt.objects.aggregate(total=Sum('last_payment'))
        context['receipt_total'] = MustPayReceipt.objects.all()\
        .select_related('must_pay')
        print('=================================')
        for item in context['receipt_total']:
            # print(item.last_payment_date1)

            print(item.must_pay.first_name)
            print(item.must_pay.receipt_total)
            print(item.must_pay.alimony.category)
            print(item.must_pay.alimony.recipient)
        print('=================================')
        return context


class AlimonyDetail(DetailView):
    model = Alimony
    context_object_name = 'alimony'
    template_name = 'report/alimony-detail.html'


class CreateAlimony(CreateView):
    form_class = AddAlimonyForm
    template_name = 'report/alimony-add.html'



