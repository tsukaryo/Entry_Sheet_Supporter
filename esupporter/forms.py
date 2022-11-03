from esupporter.models import User, Company, ES, Question
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label #全てのフォームの部品にplaceholderを定義して、入力フォームにフォーム名が表示されるように指定する


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')

class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('company_name',)

class ESCreateForm(forms.ModelForm):
    class Meta:
        model = ES
        fields = ('question','answer')

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question','answer')