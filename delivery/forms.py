from django import forms
from .models import DeliveryAddress


class DeliveryAddressForm(forms.ModelForm):
    """Форма добавления адреса доставки с чекбоксом квартиры"""
    
    # Выпадающий список городов
    city = forms.ChoiceField(
        choices=[],  # Будет заполнено в __init__
        label='Город / Населенный пункт',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = DeliveryAddress
        fields = ['city', 'street', 'house', 'apartment', 'entrance', 'floor']
        labels = {
            'street': 'Улица',
            'house': 'Дом',
            'apartment': 'Квартира',
            'entrance': 'Подъезд',
            'floor': 'Этаж',
        }
        widgets = {
            'street': forms.TextInput(attrs={'placeholder': 'Название улицы'}),
            'house': forms.TextInput(attrs={'placeholder': 'Номер дома'}),
            'apartment': forms.TextInput(attrs={'placeholder': 'Номер квартиры'}),
            'entrance': forms.TextInput(attrs={'placeholder': 'Номер подъезда'}),
            'floor': forms.TextInput(attrs={'placeholder': 'Этаж'}),
        }
        help_texts = {
            'apartment': 'Необязательное поле',
            'entrance': 'Необязательное поле',
            'floor': 'Необязательное поле',
        }

    def __init__(self, *args, **kwargs):
        from .cities import MAIN_CITIES
        super().__init__(*args, **kwargs)
        # Заполняем список городов
        self.fields['city'].choices = MAIN_CITIES

    def clean_street(self):
        street = self.cleaned_data.get('street')
        if not street or len(street.strip()) < 2:
            raise forms.ValidationError('Улица должна содержать минимум 2 символа')
        return street.strip()

    def clean_house(self):
        house = self.cleaned_data.get('house')
        if not house or len(house.strip()) < 1:
            raise forms.ValidationError('Номер дома обязателен')
        return house.strip()

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Формируем полный адрес
        full_address = f"{instance.city}, {instance.street}, д. {instance.house}"
        if instance.apartment:
            full_address += f", кв. {instance.apartment}"
        instance.full_address = full_address
        if commit:
            instance.save()
        return instance


class CheckoutAddressForm(forms.ModelForm):
    """Форма адреса для оформления заказа (автоматическое привязывание к пользователю)"""
    
    # Дополнительные поля для данных пользователя
    first_name = forms.CharField(
        label='Имя',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'})
    )
    last_name = forms.CharField(
        label='Фамилия',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'})
    )
    phone = forms.CharField(
        label='Телефон',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Ваш email'})
    )
    
    city = forms.ChoiceField(
        choices=[],
        label='Город / Населенный пункт',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    save_to_profile = forms.BooleanField(
        label='Сохранить этот адрес в профиль',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'checked': True})
    )
    comment = forms.CharField(
        label='Комментарий к заказу',
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Дополнительная информация', 'rows': 4})
    )
    
    class Meta:
        model = DeliveryAddress
        fields = ['city', 'street', 'house', 'apartment', 'entrance', 'floor', 'save_to_profile']
        labels = {
            'street': 'Улица',
            'house': 'Дом',
            'apartment': 'Квартира',
            'entrance': 'Подъезд',
            'floor': 'Этаж',
        }
        widgets = {
            'street': forms.TextInput(attrs={'placeholder': 'Название улицы'}),
            'house': forms.TextInput(attrs={'placeholder': 'Номер дома'}),
            'apartment': forms.TextInput(attrs={'placeholder': 'Номер квартиры'}),
            'entrance': forms.TextInput(attrs={'placeholder': 'Номер подъезда'}),
            'floor': forms.TextInput(attrs={'placeholder': 'Этаж'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .cities import MAIN_CITIES
        self.fields['city'].choices = MAIN_CITIES

    def clean_street(self):
        street = self.cleaned_data.get('street')
        if not street or len(street.strip()) < 2:
            raise forms.ValidationError('Улица должна содержать минимум 2 символа')
        return street.strip()

    def clean_house(self):
        house = self.cleaned_data.get('house')
        if not house or len(house.strip()) < 1:
            raise forms.ValidationError('Номер дома обязателен')
        return house.strip()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('Телефон обязателен')
        return phone.strip()
