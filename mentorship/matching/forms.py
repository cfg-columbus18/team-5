from django.forms import ModelForm

class ProfileForm(forms.ModelForm):
    form = ProfileForm()
    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
       self.current_user = kwargs.pop('current_user')
#       super(ProfileForm, self).__init__(*args, **kwargs)
