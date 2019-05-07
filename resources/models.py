from django.db import models
from resources.models_utils import GalleryFactory


class ExcelFile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='ExcelFile_file')

    def __str__(self):
        return "{}".format(self.name)


class Image(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="ImageFile_file")
    image_url = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        if self.image:
            return "{} (image)".format(self.name)
        else:
            return "{} (url)".format(self.name)

    @staticmethod
    def create_gallery_from_list(images):
        urls = {value: value for value in images}
        for value in Image.objects.filter(name__in=images):
            urls[value.name] = value.url
        return GalleryFactory.create(urls.values())

    @property
    def url(self):
        if self.image:
            return self.image.url
        return self.image_url


class Text(models.Model):
    name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    text = models.TextField(default="")

    def __str__(self):
        return "{} ({})".format(self.title, self.name)

