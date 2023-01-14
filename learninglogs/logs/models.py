from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()


class Log(models.Model):
    """A log for a user to record their learning."""
    text = RichTextField()
    description = models.TextField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField('Картинка',
                              upload_to='posts/',
                              blank=True
                              )

    def __str__(self):
        """Return a string representation of the model."""
        return self.text[:50] + '...'

    class Meta:
        ordering = ['date_added']
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'


class Group(models.Model):
    """A group of users who can share logs."""
    title = models.CharField(max_length=200)
    description = RichTextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    logs = models.ManyToManyField(
        Log,
        related_name='groups'
    )

    def __str__(self):
        """Return a string representation of the model."""
        return self.title

    class Meta:
        ordering = ['date_added']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
