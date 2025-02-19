from django.db import models


class SentMessage(models.Model):
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    response = models.JSONField()  # To store the response from the SMS API

    def __str__(self):
        return f"Message sent at {self.sent_at}"
