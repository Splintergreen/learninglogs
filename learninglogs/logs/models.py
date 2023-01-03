from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Log(models.Model):
    """A log for a user to record their learning."""
    text = models.TextField()
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

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
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    logs = models.ManyToManyField(
        Log,
        blank=True,
        related_name='groups'
    )

    def __str__(self):
        """Return a string representation of the model."""
        return self.title

    class Meta:
        ordering = ['date_added']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
