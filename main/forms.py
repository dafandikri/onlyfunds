from django.forms import ModelForm
from main.models import ItemEntry
from django.utils.html import strip_tags

class ItemEntryForm(ModelForm):
    class Meta:
        model = ItemEntry
        fields = ["name", "description", "price", "bank"]
    
    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
    
    def clean_bank(self):
        bank = self.cleaned_data["bank"]
        return strip_tags(bank)