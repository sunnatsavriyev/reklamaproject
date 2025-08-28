from rest_framework import serializers
from .models import Advertisement, Station, MetroLine, Position, AdvertisementArchive
from rest_framework.fields import CurrentUserDefault
from datetime import date, timedelta


class MetroLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetroLine
        fields = ['id', 'name', ]



class StationSerializer(serializers.ModelSerializer):
    line_name = serializers.CharField(source='line.name', read_only=True)

    class Meta:
        model = Station
        fields = ['id', 'name','line', 'line_name', 'schema_image']



class AdvertisementSerializer(serializers.ModelSerializer):
    station = serializers.CharField(source='position.station.name', read_only=True)
    position_number = serializers.IntegerField(source='position.number', read_only=True)

    # Reklama ko'rishda barcha pozitsiyalar bo'lishi mumkin
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())

    class Meta:
        model = Advertisement
        fields = [
            'id', 'user', 'position', 'station', 'position_number',
            'Reklama_nomi', 
            'Qurilma_turi',
            'Ijarachi', 
            'Shartnoma_raqami',
            'Shartnoma_muddati_boshlanishi', 'Shartnoma_tugashi',
            'O_lchov_birligi', 
            'Qurilma_narxi', 'Egallagan_maydon', 'Shartnoma_summasi',
            'Shartnoma_fayl', 'photo', 'contact_number', 'created_at'
        ]
        read_only_fields = ['user']

    def get_station(self, obj):
        if obj.position and obj.position.station:
            return obj.position.station.name
        return None
    
    def get_status(self, obj):
        today = date.today()
        if obj.Shartnoma_tugashi and obj.Shartnoma_tugashi < today:
            return "tugagan"
        elif obj.Shartnoma_tugashi and obj.Shartnoma_tugashi <= today + timedelta(days=7):
            return "7_kunda_tugaydigan"
        return ""




# Reklama YARATISH uchun — faqat advertisement bo'sh joylar
class CreateAdvertisementSerializer(AdvertisementSerializer):
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.none(), required=True,allow_null=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            current_position = self.instance.position
            bosh_joylar = Position.objects.filter(advertisement__isnull=True)

            if current_position:
                bosh_joylar = bosh_joylar | Position.objects.filter(pk=current_position.pk)

            self.fields['position'].queryset = bosh_joylar.distinct()
        else:
            self.fields['position'].queryset = Position.objects.filter(advertisement__isnull=True)

    def validate(self, attrs):
        if 'position' not in attrs or attrs['position'] is None:
            raise serializers.ValidationError({
                'position': "Joy tanlanishi shart."
            })

        if not self.instance:
            shartnoma_raqami = attrs.get('Shartnoma_raqami')
            if shartnoma_raqami and Advertisement.objects.filter(Shartnoma_raqami=shartnoma_raqami).exists():
                raise serializers.ValidationError({
                    'Shartnoma_raqami': 'Bu shartnoma raqami allaqachon mavjud.'
                })
        return attrs

    def update(self, instance, validated_data):
        if 'position' not in validated_data:
            validated_data['position'] = instance.position
        return super().update(instance, validated_data)
    


class PositionSerializer(serializers.ModelSerializer):
    station = serializers.CharField(source="station.name", read_only=True)
    station_id = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(),
        source="station",
        write_only=True
    )
    advertisement = AdvertisementSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = ['id', 'station', 'station_id', 'number', 'advertisement', 'status']

    def get_status(self, obj):
        return getattr(obj, "advertisement", None) is not None

    def update(self, instance, validated_data):
        validated_data.pop("station", None)
        return super().update(instance, validated_data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agar update bo'lsa -> station_id ni olib tashlaymiz
        request = self.context.get("request")
        if request and request.method in ("PUT", "PATCH"):
            self.fields.pop("station_id", None)




class AdvertisementArchiveSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    line_name = serializers.CharField(source='line.name', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    class Meta:
        model = AdvertisementArchive
        fields = '__all__'

    def get_station_name(self, obj):
        try:
            return obj.position.station.name
        except AttributeError:
            return None


class ExportAdvertisementSerializer(serializers.Serializer):
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())

    def validate_position(self, value):
        if not value:
            raise serializers.ValidationError("Joy tanlanishi shart.")
        return value


