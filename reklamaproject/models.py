from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_file_extension
import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class MetroLine(models.Model):
    name = models.CharField(max_length=100, unique=True,null=True)

    def __str__(self):
        return str(self.name or "No name")

 

class Station(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    line = models.ForeignKey(MetroLine, on_delete=models.SET_NULL, related_name='stations', null=True, blank=True)
    schema_image = models.ImageField(upload_to='station_schemas/', null=True, blank=True, help_text="Bekat sxemasi rasmi")
    def __str__(self):
        return f"{self.name} ({self.line.name})" if self.line and self.line.name else self.name or "No name"



class Position(models.Model):
    station = models.ForeignKey(Station, on_delete=models.SET_NULL,null=True, related_name='positions')
    number = models.PositiveIntegerField(help_text="Joy raqami, masalan: 1, 2, 3")
    x = models.FloatField(help_text='Horizontal position (0-100%)', null=True, blank=True)
    y = models.FloatField(help_text='Vertical position (0-100%)', null=True, blank=True)
    def __str__(self):
        return f"{self.station.name} - Joy #{self.number}" if self.station else f"Joy #{self.number}"

    class Meta:
        unique_together = ('station', 'number')
        verbose_name = "Pozitsiya"
        verbose_name_plural = "Pozitsiyalar"


        
class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ads')
    position = models.OneToOneField(Position, on_delete=models.SET_NULL, related_name='advertisement', null=True, blank=True)
    Reklama_nomi = models.CharField(max_length=255, default='Reklama nomi',)
    Qurilma_turi = models.CharField(max_length=100, default='led',)
    Ijarachi = models.CharField(max_length=255, null=True, blank=True)
    Shartnoma_raqami = models.CharField(max_length=100, help_text="Shartnoma raqami o'zbekcha", null=True, blank=True)
    Shartnoma_muddati_boshlanishi = models.DateField()
    Shartnoma_tugashi = models.DateField()
    O_lchov_birligi = models.CharField(max_length=50, choices=[
        ('dona', 'Dona'),
        ('kv_metr', 'Kv metr'),
        ('komplekt', 'Komplekt')
    ],
    default='dona',
    )
    
    Qurilma_narxi = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    Egallagan_maydon = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    Shartnoma_summasi = models.DecimalField(max_digits=20, decimal_places=2 , default=0)
    Shartnoma_fayl = models.FileField(upload_to='contracts/', default=None, validators=[validate_file_extension], null=True, blank=True)
    photo = models.ImageField(upload_to='ad_photos/', null=True, blank=True)
    contact_number = models.CharField(max_length=20, default='+998')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.Reklama_nomi and self.position:
            return f"{self.Reklama_nomi} ({self.position})"
        return self.Reklama_nomi or "Advertisement"
    

class AdvertisementArchive(models.Model):
    original_ad = models.ForeignKey('Advertisement', on_delete=models.SET_NULL, null=True, related_name='archives')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    line = models.ForeignKey('MetroLine', on_delete=models.SET_NULL, null=True, blank=True)
    station = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    Reklama_nomi = models.CharField(max_length=255)
    Qurilma_turi = models.CharField(max_length=100)
    Ijarachi = models.CharField(max_length=255, null=True, blank=True)
    Shartnoma_raqami= models.CharField(max_length=100, null=True, blank=True)
    Shartnoma_muddati_boshlanishi = models.DateField()
    Shartnoma_tugashi = models.DateField()
    O_lchov_birligi = models.CharField(max_length=50)
    Qurilma_narxi = models.DecimalField(max_digits=15, decimal_places=2)
    Egallagan_maydon = models.DecimalField(max_digits=10, decimal_places=2)
    Shartnoma_summasi = models.DecimalField(max_digits=20, decimal_places=2)
    Shartnoma_fayl = models.FileField(upload_to='contracts_archive/', null=True, blank=True)
    photo = models.ImageField(upload_to='ad_photos_archive/', null=True, blank=True)
    contact_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Reklama_nomi} ({self.position})"
    
