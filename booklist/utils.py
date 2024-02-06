from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect


from .models import *


class ObjectDetailMixin:
    model = None
    template = None
    detail_admin_panel = None
    comment_model = None
    form_comments = None

    def get(self, request, **kwargs):
        preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = 'ru' if preferred_language.startswith('ru') else 'en'
        obj = get_object_or_404(self.model, slug=kwargs['slug'])


        context = {
            self.model.__name__.lower(): obj,
            'categories': Category.objects.all(),
            'lang': lang,
        }

        return render(request, self.template, context=context)


class ObjCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form_model(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjEditMixin:
    model = None
    form_model = None
    template = None

    def get(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        bound_form = self.form_model(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        bound_form = self.form_model(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.delete()
        return redirect(reverse(self.redirect_url))
