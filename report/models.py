from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal

class Category(MPTTModel):
    """Категории"""
    name = models.CharField("Имя", max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField('url', max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('alimony-list', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = "Bolum"
        verbose_name_plural = "Bolumler"        


class Currency(models.Model):
    """Валюта"""
    name = models.CharField("Walyuta", max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Walyuta"
        verbose_name_plural = "Walyutalar"


class MustPay(models.Model):
    """Должник"""
    first_name = models.CharField(verbose_name='Bergidaryn ady', max_length=200)
    last_name = models.CharField(verbose_name='Bergidaryn Familiyasy', max_length=200)
    birthday = models.DateField(verbose_name='Doglan senesi')
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    # TODO: для slug генерить путь (first_name, last_name)
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

    @property
    def receipt_total(self):
        total = Decimal(0)
        for i in self.mustpayreceipt_set.all():
            total += i.last_payment
        return total

    class Meta:
        verbose_name = "Bergidar"
        verbose_name_plural = "Bergidarlar"


class MustPayReceipt(models.Model):
    """Оплата должника"""
    must_pay = models.ForeignKey(MustPay, on_delete=models.CASCADE)
    last_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sonky tolenen mocberi')
    last_payment_date = models.DateField(verbose_name='Tolenen resminamanyn senesi')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    # TODO: для image генерить путь (user, date)
    # TODO: создовать миниатюры ограничить вес фото и размер
    photo = models.ImageField(verbose_name='Tolegi tassyklayan resminama', upload_to="gallery/", blank=True, null=True)
    
    @property
    def last_payment_date1(self):
        return self.last_payment_date_set.all().last()
    
    def __str__(self):
        return f'{self.last_payment} - {self.currency}'

    class Meta:
        verbose_name = "Toleg"
        verbose_name_plural = "Tolegler"


class Recipient(models.Model):
    """Получатель денег"""
    first_name = models.CharField(verbose_name='Algydaryn ady', max_length=200)
    last_name = models.CharField(verbose_name='Algydaryn Familiyasy', max_length=200)
    birthday = models.DateField(verbose_name='Doglan senesi')
    # TODO: для slug генерить путь (first_name, last_name)
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

    class Meta:
        verbose_name = "Algydar"
        verbose_name_plural = "Algydarlar"


class RecipientChild(models.Model):
    """Дети получателя денег"""
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='Algydaryn ady', max_length=200)
    last_name = models.CharField(verbose_name='Algydaryn Familiyasy', max_length=200)
    birthday = models.DateField(verbose_name='Doglan senesi')

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

    class Meta:
        verbose_name = "Algydaryn cagasy"
        verbose_name_plural = "Algydarlaryn cagalary"


class Alimony(models.Model):
    """Алименты"""
    user = models.ForeignKey(User, verbose_name='Ulanyjy', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="Bolum", on_delete=models.CASCADE)
    executor = models.CharField(verbose_name='Yerine yetiryan', max_length=100)
    ruling = models.CharField(verbose_name='Karary cykaran', max_length=100)
    ruling_date = models.DateField(verbose_name='Kararyn senesi')
    must_pay = models.OneToOneField(MustPay, verbose_name='Bergidaryn ady, familiyasy', on_delete=models.CASCADE)
    recipient = models.OneToOneField(Recipient, verbose_name='Algydaryn ady, familiyasy', on_delete=models.CASCADE)
    note = models.TextField(verbose_name='Bellik', blank=True)
    status = models.BooleanField(verbose_name='Ishin statusy', default=False)
    # TODO: для slug генерить путь (user, must_pay)
    slug = models.SlugField("url", max_length=200, unique=True)

    def __str__(self):
        return f'{self.must_pay} - {self.recipient}'

    class Meta:
        verbose_name = "Aliment"
        verbose_name_plural = "Alimentlar"

    def get_absolute_url(self):
        return reverse('alimony-detail', kwargs={'category': self.category.slug, 'slug': self.slug})


