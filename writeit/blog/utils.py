class DataMixin:
    paginate_by = 3
    cat_selected = None
    extra_context = {}

    def __init__(self):
        
        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    def get_mixin_context(self, context, **kwargs):
        context['cat_selected'] = None
        context.update(kwargs)
        return context
