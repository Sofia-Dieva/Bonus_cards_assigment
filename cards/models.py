from django import forms
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class BonusCard(models.Model):
    number = models.CharField(max_length=16, verbose_name='Серия карты')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата выпуска карты')
    expiry = models.DateTimeField(verbose_name='Дата окончания активности', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата использования')
    sum_of_bonus = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = (
        ('Activated', 'Activated'),
        ('Disabled', 'Disabled'),
        ('Not activated', 'Not activated'),
    )
    status = models.CharField(max_length=13, choices=STATUS_CHOICES, default='Not activated')

    def get_absolute_url(self):
        return reverse('card', kwargs={"pk": self.pk})

    def __str__(self):
        return self.number

    def clean(self):
        if len(self.number) < 16 or self.number.isdigit() is False:
            raise forms.ValidationError('Серия карты должна состоять из 16 цифр')


class Purchase(models.Model):
    card = models.ForeignKey(BonusCard, on_delete=models.CASCADE, related_name='used_card', verbose_name='Карта')
    bill = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField('Name', max_length=35)
    shopping_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')

    def __str__(self):
        return self.name


@receiver(post_save, sender=Purchase)
def update_tasks(sender, instance, created, **kwargs):
    if created:
        instance.card.updated_at = instance.shopping_date
        instance.card.sum_of_bonus += instance.bill
        instance.card.save()
