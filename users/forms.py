from django import forms



class RegisterForm(forms.Form):
    avatar = forms.ImageField()
    age = forms.IntegerField()
    username = forms.CharField(max_length=100)
    password = forms.CharField()
    password_confirm = forms.CharField()


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data    
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)