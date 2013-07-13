import json

from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.core.serializers.json import DjangoJSONEncoder


class AjaxFormMixin(object):
    """
    Mixin which adds support of AJAX requests to the form.
    Can be used with any view which has FormMixin.
    """

    json_dumps_kwargs = None
    success_message = ''

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_json_dumps_kwargs(self):
        if self.json_dumps_kwargs is None:
            self.json_dumps_kwargs = {}
        self.json_dumps_kwargs.setdefault('ensure_ascii', False)
        return self.json_dumps_kwargs

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context, cls=DjangoJSONEncoder, **self.get_json_dumps_kwargs())
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_valid(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.info(self.request, success_message)

        if self.request.is_ajax():
            context = self.get_json_context(form)
            return self.render_to_json_response(context)
        else:
            return super(AjaxFormMixin, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            context = {
                'status': 'error',
                'error': 'Bad Request'
            }
            errors = self.get_json_errors(form)
            if errors:
                context["errors"] = errors
            return self.render_to_json_response(context, status=400)
        else:
            return super(AjaxFormMixin, self).form_invalid(form)

    def is_result_requested(self):
        return self.request.POST.get("_return", "redirect") == "result"

    def get_json_context(self, form):
        if self.request.POST.get("_return", "redirect") == "result":
            context = {
                "status": "success"
            }
            msgs = self.get_json_messages()
            if msgs:
                context["messages"] = msgs
            obj = self.get_json_object(form)
            if obj:
                context["object"] = obj
        else:
            context = {
                "status": "redirect",
                "location": self.get_success_url()
            }
        return context

    def get_json_messages(self):
        msgs = []
        for message in messages.get_messages(self.request):
            msgs.append({
                "level": message.tags,
                "message": message.message,
            })
        return msgs

    def get_json_errors(self, form):
        errors = {}
        for error in form.errors.iteritems():
            errors.update({
                form.prefix + "-" + error[0] if form.prefix else error[0]: [unicode(msg) for msg in error[1]]
            })
        return errors

    def get_json_object(self, form):
        """
        Method returns dict representation of result (self.object of form.instance, etc)
        """
        return None


class AjaxModelFormMixin(AjaxFormMixin):
    """
    This mixin adds AJAX handling of model form.
    Can be used with any view which has ModelFormMixin.
    """
    def form_valid(self, form):
        if self.request.is_ajax():
            self.object = form.save()
        return super(AjaxModelFormMixin, self).form_valid(form)


class AjaxFormView(AjaxFormMixin, FormView):
    pass


class AjaxUpdateView(AjaxModelFormMixin, UpdateView):
    pass


class AjaxCreateView(AjaxModelFormMixin, CreateView):
    pass
