class CommonMixin:
    title = None
    flag = None

    def get_context_data(self, **kwargs):
        context = super(CommonMixin, self).get_context_data(**kwargs)
        context["title"] = self.title
        context["flag"] = self.flag

        return context
