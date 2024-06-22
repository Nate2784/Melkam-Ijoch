from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Donation, AddCharity, Project,Charity #,Message

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'avatar', )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        avatar = self.cleaned_data.get('avatar')

        if commit:
            user.save()
            Profile.objects.create(user=user, avatar=avatar if avatar else 'avatars/default.jpg')

        return user


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )

    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)
        if commit:
            user.save()
            profile = Profile.objects.get(user=user)
            avatar = self.cleaned_data.get('avatar')
            if avatar:
                profile.avatar = avatar
                profile.save()
        return user


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['user_ID', 'project_ID', 'charity_ID', 'amount', 'paymentMethod']
        widgets = {
            'user_ID': forms.HiddenInput(),
            'project_ID': forms.HiddenInput(),
            'charity_ID': forms.HiddenInput(),
        }

class AddCharityForm(forms.ModelForm):
    class Meta:
        model = AddCharity
        fields = ['name', 'image', 'description', 'website', 'location', 'establishedYear', 'authorisedDocuments', 'statement']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter charity name', 'required': True}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept': 'image/*', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Briefly describe the charity', 'required': True}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter charity website URL'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter charity location', 'required': True}),
            'establishedYear': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter establishment year', 'required': True}),
            'authorisedDocuments': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept': '.pdf', 'required': True}),
            'statement': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional statements or information'}),
        }


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        self.fields['charity_ID'].queryset = Charity.objects.filter(user_ID=user)

    class Meta:
        model = Project
        fields = ['name', 'description', 'image', 'charity_ID']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter project description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


# class ContactForm(forms.ModelForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

#     class Meta:
#         model = Message
#         fields = ['email', 'message']

