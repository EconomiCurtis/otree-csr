from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings
import time
from scipy.stats import rankdata
import numpy as np
import random

class WaitPage1(WaitPage):

    def is_displayed(self):
    
        #if no ret score, get own score from ret in part 1.
        if 'ret_score' not in self.participant.vars: 
            ret_score = random.choice([62,63,64,65])
            self.participant.vars["ret_score"] = ret_score
        else: 
            ret_score = self.participant.vars["ret_score"]

        return self.round_number == 1

    def after_all_players_arrive(self):
        pass

    def vars_for_template(self):      


        self.participant.vars['vcm_round_number'] = 1

        return {
        'ret_score':self.participant.vars["ret_score"],
        }

class Instructions(Page):


    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        self.participant.vars['vcm_round_number'] = 1

        ret_score = self.participant.vars["ret_score"]

        # get other player's scores in group
        op_scores = []
        for p in self.player.get_others_in_group():
            op_scores.append(p.participant.vars["ret_score"])

        op_scores_sum = sum(op_scores)


        return {
            'ret_score':ret_score,
            'op_scores':op_scores,
            'op_scores_sum':op_scores_sum,
        }

class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.participant.vars['vcm_round_number'] <= self.participant.vars['vcm_round_count']


    def after_all_players_arrive(self):
        if self.participant.vars['vcm_round_number'] <= self.participant.vars['vcm_round_count']:
            self.subsession.group_randomly()



# class WaitPage(WaitPage):

#     def is_displayed(self):
#         return self.round_number == 2 

#     def after_all_players_arrive(self):
#         pass
#         # for p in self.group.get_players():
#         #     p.set_payoff()


class SelectInvestment(Page):

    form_model = models.Player
    form_fields = [
        # 'individual_exchange',
        # 'group_exchange',
        'group_exchange_percent',
        ]

    def after_all_players_arrive(self):
        pass

    def is_displayed(self):
        return self.participant.vars['vcm_round_number'] <= self.participant.vars['vcm_round_count']

    def vars_for_template(self):

        ret_score = self.participant.vars["ret_score"]

        # get other player's scores in group
        op_scores = []
        for p in self.player.get_others_in_group():
            op_scores.append(p.participant.vars["ret_score"])

        op_scores_sum = sum(op_scores)

        return {
            'vcm_round_number':self.participant.vars['vcm_round_number'],
            'vcm_round_count_total':self.participant.vars['vcm_round_count'],
            'ret_score':ret_score,
            'op_scores':op_scores,
            'op_scores_sum':op_scores_sum,
        }

    def before_next_page(self):
        self.player.group_exchange_percent = self.player.group_exchange_percent * 0.01
        self.player.group_exchange = self.participant.vars["ret_score"] * (self.player.group_exchange_percent)
        self.player.individual_exchange = self.participant.vars["ret_score"] - self.player.group_exchange


class WaitPage2(WaitPage):

    def is_displayed(self):
        # if self.participant.vars['vcm_round_number'] <= self.participant.vars['vcm_round_count']:
        #     self.player.group_exchange_percent = float(self.player.group_exchange) / float(self.player.group_exchange + self.player.individual_exchange)
        return self.participant.vars['vcm_round_number'] <= self.participant.vars['vcm_round_count']


class SelectInvestment_Review(Page):


    def is_displayed(self):
        return self.participant.vars['vcm_round_number'] <= self.participant.vars['vcm_round_count']


    def vars_for_template(self):

        self.player.set_payoffs()

        ret_score = self.participant.vars["ret_score"]

        # get other player's scores in group
        op_scores = []
        for p in self.player.get_others_in_group():
            op_scores.append(p.participant.vars["ret_score"])

        op_scores_sum = sum(op_scores)
        

        # get other player's contributions
        op_individual_exchange_thisround = []
        op_group_exchange_thisround = []
        for op in self.player.get_others_in_group():
            op_individual_exchange_thisround.append(round(op.individual_exchange, 2))
            op_group_exchange_thisround.append(round(op.group_exchange, 2))

        score_op_individual_exchange_thisround = 1/2 * sum(op_individual_exchange_thisround)


        # get own ge_percent, avg ge contribution for all rounds.  
        own_ge_percent = []
        for prev_player in self.player.in_all_rounds():
            if prev_player.group_exchange_percent != None:
                own_ge_percent.append(prev_player.group_exchange_percent)
        own_ge_percent = sum(own_ge_percent) / len(own_ge_percent)

        # all players in group, ge_percent; avg ge contribution for all rounds.  
        ge_percent_list = []
        overall_ge_list = []
        for op in self.group.get_players():
            op_ge_percent = []
            op_ge = []
            for prev_op in op.in_all_rounds():
                if prev_op.group_exchange_percent != None:
                    op_ge_percent.append(prev_op.group_exchange_percent)
                    op_ge.append(prev_op.group_exchange)
            ge_percent_list.append(np.sum(op_ge_percent) / np.size(op_ge_percent))
            overall_ge_list.append(np.sum(op_ge) / np.size(op_ge))

        self.participant.vars['overall_ge_percent_list'] = ge_percent_list
        self.session.vars['overall_ge_percent_list'] = ge_percent_list #used in stage game
        self.participant.vars['overall_own_ge_percent'] = own_ge_percent
        self.participant.vars['overall_ge_list'] = overall_ge_list

        return {
            'vcm_round_number':self.participant.vars['vcm_round_number'],
            'ret_score':ret_score,
            'op_scores':op_scores,
            'op_scores_sum':op_scores_sum,
            'self_individual_exchange':self.player.individual_exchange,
            'self_group_exchange':self.player.group_exchange,
            'self_group_exchange_percent':self.player.group_exchange_percent,
            'group_exchange_score':(1/2)*self.player.group_exchange,
            'op_individual_exchange_thisround':op_individual_exchange_thisround,
            'op_group_exchange_thisround':op_group_exchange_thisround,
            'score_op_individual_exchange_thisround':score_op_individual_exchange_thisround,
            'round_points':self.player.round_points,
            'overall_own_ge_percent':own_ge_percent,
            'overall_ge_percent_list':ge_percent_list,
            'overall_ge_list':self.participant.vars['overall_ge_list'],
        } 



    def before_next_page(self):
        self.player.vcm_round = self.participant.vars['vcm_round_number']
        self.participant.vars['vcm_round_number'] += 1




class Part3_prep(Page):
    # timeout_seconds = 9000

    def is_displayed(self):
        return ((self.participant.vars['vcm_round_number'] == (self.participant.vars['vcm_round_count'] + 1) )
            & (self.round_number <= self.participant.vars['vcm_round_count']))
    

    def vars_for_template(self):
        # # assign this play to a type. 
        # # it really should be implemented in group class
        # # but this uses a consistent method so each player figures out their own type given the same informaiotn. 
        # own_ge_percent = self.participant.vars['overall_own_ge_percent']
        ge_percent_list = self.participant.vars['overall_ge_percent_list'] #all playe'rs ge%, sorted by player ID

        # own_id_index = self.player.id_in_group - 1

        # # rank 1 and 2 are smallest ge%
        # # rank 3 and 4 are biggest ge contributers (check out scipy.stats `rankdata` for details)
        # if (np.where(rankdata(np.array(ge_percent_list), method='ordinal') == 4)[0]==own_id_index):
        #     self.participant.vars['Role'] = "A"
        # elif (np.where(rankdata(np.array(ge_percent_list), method='ordinal') == 3)[0]==own_id_index):
        #     self.participant.vars['Role'] = "A"
        # else: 
        #     self.participant.vars['Role'] = "F"

        self.player.set_roles(ge_percent_list)

        # record player roles. 
        # used in template output
        for prev_player in self.player.in_all_rounds():
            if prev_player.player_role != None:
                role = prev_player.player_role
        for prev_player in self.player.in_all_rounds():
            if prev_player.player_role_list != None:
                roles = prev_player.player_role_list


        # get score for VCM round. 
        # randomly select a round, and save the final score and group exchange contrib
        final_scores = []
        final_ges = []
        ret_scores = []

        for p in self.group.get_players():

            p.final_score = p.in_round(p.participant.vars['paid_round']).round_points
            final_scores.append(p.in_round(p.participant.vars['paid_round']).round_points)
            
            p.final_ge = p.in_round(p.participant.vars['paid_round']).group_exchange
            final_ges.append(p.in_round(p.participant.vars['paid_round']).group_exchange)

            ret_scores.append(p.participant.vars['ret_score'])

        self.player.paid_round = self.participant.vars['paid_round']

        self.participant.vars['final_scores'] = final_scores
        self.participant.vars['final_ges'] = final_ges
        #session vars to be used in stage game
        self.session.vars['final_scores'] = final_scores
        self.session.vars['final_ges'] = final_ges
        # self.session.vars['player_role_list'] = player_role_list #handled in models.py now
        self.participant.vars["ret_scores"] = ret_scores

        #set up participant variables
        # self.participant.vars['Role'] defined in models.py set_roles
        self.participant.vars['final_score'] = self.player.final_score
        self.participant.vars['final_ge'] = self.player.final_ge
        # self.participant.vars["ret_score"] handled above
        # self.participant.vars["overall_ge_percent"] defined in models.py set_roles


        table_rows = []
        for prev_player in self.player.in_all_rounds():
            if prev_player.round_number != None:
                row = {
                    'round_number': prev_player.vcm_round,
                    'individual_exchange': prev_player.individual_exchange,
                    'group_exchange': prev_player.group_exchange,
                    'group_exchange_percent':round(100*prev_player.group_exchange/(prev_player.group_exchange + prev_player.individual_exchange) , 1),
                    'round_points':prev_player.round_points,
                }
                table_rows.append(row)

        return {
            'table_rows': table_rows,
            'own_ge_percent':self.participant.vars["overall_ge_percent"],
            'own_ge_overallavg':self.participant.vars['overall_own_ge'],
            'role':self.participant.vars['Role'],
            'roles':roles,
            'paid_round':self.participant.vars['paid_round'],
            'final_scores':self.participant.vars['final_scores'],
            'final_score':self.participant.vars['final_score'],
            'self_final_score':self.participant.vars['final_scores'][self.player.id_in_group - 1],
            'final_ges':self.participant.vars['final_ges'],
            'final_ge':self.participant.vars['final_ge'],
            'ret_scores':self.participant.vars["ret_scores"],
            'ret_score':self.participant.vars["ret_score"],
            'overall_ge_percent_list':self.participant.vars['overall_ge_percent_list'],
            'overall_ge_list':self.participant.vars['overall_ge_list'],
            'player_role_list':self.participant.vars['player_role_list'],
            
            'debug': settings.DEBUG,
        }




class WaitPage3(WaitPage):

    def is_displayed(self):
        return ((self.participant.vars['vcm_round_number'] == (self.participant.vars['vcm_round_count'] + 1) )
            & (self.round_number <= self.participant.vars['vcm_round_count']))

    def after_all_players_arrive(self):
        self.participant.vars['vcm_round_number'] += 1





page_sequence = [
    WaitPage1,
    Instructions,
    WaitPage, 
    SelectInvestment,
    WaitPage2,
    SelectInvestment_Review,
    ShuffleWaitPage,
    Part3_prep,
    WaitPage3
    ]