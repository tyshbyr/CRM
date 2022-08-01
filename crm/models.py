from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class Client(models.Model):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=15, blank=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        
class Status(models.Model):
    title = models.CharField(verbose_name='Название', max_length=150)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

class Source(models.Model):
    title = models.CharField(verbose_name='Название', max_length=150)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

