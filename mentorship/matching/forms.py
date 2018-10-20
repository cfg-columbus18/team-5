from django.forms import ModelForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

form = ProfileForm()
