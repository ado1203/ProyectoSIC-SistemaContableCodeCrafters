from django.forms import ModelForm
from .models import Move


class MoveForm(ModelForm):
    class Meta:
        model = Move
        fields = ['move_date', 'move_description', 'move_type',
                  'move_quantity', 'move_unitPrice', 'stock']
