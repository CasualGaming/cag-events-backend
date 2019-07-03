from django.forms.models import BaseInlineFormSet


class NoDeleteBaseInlineFormSet(BaseInlineFormSet):
    """
    Custom formset to prevent deletion.
    Used by the inline for userprofiles to prevent the possibility
    of deleting the profile object.
    """
    def __init__(self, *args, **kwargs):
        super(NoDeleteBaseInlineFormSet, self).__init__(*args, **kwargs)
        self.can_delete = False
