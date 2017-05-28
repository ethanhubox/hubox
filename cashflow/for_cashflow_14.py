form.fields['MerchantID'].initial = 'MS39344778'
form.fields['Version'].initial = '1.4'
form.fields['RespondType'].initial = 'JSON'
form.fields['TimeStamp'].initial = str(time.time())
form.fields['LangType'].initial = 'zh-tw'
form.fields['MerchantOrderNo'].initial = 'HBX{}_{}'.format(str(course_order.pk), request.user.pk)
form.fields['Amt'].initial = int(total_amount)
form.fields['ItemDesc'].initial = str(request.user)
form.fields['TradeLimit'].initial = ''
form.fields['ExpireDate'].initial = ''
form.fields['ReturnURL'].initial = request.build_absolute_uri(reverse('finish_order'))
form.fields['NotifyURL'].initial = ''
form.fields['CustomerURL'].initial = request.build_absolute_uri(reverse('finish_order'))
form.fields['ClientBackURL'].initial = ''
form.fields['Email'].initial = request.user.email
form.fields['EmailModify'].initial = 1
form.fields['LoginType'].initial = 0
form.fields['OrderComment'].initial = ''
form.fields['CREDIT'].initial = 1
form.fields['CVS'].initial = 1

trade_info = 'MerchantID=' + str(form.fields['MerchantID'].initial) + "&RespondType=" + form.fields['RespondType'].initial + '&TimeStamp=' + str(form.fields['TimeStamp'].initial) + '&Version=' + form.fields['Version'].initial + '&MerchantOrderNo=' + str(form.fields['MerchantOrderNo'].initial) + '&Amt=' + str(form.fields['Amt'].initial) + '&ItemDesc=' + form.fields['ItemDesc'].initial
print(trade_info)

BLOCK_SIZE = 32
PADDING = ' '
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
encryption_suite = AES.new(os.environ['PAYMENT_HASHKEY'], AES.MODE_CBC, os.environ['PAYMENT_HASHIV'])
cipher_text = encryption_suite.encrypt(pad(trade_info))
trade_info_hex = binascii.hexlify(cipher_text).decode("utf-8")

form.fields['TradeInfo'].initial = trade_info_hex

shavalue = hashlib.sha256()
trade_sha = "HashKey=" + os.environ['PAYMENT_HASHKEY'] + "&" + trade_info_hex + '&HashIV=' + os.environ['PAYMENT_HASHIV']
shavalue.update(trade_sha.encode('utf-8'))
form.fields['TradeSha'].initial = shavalue.hexdigest().upper()
print(form.fields['TradeSha'].initial)



form
MerchantID = forms.CharField(max_length=15, widget = forms.HiddenInput())
TradeInfo = forms.CharField(max_length=255, required = False, widget = forms.HiddenInput())
TradeSha = forms.CharField(max_length=255, required = False, widget = forms.HiddenInput())
Version = forms.CharField(max_length=5, widget = forms.HiddenInput())
RespondType = forms.CharField(max_length=6, required = False, widget = forms.HiddenInput())
TimeStamp = forms.CharField(max_length=50, required = False, widget = forms.HiddenInput())
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
CVS = forms.IntegerField(required = False, widget = forms.HiddenInput())



"訂單資訊：\n訂單編號：{}\n會員：{}\n聯絡電話：{}\n聯絡地址：{}\n訂單內容：{} {} {}~{} 參加人數：{}人\n訂單金額：{}".format(
    course_order.order_number,
    str(course_order.user),
    course_order.user.userprofile.phone,
    course_order.user.userprofile.address,
    course_order.available_time.course.name,
    course_order.available_time.date.strftime("%Y-%m-%d %H:%M"),
    course_order.available_time.start_time.strftime("%H:%M"),
    course_order.available_time.end_time.strftime("%H:%M"),
    str(course_order.participants_number),
    str(course_order.total_amount)
)
+ course_order.order_number +
"\n會員：" + str(course_order.user) +
"\n聯絡電話：" + course_order.user.userprofile.phone +
"\n聯絡地址：" + course_order.user.userprofile.address +
"\n訂單內容：" + course_order.available_time. +
"\n訂單金額：" + str(course_order.total_amount)


course_order.available_time.course.name + " " + course_order.available_time.date.strftime("%Y-%m-%d %H:%M") + " " + course_order.available_time.start_time.strftime("%H:%M") + "～" + course_order.available_time.end_time.strftime("%H:%M") + " " + str(course_order.participants_number) + "人"
