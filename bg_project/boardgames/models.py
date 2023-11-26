from django.db import models
from django.contrib.auth.models import User


class Boardgame(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    year_published = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Borrowing(models.Model):
    boardgame = models.ForeignKey(Boardgame, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    date_borrowed = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.boardgame.name} - Borrowed by {self.borrower.username}"

    class Meta:
        unique_together = ['boardgame', 'date_returned']

    @property
    def is_returned(self):
        return self.date_returned is not None
