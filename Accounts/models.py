from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'accounts/{0}/{1}'.format(instance.slug, 'avatar')

class User(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="Имя")
    sur_name = models.CharField(max_length=20, verbose_name="Фамилия")
    sur_sur_name = models.CharField(max_length=20, verbose_name="Отчество")
    slug = models.SlugField(verbose_name='Слаг')
    descriptions = models.TextField(max_length=300, verbose_name='Описание')
    email = models.EmailField(verbose_name='Почта')
    spec = models.ForeignKey('Specs', db_index=True, on_delete=models.PROTECT, verbose_name="Спецализация")
    photo = models.ImageField(upload_to=user_directory_path, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    vk_url = models.URLField(max_length=128, blank=True, verbose_name='VK')
    hh_url = models.URLField(max_length=128,blank=True, verbose_name='HH')
    behance_url = models.URLField(max_length=128,blank=True,verbose_name='BH')
    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(validators=[phone_number_regex], max_length=16, unique=True)

    def __str__(self):
        return self.name+self.sur_name



    def get_projects(self):
        return Project.objects.all().filter(user_id=self.id)

    def get_followers(self):
        return Follow.objects.all().filter(follow_to_id=self.id)

    def slug_create(self):
        self.slug = slugify(self.name+self.sur_name)

    def get_absolute_url(self):
        return reverse('user', kwargs={'user': self.name+self.sur_name})

    class Meta:
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'
        ordering = ['id']


class Project(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Название")
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Автор проекта")
    sum_registred = models.IntegerField(default=0, verbose_name='Сумма оценок зареганных')
    count_registred = models.IntegerField(default=0, verbose_name='Колисчество оценок зареганных')
    sum_unregistred = models.IntegerField(default=0, verbose_name='Сумма оценок незареганных')
    count_unregistred = models.IntegerField(default=0, verbose_name='Количество оценок незареганных')
    descriptions = models.TextField(max_length=300, verbose_name='Описание')
    github_url = models.URLField(max_length=128, blank=True, verbose_name='github')
    behance_url = models.URLField(max_length=128,  blank=True, verbose_name='BH')

    def get_photos(self):
        return Image.objects.all().filter(proj_id=self.id)

    def __str__(self):
        return self.name+self.name

    def get_absolute_url(self):
        return reverse('project', kwargs={'user': self.user.slug,'post_slug': self.name})

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['id']


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'accounts/projects/{0}/{1}'.format(instance.proj.user.slug, filename)
class Image(models.Model):
    proj = models.ForeignKey('Project', verbose_name='Фото проекта', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=image_directory_path)
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['id']


class Specs(models.Model):
    name = models.CharField(max_length=40, verbose_name="Специализация")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
        ordering = ['id']


class Follow(models.Model):
    follow_from = models.ForeignKey('User', related_name='follower', on_delete=models.CASCADE, verbose_name='Кто подписался')
    follow_to = models.ForeignKey('User', related_name='following',on_delete=models.CASCADE, verbose_name='На кого подписался')
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['id']


