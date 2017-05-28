from django import forms
from .models import CourseOrder

from ecommerce.models import AvailableTime

class CoursePreOrderForm(forms.Form):
    available_time = forms.ModelChoiceField(queryset=AvailableTime.objects.all())
    participants_number = forms.ChoiceField(choices=[('','選擇參加人數'), (1,'1人'), (2,'2人'), (3,'3人'), (4,'4人')])

    def __init__(self, *args, **kwargs):
        super(CoursePreOrderForm, self).__init__(*args, **kwargs)
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

class CheckOutForm(forms.Form):
    name = forms.CharField(max_length=15)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(max_length=500)
    voucher = forms.CharField(max_length=500, required=False, widget = forms.HiddenInput())
    available_time = forms.IntegerField(widget = forms.HiddenInput())
    participants_number = forms.IntegerField(widget = forms.HiddenInput())



class CourseOrderPaymentForm(forms.Form):
    MerchantID = forms.CharField(max_length=15, widget = forms.HiddenInput())
    RespondType = forms.CharField(max_length=6, required = False, widget = forms.HiddenInput())
    CheckValue = forms.CharField(max_length=255, required = False, widget = forms.HiddenInput())
    TimeStamp = forms.CharField(max_length=50, required = False, widget = forms.HiddenInput())
    Version = forms.CharField(max_length=5, widget = forms.HiddenInput())
    LangType = forms.CharField(max_length=5, required = False, widget = forms.HiddenInput())
    MerchantOrderNo = forms.CharField(max_length=20, widget = forms.HiddenInput())
    Amt = forms.IntegerField(widget = forms.HiddenInput())
    ItemDesc = forms.CharField(max_length=50, widget = forms.HiddenInput())
    TradeLimit = forms.IntegerField(required = False, widget = forms.HiddenInput())
    ExpireDate = forms.CharField(max_length=10, required = False, widget = forms.HiddenInput())
    ReturnURL = forms.CharField(max_length=50, required = False, widget = forms.HiddenInput())
    NotifyURL = forms.CharField(max_length=50, required = False, widget = forms.HiddenInput())
    CustomerURL = forms.URLField(max_length=50, required = False, widget = forms.HiddenInput())
    ClientBackURL = forms.URLField(max_length=50, required = False, widget = forms.HiddenInput())
    Email = forms.CharField(max_length=50, widget = forms.HiddenInput())
    EmailModify = forms.IntegerField(required = False, widget = forms.HiddenInput())
    LoginType = forms.IntegerField(required = False, widget = forms.HiddenInput())
    OrderComment = forms.CharField(max_length=300, required = False, widget = forms.HiddenInput())
    CREDIT = forms.IntegerField(required = False, widget = forms.HiddenInput())
    InstFlag = forms.CharField(max_length=18, required = False, widget = forms.HiddenInput())
    UNIONPAY = forms.IntegerField(required = False, widget = forms.HiddenInput())
    WEBATM = forms.IntegerField(required = False, widget = forms.HiddenInput())
    VACC = forms.IntegerField(required = False, widget = forms.HiddenInput())
    CVS = forms.IntegerField(required = False, widget = forms.HiddenInput())
    BARCODE = forms.IntegerField(required = False, widget = forms.HiddenInput())
    CUSTOM = forms.IntegerField(required = False, widget = forms.HiddenInput())
