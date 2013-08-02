Django Formalizr
================

Class Based Views which takes forms throught AJAX and returns JSON response.
Response includes:
 * status of request
 * validation errors, if any
 * messages from django messages framework, if any
 * url for redirection or result object, in case of success

Quick start
-----------

0. Installation::

      pip install -U django-formalizr


1. Add "formalizr" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'formalizr',
      )

2. Inherit your form views from formalizr.views.AjaxFormView::

      from formalizr.views import AjaxFormView

      class SampleFormView(AjaxFormView):
           form_class = SampleForm

3. Make AJAX requests to your views and process JSON responses


Views Classes
-------------
Available view classes are: AjaxFormView, AjaxCreateView and AjaxUpdateView. Their purpose must be obvious.

JSON Responses
--------------

#### Redirect location after successful form submission.

In simplest case, when form processed without errors and messages, `HTTP 200 OK` is returned with `application/json`::

    {
       "status": "redirect",
       "location": "/path/to/some/view/"
    }

View's method `get_success_url()` is used to get the redirect location.


#### Object and messages after successful form submission

If `_return=result` parameter is included into request, then JSON representation of result is returned::

    {
       "status": "success",
       "object": {"pk":1},
       "messages": [{"level": "info", "message": "Object created!"}]
    }

View's method `get_json_object()` is used to dump result into dict, later this dict is dumped into JSON.
Messages are included into response.


#### Error messages after failed form submission

In case of errors, `HTTP 400 Bad Request` is returned with `application/json` content::

    {
        "status": "error",
        "error": "Bad Request"
        "errors": {
                      "__all__":["Common form errors"],
                      "first-field": ["First field error"],
                      "second-field": ["Second fields error"]
                  }
    }

If form comes with prefix, then names of all fields will have same prefix.