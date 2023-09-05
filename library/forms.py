from .models import BookReview, User, Profilis, BookInstance
from django import forms



class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reviewer')
        widgets = { # paslepia laukus
            'book': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']


class DateInput(forms.DateInput):
    input_type = 'date'


class UserBookCreateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'reader', 'due_back']
        widgets = {'reader': forms.HiddenInput(),
                   'due_back': DateInput()
                   }
