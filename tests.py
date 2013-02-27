#-*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.template.base import TemplateDoesNotExist
from views import AjaxTemplateView

class DjangoAjaxTest(TestCase):
    urls = 'djax.test_urls'
    def setUp(self):
        self.c = Client()
    def testGuessTemplate(self):
        """Ajax query recieved"""
        try:
            response = self.c.get('/', HTTP_X_PJAX=True)
        except TemplateDoesNotExist, e:
            self.assertEqual(str(e), "filename-ajax.ext, filename.ext",
                             msg="Template list does not look like it should be!")

    def testUsualRequest(self):
        """Browser request"""
        try:
            response = self.c.get('/')
        except TemplateDoesNotExist, e:
            self.assertEqual(str(e), "filename.ext",
                             msg="Template list does not look like it should be!")
