from django import forms

class PaymentForm(forms.Form):
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
