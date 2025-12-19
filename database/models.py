import os
import json

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from rest_framework import serializers


imgs_dir = settings.IMGS_URL
json_dir = settings.JSON_URL
main_dir = settings.BASE_DIR


latin_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_]+$',
    message='Only latin characters, numbers and  underscores are allowed.',
    code='invalid_latin'
)


# Creating a text file
def create_text_file(directory : str, file_name : str, text : dict):
    address = os.path.join(directory, file_name)
    with open(address, 'w', encoding='utf-8') as file:
        json.dump(text, file, ensure_ascii=False, indent=4)


class Place(models.Model):
    title = models.CharField(max_length=50)
    description_short = models.TextField(max_length=500)
    description_long = models.TextField(max_length=2500)
    place_id = models.CharField(max_length=20, validators=[latin_validator], blank=False, unique=True)

    def __str__(self):
        return self.title

    def save(self):
        super().save()

        if not hasattr(self, 'place'):
            obj = self
        else:
            obj = self.place

        ful_obj = PlaceSerializerJSON(obj).data
        create_text_file(str(main_dir) + json_dir, ful_obj['place_id'] + '.json', ful_obj)


class Images(models.Model):
    title = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='images/')
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='images')


class Coordinates(models.Model):
    latitude = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(90.0)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    place = models.OneToOneField('Place', on_delete=models.CASCADE, related_name='coordinates')


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ['latitude', 'longitude']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image']


class PlaceSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer(many=False)

    class Meta:
        model = Place
        fields = ['id', 'title', 'place_id', 'coordinates']


class PlaceSerializerJSON(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer(many=False)
    imgs = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ['title', 'description_short', 'description_long', 'place_id', 'coordinates', 'imgs']

    def get_imgs(self, obj):
        return [img.image.url for img in obj.images.all()]