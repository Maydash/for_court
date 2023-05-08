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


class MustPay(models.Model):
    JOB_CHOICES = [
        (1, 'Hokumet edara'),
        (2, 'Firma'),
        (3, 'Islanok')
    ]
    """Должник"""
    first_name = models.CharField(verbose_name='Bergidaryn ady', max_length=200)
    last_name = models.CharField(verbose_name='Bergidaryn Familiyasy', max_length=200)
    birthday = models.DateField(verbose_name='Doglan senesi')
    phone_number = models.CharField(max_length=12, verbose_name='Telefon belgisi 1')
    phone_number = models.CharField(max_length=12, verbose_name='Telefon belgisi 2')
    address = models.CharField(max_length=200, verbose_name='Oy salgysy')
    document_scan = models.FileField(verbose_name='Passport nusgasy', upload_to="file/", blank=True, null=True)
    job_status = models.CharField(max_length=100, verbose_name='Isin gornusi', choices=JOB_CHOICES)

    # TODO: для slug генерить путь (first_name, last_name)
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

    @property
    def receipt_total(self):
        total = Decimal(0)
        for i in self.mustpayreceipt_set.all():
            total += i.payment
        return total

    class Meta:
        verbose_name = "Bergidar"
        verbose_name_plural = "Bergidarlar"


class MustPayReceipt(models.Model):
    CURRENCY_CHOICES = [
        (1, 'TMT'),
        (2, 'USD')
    ]
    """Оплата должника"""
    must_pay = models.ForeignKey(MustPay, on_delete=models.CASCADE)
    payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tolenen mocberi')
    payment_date = models.DateField(verbose_name='Tolenen senesi')
    currency = models.CharField(max_length=20, verbose_name='Walyuta', choices=CURRENCY_CHOICES)
    # TODO: для document_scan генерить путь (user, date)
    document_scan = models.FileField(verbose_name='Tolegi tassyklayan resminama', upload_to="file/", blank=True, null=True)
    alimony_percent = models.IntegerField()

    # @property
    # def last_payment_date1(self):
    #     return self.last_payment_date_set.all().last()
    
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
    phone_number = models.CharField(max_length=12, verbose_name='Telefon belgisi')
    # TODO: для slug генерить путь (user, must_pay)
    document_scan = models.FileField(verbose_name='Passport nusgasy', upload_to="file/", blank=True, null=True)
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
    # TODO: для slug генерить путь (user, must_pay)
    document_scan = models.FileField(verbose_name='Passport nusgasy', upload_to="file/", blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

    class Meta:
        verbose_name = "Algydaryn cagasy"
        verbose_name_plural = "Algydarlaryn cagalary"


class Alimony(models.Model):
    """Алименты"""
    user = models.ForeignKey(User, verbose_name='Ulanyjy', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, verbose_name="Bolum", on_delete=models.SET_NULL, null=True)
    ruling = models.CharField(verbose_name='Karary cykaran', max_length=100)
    ruling_date = models.DateField(verbose_name='Kararyn senesi')
    # TODO: для slug генерить путь (user, must_pay)
    ruling_scan = models.FileField(verbose_name='Kararyn nusgasy', upload_to="file/", blank=True, null=True)
    executor = models.CharField(verbose_name='Yerine yetiryan', max_length=100)
    executor_register = models.CharField(verbose_name='Onumciligin belgisi', max_length=100)
    executor_date = models.DateTimeField(verbose_name='Onumciligin senesi')
    must_pay = models.OneToOneField(MustPay, verbose_name='Bergidaryn ady, familiyasy', on_delete=models.CASCADE)
    recipient = models.OneToOneField(Recipient, verbose_name='Algydaryn ady, familiyasy', on_delete=models.CASCADE)
    note = models.TextField(verbose_name='Bellik', blank=True)
    status = models.BooleanField(verbose_name='Ishin statusy', default=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    # TODO: для slug генерить путь (user, must_pay)
    slug = models.SlugField("url", max_length=200, unique=True)

    def __str__(self):
        return f'{self.must_pay} - {self.recipient}'

    class Meta:
        verbose_name = "Aliment"
        verbose_name_plural = "Alimentlar"

    def get_absolute_url(self):
        return reverse('alimony-detail', kwargs={'category': self.category.slug, 'slug': self.slug})


