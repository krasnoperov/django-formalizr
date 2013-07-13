from formalizr.tests.forms import SimpleForm, SimpleModelForm
from formalizr.tests.models import SimpleModel
from formalizr.views import AjaxFormView, AjaxCreateView, AjaxUpdateView


class SimpleFormView(AjaxFormView):
    form_class = SimpleForm
    template_name = 'base.html'
    success_url = "/"


class SimpleCreateView(AjaxCreateView):
    form_class = SimpleModelForm
    template_name = 'base.html'
    success_url = "/"

    def get_json_object(self, form):
        return {
            "pk": self.object.pk
        }


class SimpleUpdateView(AjaxUpdateView):
    form_class = SimpleModelForm
    template_name = 'base.html'
    success_url = "/"

    VALUE = 11

    def get_json_object(self, form):
        return {
            "pk": self.object.pk
        }

    def get_object(self, queryset=None):
        return SimpleModel.objects.get(value=SimpleUpdateView.VALUE)