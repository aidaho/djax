from django.conf.urls import patterns, include, url
from djax.views import AjaxTemplateView

urlpatterns = patterns('', url(r'^$', AjaxTemplateView.as_view(template_name="filename.ext")))
