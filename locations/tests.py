from django.test import TestCase
# from django_nose import FastFixtureTestCase as TestCase
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry

from locations.templatetags import distance
from locations.models import Location


class LocationTestCase(TestCase):
    fixtures = ["data/locations.json"]

    def test_find_cities(self):
        # not really a test... just seeing if there are two items
        self.assertEqual(Location.objects.count(), 2)

    def test_on_earth(self):
        p = GEOSGeometry('POINT(0 0)')

        ls = Location.objects.filter(geom__distance_lte=(p, D(km=40000)))
        self.assertEqual(ls.count(), 2)

        ls = Location.objects.filter(geom__distance_lte=(p, D(km=6000)))
        self.assertEqual(ls.count(), 1)

        ls = Location.objects.filter(geom__distance_gte=(p, D(km=6000)))
        self.assertEqual(ls.count(), 1)


class DistanceFilterCase(TestCase):
    fixtures = ["data/locations.json"]

    def test_find_distance(self):
        a, b = Location.objects.all()
        # print a, b
        result = distance.calc_distance(a, b)
        self.assertEqual(result, 8794.624631776502)