Django Formalizr
================

Django AJAX Class Based Views

Quick start
-----------

1. Add "formalizr" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'formalizr',
      )

2. Inherit your form views from formalizr.views.AjaxFormView::

      from formalizr.views import AjaxFormView

      class SampleFormView(AjaxFormView):
           form_class = SampleForm

