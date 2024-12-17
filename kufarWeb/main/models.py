from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email является обязательным")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)  # Имя
    last_name = models.CharField(max_length=30, blank=True)   # Фамилия

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Добавим обязательные поля

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Ad(models.Model):
    # Связь с моделью пользователя (CustomUser)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')

    # Связь с моделью категории
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads')

    # Поля объявления
    title = models.CharField(max_length=200)  # Название объявления
    description = models.TextField()  # Описание объявления
    phone_number = models.CharField(max_length=15)  # Номер телефона
    image = models.ImageField(upload_to='ads_images/', null=True, blank=True)  # Картинка объявления
    region = models.CharField(max_length=100)  # Область (например, "Минская область")
    city = models.CharField(max_length=100)  # Город (например, "Минск")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Цена в BYN
    # Дополнительные поля
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания объявления
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления объявления

    def __str__(self):
        return f"{self.title} - {self.user.email}"  # Название и email пользователя

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']  # Сортировка по дате создания
