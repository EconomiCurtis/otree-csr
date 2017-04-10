from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings
import time


class Instructions3(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        if 'ret_score' not in self.participant.vars:
            self.participant.vars["ret_score"] = 61
        if 'op_scores' not in self.participant.vars: 
            self.participant.vars["op_scores"] = [41,50,61]

        return {
            'ret_score':self.participant.vars["ret_score"],
            'op_scores':self.participant.vars["op_scores"]
        }

####################### Quiz 3 #########################################
class quiz1(Page):

    form_model = models.Player
    form_fields = ['quiz_01']

    def is_displayed(self):
        return self.round_number == 2

    def quiz_01_error_message(self, value):
        if (value != 135):
            return 'Incorrect'

    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
        }

class quiz1_sol(Page):

    def is_displayed(self):
        return ((self.round_number > 2) & (self.round_number < 4))


####################### Quiz 2 #########################################
class quiz2(Page):

    form_model = models.Player
    form_fields = ['quiz_02']

    def is_displayed(self):
        return self.round_number == 4

    def quiz_02_error_message(self, value):
        if (value != 145):
            return 'Incorrect'
            
    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
        }

class quiz2_sol(Page):

    def is_displayed(self):
        return self.round_number == 5

####################### Quiz 3 #########################################
class quiz3(Page):

    form_model = models.Player
    form_fields = ['quiz_03']

    def is_displayed(self):
        return self.round_number == 6

    def quiz_03_error_message(self, value):
        if (value != 105):
            return 'Incorrect'
            
    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
        }

class quiz3_sol(Page):

    def is_displayed(self):
        return self.round_number == 7

####################### Quiz 4 #########################################
class quiz4(Page):

    form_model = models.Player
    form_fields = ['quiz_04']

    def is_displayed(self):
        return self.round_number == 8

    def quiz_04_error_message(self, value):
        if (value != 112.5):
            return 'Incorrect'
            
    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
        }

class quiz4_sol(Page):

    def is_displayed(self):
        return self.round_number == 9


####################### Quiz 5 #########################################
class quiz5(Page):

    form_model = models.Player
    form_fields = ['quiz_05']

    def is_displayed(self):
        return self.round_number == 10

    def quiz_05_error_message(self, value):
        if (value != 60):
            return 'Incorrect'
            
    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
        }

class quiz5_sol(Page):

    def is_displayed(self):
        return self.round_number == 11



####################### Quiz 6 #########################################
class quiz6(Page):

    form_model = models.Player
    form_fields = ['quiz_06']

    def is_displayed(self):
        return self.round_number == 12

    def quiz_06_error_message(self, value):
        if (value != 90):
            return 'Incorrect'
            
    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
        }

class quiz6_sol(Page):

    def is_displayed(self):
        return self.round_number == 13



class WaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == 14
    def after_all_players_arrive(self):
        pass
        # for p in self.group.get_players():
        #     p.set_payoff()





page_sequence = [
    Instructions3,
    quiz1,
    quiz1_sol,
    # quiz2,
    # quiz2_sol,
    quiz3,
    quiz3_sol,
    # quiz4,
    # quiz4_sol,
    quiz5,
    quiz5_sol,
    # quiz6,
    # quiz6_sol,
    WaitPage,

    ]