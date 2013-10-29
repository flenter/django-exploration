from django.contrib.gis.db import models


class Location(models.Model):
    name = models.CharField(max_length=150)
    geom = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return unicode(self.name)

    def get_lat_long(self):
        return (self.geom.coords[1], self.geom.coords[0])
