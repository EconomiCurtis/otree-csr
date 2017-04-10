from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings
import time
import numpy
import decimal
import json
from math import ceil

def round_up(Num, RoundTo):
    ''' rounds up to nearest... RoundTo '''
    return int(ceil(Num / float(RoundTo))) * RoundTo


class InitWaitPage(WaitPage):
    #this page is regrouping based on Role
    
    wait_for_all_groups = True

    def is_displayed(self):
        return (self.round_number == 1)

    def after_all_players_arrive(self):
        # executed only once for the entire group.
 
        self.participant.vars['stage_round'] = 1 #just setup stage_round counter. I do this after too. 

        # player_role_list = self.session.vars["player_role_list"]
        # final_scores = self.session.vars["final_scores"] 
        # final_ges = self.session.vars["final_ges"]
        # ret_scores = self.session.vars["ret_scores"]
        # overall_ge_percent = self.session.vars['overall_ge_percent_list']

        #         # collect subject data from previous parts of experimetn. 
        # cnt = 0
        # for p in self.subsession.get_players():
        #     p.participant.vars['Role'] = player_role_list[cnt]
        #     p.role = player_role_list[cnt]
        #     p.participant.vars['final_score'] = final_scores[cnt] #final score from vcm round
        #     p.participant.vars['final_ge'] = final_ges[cnt] # the GE from the randomly selected round. 
        #     p.participant.vars["ret_score"] = ret_scores[cnt] # ret score
        #     p.participant.vars["overall_ge_percent"] = overall_ge_percent[cnt] # ret scoreoverall_ge_percent
        #     cnt += 1


        players = self.subsession.get_players()

        A_players = [p for p in players if p.participant.vars['Role'] == 'A']
        F_players = [p for p in players if p.participant.vars['Role'] == 'F']

        group_matrix = []

        # pop elements from A_players until it's empty
        while A_players:
            new_group = [
              A_players.pop(),
              F_players.pop(),
            ]
            group_matrix.append(new_group)

        self.subsession.set_group_matrix(group_matrix)

        for subsession in self.subsession.in_rounds(2, Constants.num_rounds):
            subsession.group_like_round(1)



class Instructions(Page):


    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        self.participant.vars['stage_round'] = 1
        self.participant.vars['end_this_stage_round'] = False

##############################################################

        # player_role_list = self.session.vars["player_role_list"]
        # final_scores = self.session.vars["final_scores"] 
        # final_ges = self.session.vars["final_ges"]
        # ret_scores = self.session.vars["ret_scores"]
        # overall_ge_percent = self.session.vars['overall_ge_percent_list']

        # # collect subject data from previous parts of experimetn. 
        # cnt = 0
        # for p in self.subsession.get_players():
        #     p.participant.vars['Role'] = player_role_list[cnt]
        #     p.role = p.participant.vars['Role']
        #     p.participant.vars['final_score'] = final_scores[cnt] #final score from vcm round
        #     p.participant.vars['final_ge'] = final_ges[cnt] # the GE from the randomly selected round. 
        #     p.participant.vars["ret_score"] = ret_scores[cnt] # ret score
        #     p.participant.vars["overall_ge_percent"] = overall_ge_percent[cnt] # ret scoreoverall_ge_percent
        #     cnt += 1

        for p in self.subsession.get_players():
            p.player_role = p.participant.vars['Role']

        ##############################################################

        # set previous rounds data into experiment output file
        self.player.role = self.participant.vars["Role"]
        self.player.ret_score = self.participant.vars["ret_score"]
        self.player.vcm_score = self.participant.vars["final_score"]
        self.player.vcm_ge_percent = self.participant.vars["overall_ge_percent"]


        players = self.subsession.get_players()

        A_players = [p for p in players if p.participant.vars['Role'] == 'A']
        F_players = [p for p in players if p.participant.vars['Role'] == 'F']

        group_matrix = []

        # pop elements from A_players until it's empty
        while A_players:
            new_group = [
              A_players.pop(),
              F_players.pop(),
            ]
            group_matrix.append(new_group)



        return {
            'player_role_list':self.participant.vars["player_role_list"],
            'stage_round':self.participant.vars['stage_round'],
            'Role_self':self.player.role,
            'Role_partic_var':self.participant.vars["Role"],
            'counter_party_id':self.player.get_others_in_group(),
            'counter_party_role':self.player.get_others_in_group()[0].participant.vars['Role'],    
            'counter_party_score':self.player.get_others_in_group()[0].participant.vars['final_score'], 
            'countery_party_ret_score':self.player.get_others_in_group()[0].participant.vars['ret_score'], 
            'counter_party_ge':self.player.get_others_in_group()[0].participant.vars['final_ge'],  
            'counter_party_overall_ge_percent':round(self.player.get_others_in_group()[0].participant.vars['overall_ge_percent'],2),   
            'self_ret_score':self.participant.vars["ret_score"], 
            'self_score':self.participant.vars['final_score'],
            'self_ge':self.participant.vars['final_ge'],
            'self_overall_ge_percent':self.participant.vars['overall_ge_percent'],
            'overall_ge_percent_list':self.participant.vars['overall_ge_percent_list'],
            'overall_ge_list':self.participant.vars['overall_ge_list'],
            'ret_scores':self.participant.vars["ret_scores"],
            'role':self.participant.vars['Role'],
            'final_scores':self.participant.vars['final_scores'],
            'final_ges':self.participant.vars['final_ges'],
            'ret_scores':self.participant.vars["ret_scores"],
            'overall_ge_percent_list':self.participant.vars['overall_ge_percent_list'],
            'group_matrix':group_matrix,
            'allplayers':group_matrix,
            'debug': settings.DEBUG,
        }

    def before_next_page(self):
        if self.participant.vars["Role"] == 'A':
            self.player.role = 'A'
        elif self.participant.vars["Role"] == 'F':
            self.player.role = 'F'
        else:  self.player.role = "sadf"




###############################################################################
## Quiz Time ##################################################################
###############################################################################

class quiz1(Page):

    form_model = models.Player
    form_fields = ['quiz_01']

    def is_displayed(self):
        return self.round_number == 1

    def quiz_01_error_message(self, value):
        if (value != 45):
            return 'Incorrect'


    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
        }
    
    

class quiz1_sol(Page):

    def is_displayed(self):
        return self.round_number == 1


####################### Quiz 3 #########################################
class quiz2(Page):

    form_model = models.Player
    form_fields = ['quiz_02']

    def is_displayed(self):
        return self.round_number == 1

    def quiz_02_error_message(self, value):
        if (value != 30):
            return 'Incorrect'

    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
        }

class quiz2_sol(Page):

    def is_displayed(self):
        return self.round_number == 1

###############################################################################
#### Pre Game Prep ############################################################
###############################################################################


class WaitPage(WaitPage):

    def is_displayed(self):
        return self.round_number >= 2 

    def after_all_players_arrive(self):
        pass

class pregame(Page):
    def is_displayed(self):
        return (self.round_number == 1)

    def after_all_players_arrive(self):
        pass

    def vars_for_template(self):

        ges_extra_2p = self.participant.vars['overall_ge_list'][:]
        ges_percent_extra_2p = self.participant.vars['overall_ge_percent_list'][:]
        ret_extra_2p = self.participant.vars['ret_scores'][:]
        poobar=[1,2,3,4]
        ges_team_2p = [
            self.player.get_others_in_group()[0].participant.vars['overall_own_ge'],   
            self.participant.vars['overall_own_ge']
            ]
        ges_percent_team_2p = [
            self.player.get_others_in_group()[0].participant.vars['overall_ge_percent'],   
            self.participant.vars['overall_ge_percent']
            ]

        for ges_percent_team_2p_val in ges_percent_team_2p:
          cnt = 0
          for ges_percent_extra_2p_val in ges_percent_extra_2p:
            if ges_percent_extra_2p_val ==  ges_percent_team_2p_val:
              ges_extra_2p.pop(cnt)
              ret_extra_2p.pop(cnt)
              ges_percent_extra_2p.pop(cnt)
              poobar.pop(cnt)
              cnt=cnt+1
              break
            else: 
              cnt=cnt+1

        # be careful with op_individual_exchange, used later for payoffs
        op_individual_exchange = [self.player.get_others_in_group()[0].participant.vars['ret_score'] - self.player.get_others_in_group()[0].participant.vars['overall_own_ge']]
        op_group_exchange = [self.player.get_others_in_group()[0].participant.vars['overall_own_ge']]

        cnt = 0
        for GE in ges_extra_2p:
            op_individual_exchange.append(ret_extra_2p[cnt] - ges_extra_2p[cnt])
            op_group_exchange.append(ges_extra_2p[cnt])
            cnt = cnt + 1

        self.participant.vars['group_exchange_other2p'] = ges_extra_2p
        self.participant.vars['individual_exchange_other2p'] = op_individual_exchange[1:3]


        round_points = (
            self.participant.vars["ret_score"] - self.participant.vars['overall_own_ge'] +
            0.5 * self.participant.vars['overall_own_ge'] - 
            (sum(op_individual_exchange) * 0.0) +
            sum(op_group_exchange) * 0.5
            )  

        # log in data base facts. 
        self.player.round_base_points = self.participant.vars['round_base_points'] = round_points
        self.player.op_ge_overallavg = self.participant.vars['op_group_exchange'] = op_group_exchange
        self.player.op_ret_scores = [self.player.get_others_in_group()[0].participant.vars['ret_score']] + ret_extra_2p


        return {

            # own info
            'revwPg_self_group_id':self.group.get_players(),
            'revwPg_self_ge_overallavg':self.participant.vars['overall_own_ge'],
            'revwPg_self_ret_score':self.participant.vars["ret_score"],  
            'revwPg_self_role':self.participant.vars["Role"],
            'revwPg_self_ge_percent':self.participant.vars["overall_ge_percent"] * 100,
            'revwPg_self_avg_individual_exchange':self.participant.vars["ret_score"] * (1 - self.participant.vars['overall_ge_percent']),
            'revwPg_self_ge':self.participant.vars['overall_own_ge'],
            'revwPg_self_group_exchange_score':0.5 * self.participant.vars['overall_own_ge'],
           
            # counter part player info
            'revwPg_counter_party_id':self.player.get_others_in_group(),
            'revwPg_counter_party_role':self.player.get_others_in_group()[0].participant.vars['Role'],  
            'revwPg_countery_party_ret_score':self.player.get_others_in_group()[0].participant.vars['ret_score'], 
            'revwPg_counter_party_ge_overallavg':self.player.get_others_in_group()[0].participant.vars['overall_own_ge'],
            'revwPg_counter_ge_percent':self.player.get_others_in_group()[0].participant.vars['overall_ge_percent'] * 100,

            # other players
            'revwPg_0_ges_overallavg_list':self.participant.vars['overall_ge_list'],
            'revwPg_0_ges_team_2p':ges_team_2p,
            'revwPg_0_ges_extra_2p':self.participant.vars['group_exchange_other2p'],
            'revwPg_0_ies_extra_2p':self.participant.vars['individual_exchange_other2p'],
            'revwPg_0_ret_extra_2p':ret_extra_2p,
            'revwPg_0_ret_scores':self.participant.vars["ret_scores"],
            'revwPg_0_poobar':poobar,
            'revwPg_0_ges_percent_overall_list':self.participant.vars['overall_ge_percent_list'],
            'revwPg_0_ges_percent_extra_2p':[i * 100 for i in ges_percent_extra_2p],
            'revwPg_0_ges_percent_team_2p':ges_percent_team_2p,
            'revwPg_op_individual_exchange': [round(i,2) for i in op_individual_exchange],
            'revwPg_score_op_individual_exchange':sum(op_individual_exchange) * 0.5,
            'revwPg_score_op_group_exchange':sum(op_group_exchange) * 0.5,
            'revwPg_op_group_exchange':[round(i,2) for i in op_group_exchange],
            'revwPg_round_points':self.player.round_base_points,


            'debug': settings.DEBUG,
        }      

    def after_all_players_arrive(self):
        pass



###############################################################################
#### A1 A2 ####################################################################
###############################################################################


class A_Stage1(Page):

    form_model = models.Player
    form_fields = ['A_stage1']

    def is_displayed(self):
        return (
            (self.round_number == 1) 
            & (self.participant.vars['Role'] == 'A') 
            & (self.participant.vars['stage_round'] <= Constants.stage_rounds))

    def vars_for_template(self):

        return {
            'stage_round':self.participant.vars['stage_round'],
            'Role_partic_var':self.participant.vars["Role"],
            'counter_party_id':self.player.get_others_in_group(),
            'counter_party_role':self.player.get_others_in_group()[0].participant.vars['Role'],    
            'counter_party_score':self.player.get_others_in_group()[0].participant.vars['final_score'], 
            'countery_party_ret_score':self.player.get_others_in_group()[0].participant.vars['ret_score'], 
            'counter_party_ge':self.player.get_others_in_group()[0].participant.vars['final_ge'],  
            'counter_party_overall_ge_percent':round(self.player.get_others_in_group()[0].participant.vars['overall_ge_percent']*100,2),    
            'self_ret_score':self.participant.vars["ret_score"], 
            'self_score':self.participant.vars['final_score'],
            'self_ge':self.participant.vars['final_ge'],
            'self_overall_ge_percent':round(self.participant.vars['overall_ge_percent']*100, 2),
        'revwPg_round_points':self.player.participant.vars['round_base_points'],
        'revwPg_self_ge_overallavg':self.participant.vars['overall_own_ge'],
        # 'revwPg_counterpart_round_points':self.player.get_others_in_group()[0].participant.vars['round_base_points'],

        }




class WaitPage_F1(WaitPage):

    def is_displayed(self):
        return (self.round_number == 1)


    def after_all_players_arrive(self):
        # another wait page, with logic to decide to skip all next rounds. 
        pass


###############################################################################
#### F1 F2 ####################################################################

class F_Stage2(Page):

    form_model = models.Player
    form_fields = ['F_stage2']

    def is_displayed(self):
        return ((self.round_number == 1) 
            & (self.participant.vars['Role'] == 'F') 
            & (self.participant.vars['end_this_stage_round'] == False)
            & (self.participant.vars['stage_round'] <= Constants.stage_rounds))

    def vars_for_template(self):

        return {
            'stage_round':self.participant.vars['stage_round'],
            'Role_partic_var':self.participant.vars["Role"],
            'counter_party_id':self.player.get_others_in_group(),
            'counter_party_role':self.player.get_others_in_group()[0].participant.vars['Role'],    
            'counter_party_score':self.player.get_others_in_group()[0].participant.vars['final_score'], 
            'countery_party_ret_score':self.player.get_others_in_group()[0].participant.vars['ret_score'], 
            'counter_party_ge':self.player.get_others_in_group()[0].participant.vars['final_ge'],  
            'counter_party_overall_ge_percent':round(self.player.get_others_in_group()[0].participant.vars['overall_ge_percent']*100,2),   
            'self_ret_score':self.participant.vars["ret_score"], 
            'self_score':self.participant.vars['final_score'],
            'self_ge':self.participant.vars['final_ge'],
            'self_overall_ge_percent':round(self.participant.vars['overall_ge_percent']*100, 2),
        'revwPg_round_points':self.player.participant.vars['round_base_points'],
        'revwPg_self_ge_overallavg':self.participant.vars['overall_own_ge'],
        'revwPg_counterpart_round_points':self.player.get_others_in_group()[0].participant.vars['round_base_points'],

        }




class WaitPage_A1(WaitPage):

    def is_displayed(self):
        return (self.round_number == 1)


    def after_all_players_arrive(self):
        # another wait page, with logic to decide to skip all next rounds. 
        pass



###############################################################################
#### A3 A4 ####################################################################



class A_Stage3(Page):

    form_model = models.Player
    form_fields = ['A_stage3']

    def is_displayed(self):
        return ((self.round_number == 1) 
            & (self.participant.vars['Role'] == 'A') 
            & (self.participant.vars['end_this_stage_round'] == False)
            & (self.participant.vars['stage_round'] <= Constants.stage_rounds))

    def vars_for_template(self):

        return {
        'stage_round':self.participant.vars['stage_round'],
        'Role_partic_var':self.participant.vars["Role"],
        'counter_party_id':self.player.get_others_in_group(),
        'counter_party_role':self.player.get_others_in_group()[0].participant.vars['Role'],    
        'counter_party_score':self.player.get_others_in_group()[0].participant.vars['final_score'], 
        'countery_party_ret_score':self.player.get_others_in_group()[0].participant.vars['ret_score'], 
        'counter_party_ge':self.player.get_others_in_group()[0].participant.vars['final_ge'],  
            'counter_party_overall_ge_percent':round(self.player.get_others_in_group()[0].participant.vars['overall_ge_percent']*100,2),    
        'self_ret_score':self.participant.vars["ret_score"], 
        'self_score':self.participant.vars['final_score'],
        'self_ge':self.participant.vars['final_ge'],
        'self_overall_ge_percent':round(self.participant.vars['overall_ge_percent']*100, 2),
        'revwPg_round_points':self.player.participant.vars['round_base_points'],
        'revwPg_self_ge_overallavg':self.participant.vars['overall_own_ge'],
        'revwPg_counterpart_round_points':self.player.get_others_in_group()[0].participant.vars['round_base_points'],

        }





class WaitPage_F2(WaitPage):

    def is_displayed(self):
        return (self.round_number == 1)


    def after_all_players_arrive(self):
        # another wait page, with logic to decide to skip all next rounds. 
        self.group.nature_move()



class Nature(Page):

    def is_displayed(self):
        return ((self.round_number == 1) 
            & (self.participant.vars['end_this_stage_round'] == False) 
            & (self.participant.vars['stage_round'] <= Constants.stage_rounds))

    def vars_for_template(self):

        return {
            'stage_round':self.participant.vars['stage_round'],
            'Role_partic_var':self.participant.vars["Role"],
            'counter_party_id':self.player.get_others_in_group(),
            'counter_party_role':self.player.get_others_in_group()[0].participant.vars['Role'],    
            'counter_party_score':self.player.get_others_in_group()[0].participant.vars['final_score'], 
            'countery_party_ret_score':self.player.get_others_in_group()[0].participant.vars['ret_score'], 
            'counter_party_ge':self.player.get_others_in_group()[0].participant.vars['final_ge'],  
            'counter_party_overall_ge_percent':round(self.player.get_others_in_group()[0].participant.vars['overall_ge_percent']*100,2),       
            'self_ret_score':self.participant.vars["ret_score"], 
            'self_score':self.participant.vars['final_score'],
            'self_ge':self.participant.vars['final_ge'],
            'self_overall_ge_percent':round(self.participant.vars['overall_ge_percent']*100, 2),
            'nature':self.player.Nature,
        'revwPg_round_points':self.player.participant.vars['round_base_points'],
        'revwPg_self_ge_overallavg':self.participant.vars['overall_own_ge'],
        'revwPg_counterpart_round_points':self.player.get_others_in_group()[0].participant.vars['round_base_points'],

        }


    def before_next_page(self):
        self.participant.vars['end_this_stage_round'] = True #end this round

        # define "termianl choice/node", see models.  
        self.player.set_terminal_node()


class Results(Page):

    def is_displayed(self):
        return ((self.round_number == 1) 
            & (self.participant.vars['end_this_stage_round'] == True)
            & (self.participant.vars['stage_round'] <= Constants.stage_rounds))


    def vars_for_template(self):

        TN = self.player.terminal_choice
        if ((TN == "A1") |(TN == "A2")):
            self.group.A1A2_update()
        elif ((TN == "F1") |(TN == "F2")):
            self.group.F1F2_update()
        elif ((TN == "A3") |(TN == "A4")):
            self.group.A3A4_update()
        elif ((TN == "N1") |(TN == "N2")):
            self.group.Nature_update()
         


        ges_extra_2p = self.participant.vars['overall_ge_list'][:]
        ges_percent_extra_2p = self.participant.vars['overall_ge_percent_list'][:]
        ret_extra_2p = self.participant.vars['ret_scores'][:]
        poobar=[1,2,3,4]
        ges_team_2p = [
            self.player.get_others_in_group()[0].participant.vars['overall_own_ge'],   
            self.participant.vars['overall_own_ge']
            ]
        ges_percent_team_2p = [
            self.player.get_others_in_group()[0].participant.vars['overall_ge_percent'],   
            self.participant.vars['overall_ge_percent']
            ]

        for ges_percent_team_2p_val in ges_percent_team_2p:
          cnt = 0
          for ges_percent_extra_2p_val in ges_percent_extra_2p:
            if ges_percent_extra_2p_val ==  ges_percent_team_2p_val:
              ges_extra_2p.pop(cnt)
              ret_extra_2p.pop(cnt)
              ges_percent_extra_2p.pop(cnt)
              poobar.pop(cnt)
              cnt=cnt+1
              break
            else: 
              cnt=cnt+1

        # be careful with op_individual_exchange, used later for payoffs
        op_individual_exchange = [self.player.get_others_in_group()[0].participant.vars['ret_score'] - self.player.get_others_in_group()[0].participant.vars['overall_own_ge']]
        op_group_exchange = [self.player.get_others_in_group()[0].participant.vars['overall_own_ge']]

        cnt = 0
        for GE in ges_extra_2p:
            op_individual_exchange.append(ret_extra_2p[cnt] - ges_extra_2p[cnt])
            op_group_exchange.append(ges_extra_2p[cnt])
            cnt = cnt + 1

        self.participant.vars['group_exchange_other2p'] = ges_extra_2p
        self.participant.vars['individual_exchange_other2p'] = op_individual_exchange[1:3]


        round_points = (
            self.participant.vars["ret_score"] - self.participant.vars['overall_own_ge'] +
            0.5 * self.participant.vars['overall_own_ge'] - 
            (sum(op_individual_exchange) * 0.0) +
            sum(op_group_exchange) * 0.5
            ) 

    

        # use this to double check your models.py payoff function is working right. 
        round_points_alt = self.player.postStage_self_individual_exchange + (0.5 * self.player.postStage_self_ge) - 0.5 * sum(json.loads(self.player.postStage_op_individual_exchange)) + 0 + Constants.automatic_earnings


        return {
            'stage_round':self.participant.vars['stage_round'],
            'nature':self.player.Nature,
            'Role_partic_var':self.participant.vars["Role"],
            'counter_party_id':self.player.get_others_in_group(),
            'counter_party_role':self.player.get_others_in_group()[0].participant.vars['Role'],    
            'counter_party_score':self.player.get_others_in_group()[0].participant.vars['final_score'], 
            'countery_party_ret_score':self.player.get_others_in_group()[0].participant.vars['ret_score'], 
            'counter_party_ge':self.player.get_others_in_group()[0].participant.vars['final_ge'],  
            'counter_party_overall_ge_percent':self.player.get_others_in_group()[0].participant.vars['overall_ge_percent']*100,   
            'self_ret_score':self.participant.vars["ret_score"], 
            'self_score':self.participant.vars['final_score'],
            'self_overall_ge_percent':self.participant.vars['overall_ge_percent']*100,
            'self_round_payoff':self.player.round_payoff,
            'counter_party_round_payoff':self.player.get_others_in_group()[0].round_payoff,
            'terminal_choice':self.player.terminal_choice,

            'self_avg_individual_exchange':self.player.postStage_self_individual_exchange,
            'self_ge':self.player.postStage_self_ge,
            'self_group_exchange_score':(0.5 * self.player.postStage_self_ge),
            'op_individual_exchange':[round(i,2) for i in json.loads(self.player.postStage_op_individual_exchange)],
            'score_op_individual_exchange':0.5 * sum(json.loads(self.player.postStage_op_individual_exchange)),
            'score_op_group_exchange':0.5 * sum(json.loads(self.player.postStage_op_group_exchange)),
            'op_group_exchange':[round(i,2) for i in json.loads(self.player.postStage_op_group_exchange)],
            'round_points_alt':round_points_alt,
            'round_points':self.player.postStage_round_points,
            
            # own info
            'revwPg_self_group_id':self.group.get_players(),
            'revwPg_self_ge_overallavg':self.participant.vars['overall_own_ge'],
            'revwPg_self_ret_score':self.participant.vars["ret_score"],  
            'revwPg_self_role':self.participant.vars["Role"],
            'revwPg_self_ge_percent':self.participant.vars["overall_ge_percent"] * 100,
            'revwPg_self_avg_individual_exchange':self.participant.vars["ret_score"] * (1 - self.participant.vars['overall_ge_percent']),
            'revwPg_self_ge':self.participant.vars['overall_own_ge'],
            'revwPg_self_group_exchange_score':0.5 * self.participant.vars['overall_own_ge'],
           
            # counter part player info
            'revwPg_counter_party_id':self.player.get_others_in_group(),
            'revwPg_counter_party_role':self.player.get_others_in_group()[0].participant.vars['Role'],  
            'revwPg_countery_party_ret_score':self.player.get_others_in_group()[0].participant.vars['ret_score'], 
            'revwPg_counter_party_ge_overallavg':self.player.get_others_in_group()[0].participant.vars['overall_own_ge'],
            'revwPg_counter_ge_percent':self.player.get_others_in_group()[0].participant.vars['overall_ge_percent'] * 100,

            # other players
            'revwPg_0_ges_overallavg_list':self.participant.vars['overall_ge_list'],
            'revwPg_0_ges_team_2p':ges_team_2p,
            'revwPg_0_ges_extra_2p':self.participant.vars['group_exchange_other2p'],
            'revwPg_0_ies_extra_2p':self.participant.vars['individual_exchange_other2p'],
            'revwPg_0_ret_extra_2p':ret_extra_2p,
            'revwPg_0_ret_scores':self.participant.vars["ret_scores"],
            'revwPg_0_poobar':poobar,
            'revwPg_0_ges_percent_overall_list':self.participant.vars['overall_ge_percent_list'],
            'revwPg_0_ges_percent_extra_2p':[i * 100 for i in ges_percent_extra_2p],
            'revwPg_0_ges_percent_team_2p':ges_percent_team_2p,
            'revwPg_op_individual_exchange': [round(i,2) for i in op_individual_exchange],
            'revwPg_score_op_group_exchange':sum(op_group_exchange) * 0.5,
            'revwPg_score_op_individual_exchange':sum(op_individual_exchange) * 0.5,
            'revwPg_op_group_exchange':[round(i,2) for i in op_group_exchange],
            'revwPg_round_points':round_points,
        }

    def before_next_page(self):
        self.participant.vars['end_this_stage_round'] = False
        self.participant.vars['stage_round'] = self.participant.vars['stage_round'] + 1




class FinalResults(Page):

    def is_displayed(self):
        return (self.participant.vars['stage_round'] > Constants.stage_rounds)


    def vars_for_template(self):

        table_rows = []
        roundNum = 1
        final_score = 0
        for prev_player in self.player.in_all_rounds():
            if prev_player.round_payoff != None:
                prev_player.payoff = c(prev_player.round_payoff) * prev_player.participant.vars['final_score_discounter']
                final_score += prev_player.round_payoff

                row = {
                    '00_round_number': roundNum ,
                    '01_A_stage1':prev_player.A_stage1,
                    '02_F_stage2':prev_player.F_stage2,
                    '03_A_stage3':prev_player.A_stage3,
                    "04_Nature":prev_player.Nature,
                    '05_terminal_choice':prev_player.terminal_choice,
                    '06_payoff':prev_player.payoff,
                }
                table_rows.append(row)
                roundNum += 1


        self.player.payoff = self.player.payoff + (self.participant.vars['final_score'] * self.participant.vars['final_score_discounter'])
        self.player.payoff = round_up(self.player.payoff, 5)


        #this logs payoffs into the otree "SessionPayments" screen, 
        # it needs to come after prev_player.payoff is set
        self.session.config['participation_fee'] = c(30).to_real_world_currency(self.session)
        self.session.config['real_world_currency_per_point'] = decimal.Decimal(1.0)

        return {
        'debug': settings.DEBUG,
        'part1_score':self.participant.vars["ret_score"],
        'part2_score':self.participant.vars['final_score'],
        'part2_cash':(self.participant.vars['final_score'] * self.participant.vars['final_score_discounter']),
        'final_score':c(round(final_score,1)),
        'part3_cash':self.player.payoff - (self.participant.vars['final_score'] * self.participant.vars['final_score_discounter']),
        'table_rows': table_rows,
        'Role_self':self.player.player_role,
        'showupfee':self.session.config['participation_fee'],
        'point_aed_convert':round(1/prev_player.participant.vars['final_score_discounter'],2),
        'final_cash':(c(self.player.payoff).to_real_world_currency(self.session) + self.session.config['participation_fee'])
        }


page_sequence = [
    InitWaitPage,
    Instructions,
    quiz1,
    quiz1_sol,
    quiz2,
    quiz2_sol,
    WaitPage, 
    pregame,
    A_Stage1,
    WaitPage_F1,
    F_Stage2,
    WaitPage_A1,
    A_Stage3,
    WaitPage_F2,
    Nature,
    Results,
    FinalResults,
    ]