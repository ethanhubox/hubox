from django import forms
from .models import Ordering, Material, UserProfile

class OrderingForm(forms.ModelForm):
    participants_number = forms.ChoiceField(choices=[('','選擇參加人數'), (1,'1人'), (2,'2人'), (3,'3人'), (4,'4人')])

    def __init__(self, *args, **kwargs):
        super(OrderingForm, self).__init__(*args, **kwargs)
        self.fields['available_time'].empty_label = "請先於上方選擇日期"
        self.fields['available_time'].widget.attrs = {
        'class': 'selectpicker show-tick select-availabel-time',
        # 'multiple title': '選擇時間',
        'data-width': '85%',
        }

        # self.fields['material'].empty_label = "選擇製作素材(總價依素材變動)"
        # self.fields['material'].widget.attrs = {
        # 'class': 'selectpicker show-tick select-material',
        # # 'multiple title': '選擇製作素材(總價依素材變動)',
        # 'data-width': '85%',
        # }



        self.fields['participants_number'].widget.attrs = {
        'class': 'selectpicker show-tick select-parnum',
        # 'multiple title': '選擇參加人數',
        'data-width': '85%',
        }

    class Meta:
        model = Ordering

        fields = [
        'available_time',
        # 'material',
        'participants_number'
        ]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

        fields = [
        'name',
        'phone',
        'address',
        ]
