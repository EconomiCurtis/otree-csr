from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings
import time
import utils_csr


class Instructions(Page):

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

####################### Quiz Q #########################################
class quiz(Page):
    form_model = models.Player
    form_fields = ['quiz_user_answer']

    def quiz_user_answer_error_message(self, value):
        if (value != self.player.quiz_sol):
            return 'Incorrect. Feel free to raise your hand to ask for help. '

    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
            'page_title':"Quiz " + str(self.round_number),
            'quiz_sol':self.player.quiz_sol
        }


####################### Quiz Solution #########################################
class quiz_sol(Page):
    form_model = models.Player

    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
            'page_title':"Quiz " +  str(self.round_number) + " Solution",
        }

class WaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def after_all_players_arrive(self):
        pass
        # for p in self.group.get_players():
        #     p.set_payoff()





page_sequence = [
    Instructions,
    quiz,
    quiz_sol,
    WaitPage,
    ]
