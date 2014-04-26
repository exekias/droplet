from django.views.generic import View, TemplateView


class BaseView(View):
    pass


class Home(BaseView, TemplateView):
    template_name = 'web/home.html'
    block = 'core:home'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['content_block'] = self.block
        return context
