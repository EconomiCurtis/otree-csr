from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings

class holdon(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return{
            'debug': settings.DEBUG,
        }

class Instructions(Page):
    # timeout_seconds = 60

    def is_displayed(self):
        return self.round_number == 1

    def var_for_template(self):

        return{
            'debug': settings.DEBUG,
        }



page_sequence = [
    holdon,
    Instructions,
    ]
