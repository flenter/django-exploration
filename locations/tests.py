from django.test import TestCase

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

        result = distance.calc_distance(a, b)
        self.assertEqual(result, 8794.624631776502)

        self.assertRaises(TypeError, distance.calc_distance, a, 1)
        self.assertRaises(TypeError, distance.calc_distance, 1, b)

        result = distance.calc_distance(b, a)
        self.assertEqual(result, 8794.624631776502)

import re

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class MySeleniumTests(LiveServerTestCase):
    fixtures = ["data/locations.json"]

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_locations(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/locations/'))
        print(dir(self.selenium))
        src = self.selenium.page_source
        text_found = re.search(r'text_to_search', src)
        self.assertFalse(text_found)
        text_found = re.search(r'Amsterdam', src)
        self.assertTrue(text_found)
    # self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
