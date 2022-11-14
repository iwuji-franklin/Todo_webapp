from cProfile import label
from django import forms


    
class AddNewForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class':'description', 'cols': '20', 'rows': '6'}))
    due_date = forms.DateField(label="Due Date", widget=forms.DateTimeInput(attrs={'type':'date'}))
    #override the default __init__ so we can set the request

    def __init__(self,request=None,*args, **kwargs):
        self.request = request
        super(AddNewForm, self).__init__(*args,**kwargs)

    #custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
            return self.cleaned_data