from django import forms


class SubmitForm(forms.Form):
    file = forms.FileField(label='Файл обследования')


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', max_length=100, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', max_length=100, widget=forms.PasswordInput)

    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)

    SEX_CHOICES = (
        (0, 'Мужчина'),
        (1, 'Женщина'),
    )
    sex = forms.ChoiceField(label='Пол', choices=SEX_CHOICES)

    email = forms.EmailField()
