from django.db import models

# Create your models here.
class TrafficAccident(models.Model):
    year = models.IntegerField()
    result_of_the_accident = models.CharField(max_length=100)
    number_of_people = models.IntegerField()
    result_of_the_accident_ar = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('year', 'result_of_the_accident')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.year} - {self.result_of_the_accident}"


class RainfallRecord(models.Model):
    station = models.CharField(max_length=100)
    year = models.IntegerField()
    rainfall_mm = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('station', 'year')  # prevent duplicates
        ordering = ['-year', 'station']

    def __str__(self):
        return f"{self.station} - {self.year}: {self.rainfall_mm} mm"