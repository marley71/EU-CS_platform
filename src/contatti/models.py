from django.db import models

# Create your models here.

class Contatto(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20,null=True, blank=True)
    messaggio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
