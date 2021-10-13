from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

# Create your models here.


class Material(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
# уникальный двух полей: пара слаг и дата д.б. уникальны

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_materials')

    MATERIAL_TYPE = [
        ('theory', 'Theoretical Materials'),
        ('practice', 'Practical Materials'),
    ]

    material_tape = models.CharField(max_length=255,
                                     choices=MATERIAL_TYPE,
                                     default='theory')

    def get_absolute_url(self):
        return reverse('lesson:detailed_material',
                        args=[self.publish.year,
                              self.publish.month,
                              self.publish.day,
                              self.slug])
# get_absolute_url - это не метод а отдельная функция, он должен быть в модели

    def __str__(self):
        return self.title  # для отображения названий материалов в админке
# отключили, т.к. настроили в админке
# подключили снова для отображения в других моделях


class Comment(models.Model):

    name = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    material = models.ForeignKey(Material,
                                 on_delete=models.CASCADE,
                                 related_name='comments')  # для того чтобы получить все комментарии из материала, мы могли получить их по атрибуту
# для отображения подписи в комментариях

    def __str__(self):
        return '@{name} {body} for {material}'. format(name=self.name,
                                                       body=self.body,
                                                       material=self.material
                                                       )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="user/%Y/%m/%d", blank=True)

    def __str__(self):
        return str(self.user)
