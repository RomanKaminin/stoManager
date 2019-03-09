from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView

from .forms import StatementForm
from .models import Statement


class StatementCreate(CreateView):
    model = Statement
    form_class = StatementForm
    template_name = "sent_statement.html"
    success_url = "/accepted"

    def form_invalid(self, form):
        if self.request.is_ajax():
            response_data = {"form": form.errors}
            return JsonResponse(response_data, status=400)
        else:
            return super(StatementCreate, self).form_invalid(form)


class AcceptedView(TemplateView):
    template_name = "accepted.html"
