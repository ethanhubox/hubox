from django import forms
from .models import CartItem

class CartItemForm(forms.ModelForm):
    participants_number = forms.ChoiceField(choices=[('','選擇參加人數'), (1,'1人'), (2,'2人'), (3,'3人'), (4,'4人')])

    def __init__(self, *args, **kwargs):
        super(CartItemForm, self).__init__(*args, **kwargs)
        self.fields['available_time'].empty_label = "請先於上方選擇日期"
        self.fields['available_time'].widget.attrs = {
        'class': 'selectpicker show-tick select-availabel-time',
        # 'multiple title': '選擇時間',
        'data-width': '85%',
        }


        self.fields['participants_number'].widget.attrs = {
        'class': 'selectpicker show-tick select-parnum',
        # 'multiple title': '選擇參加人數',
        'data-width': '85%',
        }

    class Meta:
        model = CartItem

        fields = [
        'available_time',
        'participants_number'
        ]
