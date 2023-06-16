from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from services.utils import unique_slugify


class Department(models.Model):
    """Модель участков/групп МЛТЦ"""
    name = models.CharField(max_length=20, verbose_name='Подразделение')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('area', kwargs={'dep_slug': self.slug})

    class Meta:
        verbose_name = 'Подразделения'
        verbose_name_plural = 'Подразделения'
        ordering = ['name']


class Area(models.Model):
    """Модель списка обслуживаемых районов"""
    name = models.CharField(max_length=20, verbose_name='Наименование района')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    department = models.ManyToManyField('Department', related_name="areas", verbose_name='Подразделение')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ats', kwargs={'area_slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Районы'
        verbose_name_plural = 'Районы'
        ordering = ['name']


class Ats(models.Model):
    """Модель списка АТС"""
    name = models.CharField(max_length=20, verbose_name='Наименование АТС')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    area = models.ForeignKey('Area', on_delete=models.CASCADE, verbose_name='Район')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ats_room', kwargs={'ats_slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'АТС'
        verbose_name_plural = 'АТС'
        ordering = ['name']


class Cable(models.Model):
    """Устройство КЛС на АТС"""
    sl = models.CharField(max_length=7, verbose_name='Соединительная линия')
    direction = models.CharField(max_length=40, verbose_name='Направление КЛС')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    tag = models.CharField(max_length=40, verbose_name='Бирка на кабеле')
    grounding = models.BooleanField(blank=True, verbose_name='Наличие заземления')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    cross = models.ForeignKey('Cross', on_delete=models.CASCADE, verbose_name='Кросс')
    ats = models.ForeignKey('Ats', on_delete=models.CASCADE, verbose_name='АТС')

    def __str__(self):
        return self.direction

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.direction)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ats_room', kwargs={'ats_slug': Cable.objects.get(slug=self.slug).ats.slug})

    class Meta:
        verbose_name = 'КЛС'
        verbose_name_plural = 'КЛС'
        ordering = ['direction']


class Cross(models.Model):
    """Устройство кросса"""
    number = models.CharField(max_length=3, verbose_name='№ кросса')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    tag = models.BooleanField(blank=True, verbose_name='Наличие бирки на кроссе')
    photo_cross = models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/", verbose_name='Фото кросса')
    photo_insert = models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/", verbose_name='Фото вкладыша')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    ats = models.ForeignKey('Ats',  on_delete=models.CASCADE, verbose_name='АТС')

    def __str__(self):
        return f"{self.ats.name}-{self.number}"

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.number)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ats_room', kwargs={'ats_slug': Cross.objects.get(slug=self.slug).ats.slug})

    class Meta:
        verbose_name = 'Кроссы'
        verbose_name_plural = 'Кроссы'
        ordering = ['number']


class Note(models.Model):
    """Примечания, что нужно выполнить"""
    description = models.TextField(blank=True, verbose_name='Примечания')
    cable = models.ForeignKey('Cable', on_delete=models.CASCADE, verbose_name='Направление КЛС')
    cross = models.ForeignKey('Cross', on_delete=models.CASCADE, verbose_name='Кросс')


    class Meta:
        verbose_name = 'Примечания'
        verbose_name_plural = 'Примечания'
