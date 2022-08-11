from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
