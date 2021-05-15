from django import forms
from django.contrib.auth.models import User
from . import models


class consumer_user_form(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class ConsumerForm(forms.ModelForm):
    class Meta:
        model=models.Consumer
        fields=['address','mobile','profile_pic']

class ItemForm(forms.ModelForm):
    class Meta:
        model=models.Item
        fields=['name','price','description','product_image']

#address of shipment
class form_of_address(forms.Form):
    Email = forms.EmailField()
    Mobile= forms.IntegerField()
    Address = forms.CharField(max_length=500)

class Form_of_Feedback(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['name','feedback']

#for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model=models.ConsumerOrder
        fields=['status']

#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class Subscribe(forms.Form):
    Email = forms.EmailField()
    def __str__(self):
        return self.Email