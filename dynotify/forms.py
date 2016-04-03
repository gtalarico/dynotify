from django.forms import ModelForm
from django.core.exceptions import FieldError

from models import Subscriber

class SubscriberForm(ModelForm):
    # error_css_class = 'danger'
    # required_css_class = 'required'

    class Meta:
        model = Subscriber
        fields = ['email', ]

    def __init__(self, *args, **kwargs):
        super(SubscriberForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs\
                    .update({
                        'placeholder': 'Email',
                        'class': 'form-control'
                    })

        # self.fields['email'].empty_label = 'Select Venue'
        # self.fields['venue'].error_messages = {
                    # 'required': 'Please select a valid venue.' }
