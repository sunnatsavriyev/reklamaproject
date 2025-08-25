from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import MetroLine, Station, Position, Advertisement, AdvertisementArchive

@admin.register(MetroLine)
class MetroLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
    search_fields = ['name', ]
    verbose_name = _("Metro liniyasi")
    verbose_name_plural = _("Metro liniyalari")

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'line','schema_image_display']
    list_filter = ['line']
    search_fields = ['name',]
    verbose_name = _("Bekat")
    verbose_name_plural = _("Bekatlar")
    def schema_image_display(self, obj):
        if obj.schema_image:
            return f"<img src='{obj.schema_image.url}' width='100' height='60' />"
        return "Yo'q"
    schema_image_display.allow_tags = True
    schema_image_display.short_description = "Sxema rasmi"

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'station', 'number',]
    list_filter = ['station']
    search_fields = ['station__name',]
    verbose_name = _("Joylashuv")
    verbose_name_plural = _("Joylashuvlar")

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        'Reklama_nomi', 'Ijarachi', 
        'get_station', 'Qurilma_turi', 
        'Shartnoma_raqami',
        'Shartnoma_muddati_boshlanishi', 'Shartnoma_tugashi','O_lchov_birligi',
        'Qurilma_narxi', 'Egallagan_maydon', 'Shartnoma_summasi','Shartnoma_fayl',
    ]
    list_filter = [
        'Ijarachi', 
        'Qurilma_turi',
    ]
    search_fields = [
        'Ijarachi', 
        'Qurilma_turi',
    ]
    verbose_name = _("Reklama")
    verbose_name_plural = _("Reklamalar")

    @admin.display(description=_("Bekat"))
    def get_station(self, obj):
        if obj.position and obj.position.station:
            return f"{obj.position.station.name} "
        return "-"
@admin.register(AdvertisementArchive)
class AdvertisementArchiveAdmin(admin.ModelAdmin):
    list_display = ['Reklama_nomi', 
        'Qurilma_turi', 'Shartnoma_raqami',
        'Shartnoma_muddati_boshlanishi', 'Shartnoma_tugashi','O_lchov_birligi',
        'Qurilma_narxi',  'Shartnoma_summasi','Shartnoma_fayl', 'user', 'created_at']
    search_fields = ['Reklama_nomi', 'Shartnoma_raqami']
    list_filter = ['created_at', 'user']
    readonly_fields = [  
        'original_ad', 'user', 'position', 'Reklama_nomi', 
        'Qurilma_turi',  'Ijarachi',
        'Shartnoma_raqami', 
        'Shartnoma_muddati_boshlanishi', 'Shartnoma_tugashi',
        'O_lchov_birligi', 'Qurilma_narxi',
        'Egallagan_maydon', 'Shartnoma_summasi', 'Shartnoma_fayl',
        'photo', 'contact_number', 'created_at'
    ]

    def has_add_permission(self, request):
        return False  

    def has_change_permission(self, request, obj=None):
        return False  

    def has_delete_permission(self, request, obj=None):
        return True 