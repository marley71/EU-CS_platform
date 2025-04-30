from django.contrib.gis.db import models

class Provincia(models.Model):
    name = models.CharField(max_length=100, editable=False)
    sigla = models.CharField(max_length=3, editable=False)
    regione = models.CharField(max_length=100, editable=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # class Meta:
    #     db_table = 'localita'  # Specifica il nome della tabella nel database

    def __str__(self):
        return f'{self.name}'

    def humanized(self):
        return self.name
