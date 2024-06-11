from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ShippingAddress, Product, Account
from django import forms

class RegistrationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['profile_picture', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class AccountForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Account
        fields = ['profile_picture']

class EditProfileForm(UserCreationForm):
    username = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['region', 'province', 'city', 'barangay', 'postal_code', 'home_address']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_picture', 'product_name', 'product_price', 'product_origin', 'product_description']

    def clean(self):
        cleaned_data = super().clean()
        product_picture = cleaned_data.get('product_picture')
        
        if not product_picture:
            self.add_error('product_picture', 'This field is required.')

        return cleaned_data

class CheckoutForm(forms.Form):
    payment_method = forms.ChoiceField(choices=(('card', 'Card Payment'), ('cod', 'Cash on Delivery')), widget=forms.RadioSelect)
    card_number = forms.CharField(max_length=16, required=False)
    expiry_date = forms.CharField(max_length=5, required=False)
    cvv = forms.CharField(max_length=3, required=False)
    