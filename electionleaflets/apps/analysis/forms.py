from django import forms

from .models import LeafletProperties

QUESTIONS = {
    'leaflet_style': {
        'label': "Leaflet Style",
        'choices': ('Leaflet', 'Letter', 'Magazine', 'Newsletter', 'Newspaper', 'CV', 'Survey')
    },
    'has_leader_photo': {
        'label': "Leader photo",
        'help_text': "Is there a photo of the sending party's leader?",
        'choices': ('Yes', 'No', 'n/a')
    },
    'has_opposition_leader': {
        'label': "Opposition leader pictured",
        'help_text': "Is there a photo of the another party leader?",
        'choices': ('Yes', 'No', 'n/a')
    },
    'has_opposition_leader_photo': {
        'label': "Opposition leader mentioned",
        'help_text': "Is another party leader mentioned?",
        'choices': ('Yes', 'No', 'n/a')
    },
    'has_logo': {
        'label': "Party logo",
        'help_text': "Is the sending party's logo on this leaflet?",
        'choices': ('Yes', 'No', 'n/a')
    },
    'squeeze_message': {
        'label': "Is there a 'squeeze message'?",
        'help_text': "i.e. does it say 'only X party can win here', 'X party can't win here', 'its a two-horse race', or a variation on that",
        'choices': ('Yes', 'No', 'n/a')
    },
    'include_graph': {
        'label': "Does it include a graph?",
        'choices': ('Yes', 'No', 'n/a')
    },
}



class QuestionSetForm(forms.ModelForm):
    class Meta:
        model = LeafletProperties

    def __init__(self, leaflet, *args, **kwargs):
      super(QuestionSetForm, self).__init__(*args, **kwargs)
      self.leaflet = leaflet
      self.fields = {
          'form_name': forms.CharField(widget=forms.HiddenInput),
          'leaflet_pk': forms.CharField(
              widget=forms.HiddenInput,
              required=False,
              ),
      }

      self.initial['form_name'] = 'analysis_questions_1'
      self.get_initial_from_models()

      for key, value in QUESTIONS.items():
        self.fields[key] = forms.ChoiceField(
            label=value['label'],
            choices=[(v,v) for v in value['choices']],
            widget=forms.RadioSelect,
            help_text=value.get('help_text', None),
            required=False,
        )

    def get_initial_from_models(self):
        for question in LeafletProperties.objects.filter(leaflet=self.leaflet):
            self.initial[question.key] = question.value


    def save(self, *args, **kwargs):
        for question, answer in self.cleaned_data.items():
            if not answer:
                continue
            if question in QUESTIONS.keys():
                question, created = LeafletProperties.objects.update_or_create(
                    leaflet=self.leaflet,
                    key=question,
                    defaults={
                        'value': answer
                    }
                )

