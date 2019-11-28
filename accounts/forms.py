# imports from django
from django.db.models import Q
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import RegexValidator
 
# instance of User model
User=get_user_model()

# creating login form for user
class UserLoginForm(forms.Form):
    phone_number=forms.CharField(label='Phone Number/Email',widget=forms.TextInput(attrs=
                                {
                                    'class':'form-control',
                                    'placeholder' : 'User Name',
                                }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=
                                {
                                    'class':'form-control',
                                    'placeholder' : 'Password',
                                }))
    # overriding default clean method for validating whether user and password are appropriate
    def clean(self, *args,**kwargs):
        query =self.cleaned_data.get('query')
        password =self.cleaned_data.get('password')
        user_qs_final=User.objects.filter(
            Q(phone_number__iexact=query)|
            Q(email__iexact=query)
        ).distinct()
        if not user_qs_final.exists() and user_qs_final.count() !=1:
            raise forms.ValidationError("Invalid Phone Number or Email")
        else:
            user_obj =user_qs_final.first()
            if not user_obj.check_password(password):
                raise forms.ValidationError("Invalid Password for {}".format(query))
        self.cleaned_data['user_obj']=user_obj
        return super(UserLoginForm, self).clean(*args,**kwargs)

#user creation form or in specific registeration form
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    name = forms.CharField(label='Full Name')
    phone_number = forms.CharField()                                
    email = forms.EmailField(required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=
                                {
                                    'class':'form-control',
                                    'placeholder' : 'Password',
                                }))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs=
                                {
                                    'class':'form-control',
                                    'placeholder' : 'Confirm Password',
                                }))

    class Meta:
        model = User
        fields = ('name','phone_number','email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if len(password1)<7:
            raise forms.ValidationError("Password must be of at least 8 digits")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# changing the user from admin panel itself
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('name', 'phone_number', 'email', 'spam_count','is_staff', 'is_admin','password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]