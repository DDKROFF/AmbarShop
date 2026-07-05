from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from .models import User, Review


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(max_length=20, required=True, label='Телефон')
    first_name = forms.CharField(max_length=150, required=True, label='Имя')
    last_name = forms.CharField(max_length=150, required=True, label='Фамилия')

    class Meta:
        model = User
        fields = ['email', 'phone', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'Email',
            'phone': 'Телефон',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        help_texts = {
            'first_name': 'Обязательное поле',
            'last_name': 'Обязательное поле',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 000-00-00'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Введите пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Подтвердите пароль'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Имя пользователя уже занято')
        if len(username) < 3:
            raise forms.ValidationError('Имя пользователя должно содержать минимум 3 символа')
        if not username.isalnum():
            raise forms.ValidationError('Имя пользователя может содержать только буквы и цифры')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email
        phone = self.cleaned_data.get('phone')
        phone_digits = ''.join(filter(str.isdigit, phone))
        if len(phone_digits) < 10:
            raise forms.ValidationError('Номер телефона слишком короткий')
        if len(phone_digits) > 11:
            raise forms.ValidationError('Номер телефона слишком длинный')
        if not phone_digits.startswith('7') and not phone_digits.startswith('8'):
            raise forms.ValidationError('Номер должен начинаться с 7 или 8')
        return phone

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов')
        if not any(c.isupper() for c in password1):
            raise forms.ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
        if not any(c.isdigit() for c in password1):
            raise forms.ValidationError('Пароль должен содержать хотя бы одну цифру')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        
        if password1 and len(password1) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов')
        
        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'required': True, 'placeholder': 'Заголовок отзыва'}),
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'required': True, 'rows': 4, 'placeholder': 'Ваш отзыв'}),
        }
        labels = {
            'rating': mark_safe('Оценка <span class="required">*</span>'),
            'title': mark_safe('Заголовок <span class="required">*</span>'),
            'comment': mark_safe('Комментарий <span class="required">*</span>'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            # Для авторизованных пользователей скрываем поля name и email
            self.fields.pop('name', None)
            self.fields.pop('email', None)


class UserProfileForm(forms.ModelForm):
    """Форма редактирования профиля"""
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Фамилия',
        widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'})
    )
    middle_name = forms.CharField(
        max_length=150,
        required=False,
        label='Отчество',
        widget=forms.TextInput(attrs={'placeholder': 'Ваше отчество'}),
        help_text='Необязательное поле'
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'middle_name', 'phone']
        labels = {
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'phone': 'Телефон',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'Ваше отчество'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 000-00-00'}),
        }
        help_texts = {
            'email': 'Используется для входа в аккаунт',
            'first_name': 'Обязательное поле',
            'last_name': 'Обязательное поле',
            'phone': 'Обязательное поле для связи',
        }


class ChangePasswordForm(forms.Form):
    """Форма смены пароля"""
    current_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите текущий пароль'}),
        min_length=8
    )
    new_password = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите новый пароль'}),
        min_length=8,
        help_text='Минимум 8 символов'
    )
    confirm_password = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите новый пароль'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Текущий пароль введен неверно')
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        
        if password1 and len(password1) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов')
        
        return cleaned_data


class ChangeEmailForm(forms.Form):
    """Форма смены email"""
    new_email = forms.EmailField(
        label='Новый email',
        widget=forms.EmailInput(attrs={'placeholder': 'Ваш новый email'})
    )
    password = forms.CharField(
        label='Пароль для подтверждения',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError('Этот email уже используется другим аккаунтом')
        return new_email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return password


class ChangePhoneForm(forms.Form):
    """Форма смены номера телефона"""
    new_phone = forms.CharField(
        label='Новый номер телефона',
        widget=forms.TextInput(attrs={'placeholder': '+7 (999) 000-00-00'}),
        min_length=10
    )
    password = forms.CharField(
        label='Пароль для подтверждения',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_phone(self):
        new_phone = self.cleaned_data.get('new_phone')
        # Очищаем номер от лишних символов
        phone_cleaned = ''.join(filter(str.isdigit, new_phone))
        
        # Проверка на российский номер (начинается с 7 или 8)
        if len(phone_cleaned) < 10:
            raise forms.ValidationError('Номер телефона слишком короткий')
        if len(phone_cleaned) > 11:
            raise forms.ValidationError('Номер телефона слишком длинный')
        if not phone_cleaned.startswith('7') and not phone_cleaned.startswith('8'):
            raise forms.ValidationError('Номер должен начинаться с 7 или 8')
        
        return new_phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return password
