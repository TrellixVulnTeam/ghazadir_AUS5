from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main.models import User,Transaction
from django.core.validators import RegexValidator
from main.enums import *

class UserSignUpForm(UserCreationForm):
    phone_regex = RegexValidator(regex=r'^\d{8}$', message="يجب أن تحتوي أرقام الهاتف على 8 أرقام.")
    username = forms.CharField(validators=[phone_regex], max_length=8,help_text=False,label="رقم الهاتف")
    phone_number = forms.CharField(widget=forms.HiddenInput,validators=[phone_regex],required=False, max_length=8,label='رقم الهاتف')
    location = forms.CharField(max_length=255,required=True,label='عنوان العمل')
    first_name = forms.CharField(max_length=255,required=True,label='الاسم الاول')
    last_name = forms.CharField(max_length=255,required=True,label='اسم العائلة')
    city = forms.ChoiceField(choices = CITY_CHOICES,widget=forms.Select(), required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','first_name', 'last_name','city',
                    'location']


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','city',
                    'location')




class TransactionForm(forms.Form):
    phone_regex = RegexValidator(regex=r'^\d{8}$', message="يجب أن تحتوي أرقام الهاتف على 8 أرقام.")
    beneficiary_number = forms.CharField(validators=[phone_regex],max_length=8,required=True,label='رقم الزبون المستلم')
    money = forms.CharField(max_length=255,required=True,label='المبلغ')
    fee = forms.CharField(max_length=255,required=True,label='الرسوم')
    to_agent_number = forms.CharField(validators=[phone_regex], max_length=8,required=True,label='رقم الوكيل المستلم')
    from_agent_number = forms.CharField(widget=forms.HiddenInput,validators=[phone_regex], max_length=8,label='رقم الوكيل الموسل')


    def clean(self):
        # form level cleaning
        cleaned_data = super(TransactionForm, self).clean()

        from_agent_phone = cleaned_data.get("from_agent_number")
        to_agent_phone = cleaned_data.get("to_agent_number")
        print("TODO: _ag : ",to_agent_phone)
        from_agent =  User.objects.filter(username=from_agent_phone).first()
        to_agent =  User.objects.filter(username=to_agent_phone).first()

        # if not from_agent and not to_agent:
        #     raise forms.ValidationError("عذرًا ، يجب أن يكون كل من الوكيل المرسل والوكيل المتلقي موجودًا ضمن الوكلاء المسجلين.")
        # if not from_agent:
        #     raise forms.ValidationError("عذرًا ، يجب أن يكون رقم الوكيل المرسل موجودًا ضمن الوكلاء المسجلين.",)
        if not to_agent:
            raise forms.ValidationError("عذرًا ، يجب أن يكون رقم الوكيل المستلم ضمن الوكلاء المسجلين.",)
