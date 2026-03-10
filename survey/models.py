from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=255, verbose_name="Başlık")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    is_active = models.BooleanField(default=False, verbose_name="Yayında mı?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Anket"
        verbose_name_plural = "Anketler"

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500, verbose_name="Soru")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")

    class Meta:
        verbose_name = "Soru"
        verbose_name_plural = "Sorular"
        ordering = ["order"]

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=300, verbose_name="Seçenek")

    class Meta:
        verbose_name = "Seçenek"
        verbose_name_plural = "Seçenekler"

    def __str__(self):
        return self.text


class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Yanıt"
        verbose_name_plural = "Yanıtlar"

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.survey.title}"


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cevap"
        verbose_name_plural = "Cevaplar"

    def __str__(self):
        return f"{self.question.text}: {self.choice.text}"
