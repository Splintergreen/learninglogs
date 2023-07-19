from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.image_resize import image_resize


class User(AbstractUser):
    email = models.EmailField(unique=True)
    about = models.TextField(max_length=200, blank=True, null=True)
    skills = models.TextField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(
        'Аватар',
        upload_to='users/',
        blank=True,
        default='users/no_image.jpg'
    )

    def __str__(self):
        return self.username
    """A user for the site."""
    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        image_resize(self.avatar, self.username, 200, 200)
        super().save(*args, **kwargs)


class Group(models.Model):
    """A group of users who can share logs."""
    title = models.CharField(max_length=200)
    description = RichTextField(max_length=400)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.title

    class Meta:
        ordering = ['date_added']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Log(models.Model):
    """A log for a user to record their learning."""
    text = RichTextUploadingField()
    description = models.TextField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        """Return a string representation of the model."""
        return self.text[:15]

    class Meta:
        ordering = ['date_added']
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'


class Comment(models.Model):
    log = models.ForeignKey(
        Log,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = RichTextUploadingField(config_name='comment')
    created = models.DateTimeField(auto_now_add=True)

    @property
    def total_comments(self):
        return self.count()

    class Meta:
        ordering = ['-created', 'author', 'log']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
