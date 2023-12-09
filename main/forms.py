from django.forms import ModelForm
from .models import Search

class SearchForm(ModelForm):
    class Meta:
        model=Search
        fields = ['owner','age','published_date','origin','dh_o','destination','dh_d','company','length','weight']