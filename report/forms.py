from django import forms
from .models import Category, MustPay, MustPayReceipt, Recipient, Alimony, Currency, RecipientChild


class AddAlimonyForm(forms.ModelForm):
    class Meta:
        model = Alimony
        fields = '__all__'
        # fields = ['executor', 'executor_1', 'must', 'recipient', 'summ_money', 'paid_money', 'last_payment', 'valute', 'comment']
        # widgets = {
        #     'executor': forms.TextInput(attrs={'class': 'form-control'}),
        #     'executor_1': forms.TextInput(attrs={'class': 'form-control'}),
        #     'must': forms.TextInput(attrs={'class': 'form-control'}),
        #     'recipient': forms.TextInput(attrs={'class': 'form-control'}),
        #     'summ_money': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'paid_money': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'last_payment': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'valute': forms.TextInput(attrs={'class': 'form-control'}),
        #     'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        # }