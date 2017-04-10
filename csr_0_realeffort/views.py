from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings
import time


class Instructions1(Page):
    # timeout_seconds = 60

    def is_displayed(self):
        return self.round_number == 1

    def var_for_template(self):

        return{
            'debug': settings.DEBUG,
        }

    def before_next_page(self):
        if ('start_time' not in self.participant.vars):
            self.participant.vars['start_time'] = time.time()
            self.participant.vars['end_time'] = time.time() + self.player.ret_timer




class TranscribeTask(Page):

    form_model = models.Player
    form_fields = ['user_text']

    def is_displayed(self):
        if "end_time" not in self.participant.vars:
            self.participant.vars['end_time'] = time.time() + 995

        return ((self.round_number > 2) & (time.time() < self.participant.vars['end_time']))

    def vars_for_template(self):

        # For Page Timer
        #get current time
        current_time = (time.time())
        # calc how long we've been here
        time_expended =  current_time - self.participant.vars['start_time']

        # For Page "Number of Correct Words"
        total_correct = 0
        for p in self.player.in_all_rounds():
            if p.round_payoff != None:
                total_correct += p.round_payoff

        # set up messgaes in transcription task
        if self.player.in_previous_rounds()[-1].ret_final_score == None: #on very first task
            correct_last_round = "<br>"
            ret_final_score = 20
        else: #all subsequent tasks
            ret_final_score = int(self.player.in_previous_rounds()[-1].ret_final_score)
            if self.player.in_previous_rounds()[-1].is_correct:
                correct_last_round = "Your last guess was <font color='green'>correct</font>"
            else:
                correct_last_round = "Your last guess was <font color='red'>incorrect</font>"






        # Page variables
        return {
            'end_time': self.participant.vars['end_time'],
            'tiemdf': self.participant.vars['end_time'] - current_time,
            'current_time': current_time,
            'time_limit':self.player.ret_timer,
            'init_time': self.participant.vars['start_time'],
            'time_expended': time_expended,
            'correct_last_round': correct_last_round,
            'total_correct': int(total_correct),
            'final_score':ret_final_score,
            'round_count':(self.round_number - 1),
            'reference_text': Constants.reference_texts[self.round_number - 1],
            'debug': settings.DEBUG,
        }



    def before_next_page(self):

        # find time at button click
        final_time = time.time()
        end_of_timer =  self.participant.vars['start_time'] + self.player.ret_timer

        # update player payoffs
        if (end_of_timer > final_time):
            if (Constants.reference_texts[self.round_number - 1] == self.player.user_text):
            	self.player.is_correct = True
            	self.player.round_payoff = 1
            else:
                self.player.is_correct = False
                self.player.round_payoff = c(0)
        else:
            self.player.is_correct = False
            self.player.round_payoff = c(0)

        self.player.set_final_score()

class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == 100
    def after_all_players_arrive(self):
        pass
        # for p in self.group.get_players():
        #     p.set_payoff()

class TaskResults(Page):
    # timeout_seconds = 1000

    def is_displayed(self):
        return self.round_number == 101

    def vars_for_template(self):


        ##### Get Own Score #####################################################
        total_correct = 0
        for p in self.player.in_all_rounds():
            if p.round_payoff != None:
                total_correct += p.round_payoff
            else:
                total_correct += 0

        # get final score, by going through all rounds, and pulling out the max observed, ignoring all the Nones.
        total_payoff = max(x.ret_final_score for x in self.player.in_previous_rounds() if x.ret_final_score is not None)

        ######### Get other members of group's scores ##########################
        op_scores = []
        for op in self.player.get_others_in_group():
            op_ret_final_score = max(x.ret_final_score for x in op.in_previous_rounds() if x.ret_final_score is not None)
            op_scores.append(op_ret_final_score)

        ######### Get other members of group's scores ##########################
        all_ret_scores = []
        for p in self.player.get_others_in_group():
            p_final_score = max(x.ret_final_score for x in p.in_previous_rounds() if x.ret_final_score is not None)
            all_ret_scores.append(op_ret_final_score)

        ##### save all variables ###############################################

        self.participant.vars['ret_correct'] = int(total_correct)
        self.participant.vars['ret_score']   = total_payoff # own final score
        self.participant.vars['op_scores']   = op_scores #other group member scores
        self.participant.vars['all_ret_scores']   = all_ret_scores #all ret scores in group


        # only keep obs if YourEntry player_sum, is not None.
        table_rows = []
        task_num = 0
        for prev_player in self.player.in_all_rounds():
            if prev_player.user_text != None:
                task_num += 1
                row = {
                    'round_number': task_num,
                    'real_text': Constants.reference_texts[prev_player.round_number - 1],
                    'player_text': prev_player.user_text,
                   	'is_correct':prev_player.is_correct,
                    'total_score': prev_player.ret_final_score,
                }
                table_rows.append(row)

        return {
        'total_correct':int(total_correct),
        'table_rows': table_rows,
        'total_score':total_payoff,
        'op_scores':op_scores
        }


page_sequence = [
    Instructions1,
    TranscribeTask,
    ResultsWaitPage,
    TaskResults,
    ]
