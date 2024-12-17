from django import forms
from .models import CustomUser, Category


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется. Выберите другой.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_client = True  # Автоматически назначаем роль клиента
        if commit:
            user.save()
        return user

from .models import Ad

class AdForm(forms.ModelForm):
    REGION_CHOICES = [
        ('', 'Выберите область'),  # Пустое значение с текстом по умолчанию
        ('Минская', 'Минская'),
        ('Гомельская', 'Гомельская'),
        ('Брестская', 'Брестская'),
        ('Витебская', 'Витебская'),
        ('Могилёвская', 'Могилёвская'),
        ('Гродненская', 'Гродненская'),
    ]
    region = forms.ChoiceField(choices=REGION_CHOICES, required=True)
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'phone_number', 'region', 'category', 'city', 'image']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Выберите категорию")