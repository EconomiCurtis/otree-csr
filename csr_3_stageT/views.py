from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings
import time
import numpy
import decimal


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
            p.role = p.participant.vars['Role']

        ##############################################################

        # set previous rounds data into experiment output file
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
            'own_ge_percent':self.participant.vars['overall_ge_percent_list'][self.player.id_in_group - 1],
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
        if (value != 60):
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
        if (value != 40):
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

        ges_extra_2p = self.participant.vars['final_ges'][:]
        ges_team_2p = [self.player.get_others_in_group()[0].participant.vars['final_ge'], self.participant.vars['final_ge']]
        for ges_team_2p_val in ges_team_2p:
          cnt = 0
          for ges_extra_2p_val in ges_extra_2p:
            if ges_extra_2p_val ==  ges_team_2p_val:
              ges_extra_2p.pop(cnt)
              cnt=cnt+1
            else: 
              cnt=cnt+1

        ges_percent_extra_2p = self.participant.vars['overall_ge_percent_list'][:]
        ges_percent_team_2p = [
            self.participant.vars['overall_ge_percent'], 
            self.player.get_others_in_group()[0].participant.vars['overall_ge_percent']]
        for ges_percent_team_2p_val in ges_percent_team_2p:
          cnt = 0
          for ges_percent_extra_2p_val in ges_percent_extra_2p:
            if ges_percent_extra_2p_val ==  ges_percent_team_2p_val:
              ges_percent_extra_2p.pop(cnt)
              cnt=cnt+1
            else: 
              cnt=cnt+1


        

        return {
        'ges_team_2p':ges_team_2p,
        'ges_percent_team_2p':ges_percent_team_2p,
        'ges_percent_extra_2p':[i * 100 for i in ges_percent_extra_2p],
        'ges_extra_2p':ges_extra_2p,
        'player_role_list':self.participant.vars["player_role_list"],
        'stage_round':self.participant.vars['stage_round'],
        'Role_self':self.player.role,
        'Role_partic_var':self.participant.vars["Role"],
        'counter_party_id':self.player.get_others_in_group(),
        'counter_party_role':self.player.get_others_in_group()[0].participant.vars['Role'],    
        'counter_party_score':self.player.get_others_in_group()[0].participant.vars['final_score'], 
        'countery_party_ret_score':self.player.get_others_in_group()[0].participant.vars['ret_score'], 
        'counter_party_ge':self.player.get_others_in_group()[0].participant.vars['final_ge'],  
        'counter_party_overall_ge_percent':round(self.player.get_others_in_group()[0].participant.vars['overall_ge_percent'],2)*100,   
        'self_ret_score':self.participant.vars["ret_score"], 
        'self_score':self.participant.vars['final_score'],
        'self_ge':self.participant.vars['final_ge'],
        'self_overall_ge_percent':self.participant.vars['overall_ge_percent']*100,
        'overall_ge_percent_list':self.participant.vars['overall_ge_percent_list'],
        'own_ge_percent':self.participant.vars['overall_ge_percent_list'][self.player.id_in_group - 1],
        'ret_scores':self.participant.vars["ret_scores"],
        'role':self.participant.vars['Role'],
        'final_scores':self.participant.vars['final_scores'],
        'final_ges':self.participant.vars['final_ges'],
        'ret_scores':self.participant.vars["ret_scores"],
        'overall_ge_percent_list':self.participant.vars['overall_ge_percent_list'],


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
        }




class WaitPage_F1(WaitPage):

    def is_displayed(self):
        return (self.round_number == 1)


    def after_all_players_arrive(self):
        # another wait page, with logic to decide to skip all next rounds. 
        self.group.A1A2_update()


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
        }




class WaitPage_A1(WaitPage):

    def is_displayed(self):
        return (self.round_number == 1)


    def after_all_players_arrive(self):
        # another wait page, with logic to decide to skip all next rounds. 
        self.group.F1F2_update()




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
        }





class WaitPage_F2(WaitPage):

    def is_displayed(self):
        return (self.round_number == 1)


    def after_all_players_arrive(self):
        # another wait page, with logic to decide to skip all next rounds. 
        self.group.A3A4_update()
        self.group.nature_move()



class Nature(Page):

    def is_displayed(self):
        return ((self.round_number == 1) 
            & (self.participant.vars['end_this_stage_round'] == False) 
            & (self.participant.vars['stage_round'] <= Constants.stage_rounds))

    def vars_for_template(self):

        self.group.Nature_update()

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
        }


    def before_next_page(self):
        self.participant.vars['end_this_stage_round'] = True #end this round

class Results(Page):

    def is_displayed(self):
        return ((self.round_number == 1) 
            & (self.participant.vars['end_this_stage_round'] == True)
            & (self.participant.vars['stage_round'] <= Constants.stage_rounds))


    def vars_for_template(self):

        # define "termianl choice/node", see models.  
        self.player.set_terminal_node()

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
            'self_ge':self.participant.vars['final_ge'],
            'self_overall_ge_percent':self.participant.vars['overall_ge_percent']*100,
            'self_round_payoff':self.player.round_payoff,
            'counter_party_round_payoff':self.player.get_others_in_group()[0].round_payoff,
            'terminal_choice':self.player.terminal_choice,
            
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

        #this logs payoffs into the otree "SessionPayments" screen, 
        # it needs to come after prev_player.payoff is set
        self.session.config['participation_fee'] = c(30).to_real_world_currency(self.session)
        self.session.config['real_world_currency_per_point'] = decimal.Decimal(1.0)

        return {
        'debug': settings.DEBUG,
        'part1_score':self.participant.vars["ret_score"],
        'part2_score':self.participant.vars['final_score'],
        'final_score':c(round(final_score,1)),
        'variable_cash':c(self.player.payoff).to_real_world_currency(self.session),
        'table_rows': table_rows,
        'Role_self':self.player.role,
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