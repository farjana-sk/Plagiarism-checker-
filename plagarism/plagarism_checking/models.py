from django.db import models
from django.contrib.auth.models import User

class PlagiarismCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc1_text = models.TextField()
    doc2_text = models.TextField()
    tfidf_score = models.FloatField()
    sbert_score = models.FloatField()
    hybrid_score = models.FloatField()
    verdict = models.CharField(max_length=20)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Check by {self.user.username} on {self.checked_at.strftime('%Y-%m-%d %H:%M')}"
