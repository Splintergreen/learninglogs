from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Log(models.Model):
    """A log for a user to record their learning."""
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text[:50] + '...'
