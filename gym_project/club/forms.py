from django import forms
from .models import Client, Service, Subscription

class ClientForm(forms.ModelForm):
    # Добавляем поле, которого нет в модели Client, чтобы сразу создать абонемент
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        label="Выберите услугу",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Client
        fields = ['full_name', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'}),
        }