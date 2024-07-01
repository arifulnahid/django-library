from django.forms import ModelForm
from .models import Rating


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['comment'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
