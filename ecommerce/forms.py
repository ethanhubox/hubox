from django import forms
from .models import Ordering, Material, UserProfile

class OrderingForm(forms.ModelForm):
    participants_number = forms.ChoiceField(choices=[('','選擇參加人數'), (1,'1人'), (2,'2人'), (3,'3人'), (4,'4人')])

    def __init__(self, *args, **kwargs):
        super(OrderingForm, self).__init__(*args, **kwargs)
        self.fields['available_time'].empty_label = "選擇時間"
        self.fields['available_time'].widget.attrs = {
        'class': 'selectpicker show-tick',
        # 'multiple title': '選擇時間',
        'data-width': '85%',
        }

        self.fields['material'].empty_label = "選擇製作素材(總價依素材變動)"
        self.fields['material'].widget.attrs = {
        'class': 'selectpicker show-tick',
        # 'multiple title': '選擇製作素材(總價依素材變動)',
        'data-width': '85%',
        }



        self.fields['participants_number'].widget.attrs = {
        'class': 'selectpicker show-tick',
        # 'multiple title': '選擇參加人數',
        'data-width': '85%',
        }

    class Meta:
        model = Ordering

        fields = [
        'available_time',
        'material',
        'participants_number'
        ]


class SignupForm(forms.Form):
    gender = forms.CharField(max_length=20)
    phone = forms.IntegerField()
    address = forms.CharField(max_length=200)

    def signup(self, request, user):
        user_profile = UserProfile.objects.create(user=user, gender=self.cleaned_data['gender'], phone=self.cleaned_data['phone'], address=self.cleaned_data['address'])
