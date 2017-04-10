# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from math import ceil




# </standard imports>



author = 'Curtis Kephart'

doc = """
CSR Experiment
This experiment ...
Designed by Chetan Dave and Alicja Reuben.
First implementation by Curtis Kephart (curtiskephart@gmail.com) 2016.11
"""

class Constants(BaseConstants):
    name_in_url = 'csr_3_stage_wp'
    players_per_group = 2
    num_rounds = 1
    stage_rounds = 1 # moved to stratagey method, one round only
    automatic_earnings = 0
    endowment_boost = 0
    final_score_discounter = 0.25
    instructions_template = 'csr_3_stageT_warmGlow/instruc.html'
    review_template = 'csr_3_stageT_warmGlow/review.html'

    def round_up(Num, RoundTo):
    	''' rounds up to nearest... RoundTo '''
    	return int(ceil(Num / float(RoundTo))) * RoundTo


class Subsession(BaseSubsession):

	def before_session_starts(self):

		for p in self.get_players():
		    if 'final_score_discounter' in self.session.config:
		        p.participant.vars['final_score_discounter'] = self.session.config['final_score_discounter']
		    else:
		        p.participant.vars['final_score_discounter'] = Constants.final_score_discounter





class Group(BaseGroup):
	
	def A1A2_update(self):

		A_player = [p for p in self.get_players() if p.participant.vars['Role'] == 'A'][0]
		F_player = [p for p in self.get_players() if p.participant.vars['Role'] == 'F'][0]

		A_GE = (A_player.participant.vars['overall_ge_percent'] * A_player.participant.vars['ret_score']) 
		A_Endow = A_player.participant.vars['ret_score'] + Constants.endowment_boost
		F_GE = (F_player.participant.vars['overall_ge_percent'] * F_player.participant.vars['ret_score']) 
		F_Endow = F_player.participant.vars['ret_score'] + Constants.endowment_boost

		# for p in self.get_players():
		# 	# p.participant.vars['end_this_stage_round'] = True #end this round
		# 	if p.participant.vars['Role'] == 'A':
		# 		A_GE = (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score']) 
		# 		A_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost
		# 	elif p.participant.vars['Role'] == 'F':
		# 		F_GE = (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score']) 
		# 		F_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost

		for p in self.get_players():
			p.set_payoff(A_GE, A_Endow, F_GE, F_Endow) # set scores # set scores



	def F1F2_update(self):

		A_player = [p for p in self.get_players() if p.participant.vars['Role'] == 'A'][0]
		F_player = [p for p in self.get_players() if p.participant.vars['Role'] == 'F'][0]

		if F_player.terminal_choice == 'F1': #F2 means pass to A to make decision A3/A4
			for p in self.get_players():
				# p.participant.vars['end_this_stage_round'] = True #end this round
				if p.participant.vars['Role'] == 'A':
					A_GE = (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score']) 
					A_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost
				elif p.participant.vars['Role'] == 'F':
					F_GE = 1.5 * (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score']) 
					F_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost
			p.set_payoff(A_GE, A_Endow, F_GE, F_Endow) # set scores

		elif F_player.terminal_choice == 'F2': #don't think i want to do anything in this case 
			pass
		else:
			pass

	def A3A4_update(self):

		A_player = [p for p in self.get_players() if p.participant.vars['Role'] == 'A'][0]
		F_player = [p for p in self.get_players() if p.participant.vars['Role'] == 'F'][0]

		#A4 means pass to Nature
		# A3 "If the Role A participant chooses A3, both participants again receive the amount they earned during Part 2."
		if A_player.terminal_choice == 'A3': 
			for p in self.get_players():
				# p.participant.vars['end_this_stage_round'] = True #end this round
				if p.participant.vars['Role'] == 'A':
					A_GE = (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score']) 
					A_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost
				elif p.participant.vars['Role'] == 'F':
					F_GE = (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score']) 
					F_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost

			for p in self.get_players():
				p.round_payoff = p.set_payoff(A_GE, A_Endow, F_GE, F_Endow) # set scores # set scores

		elif A_player.terminal_choice == 'A4':  #A4
			pass


	def nature_move(self):
		if random.randint(1,4) == 1:
			nature_move = 'N2' #25% chance of N2
		else: nature_move = 'N1'

		for p in self.get_players():
			p.Nature = nature_move

	def Nature_update(self):

		A_player = [p for p in self.get_players() if p.participant.vars['Role'] == 'A'][0]
		F_player = [p for p in self.get_players() if p.participant.vars['Role'] == 'F'][0]

		if F_player.terminal_choice == 'N1':
			for p in self.get_players():
				if p.participant.vars['Role'] == 'A':
					A_GE = 2 * (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score'])
					A_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost
				elif p.participant.vars['Role'] == 'F':
					F_GE = 1.5 * (p.participant.vars['ret_score'] * p.participant.vars['overall_ge_percent']) 
					F_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost
			for p in self.get_players():
				p.set_payoff(A_GE, A_Endow, F_GE, F_Endow) # set scores
		elif F_player.terminal_choice == 'N2':
			for p in self.get_players():
				if p.participant.vars['Role'] == 'A':
					A_GE = 2 * (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score'])
					A_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost
				elif p.participant.vars['Role'] == 'F':
					F_GE = (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score'])
					F_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost
			for p in self.get_players():
				p.set_payoff(A_GE, A_Endow, F_GE, F_Endow) # set scores





class Player(BasePlayer):

	player_role=models.CharField(doc="player role, A or F")


	quiz_01 = models.PositiveIntegerField(
	    verbose_name='Your earnings:',
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='quiz answer')
	  
	quiz_02 = models.PositiveIntegerField(
	    verbose_name='Your earnings:',
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='quiz answer')




	ret_score = models.IntegerField(
		doc="player's real effort task score - correct number of RETs mapped to a number.")

	vcm_score = models.FloatField(
		doc="score player received in vcm round.")

	vcm_ge_percent = models.FloatField(
		doc="player's average group exchange contribution in vcm rounds")

	op_ret_scores = models.CharField(
	    doc = 'this subjects opposing player ret scores from task 1.')

	op_ge_overallavg = models.CharField(
	    doc = 'this subjects opposing player overall average group contribution from vcm.')

	round_base_points = models.FloatField(
		doc = ''' player's base score. if no adjustments are made to own or counterpart GE contributions, player will earn this ''')



	def set_payoff(self, A_GE, A_Endow, F_GE, F_Endow):
		"""calc player payoffs"""
		''' called inside group functions, eg A1A2_update '''

		op_GE = self.participant.vars['group_exchange_other2p']
		op_IE = self.participant.vars['individual_exchange_other2p']

		for p in self.group.get_players():
			if p.participant.vars['Role'] == 'F':

				total_op_individual_exchange = (A_Endow - A_GE) + sum(op_IE)
				total_op_group_exchange = A_GE + sum(op_GE)

				p.round_payoff = (F_Endow - F_GE) - (0 * total_op_individual_exchange) + (1/2 * (F_GE + total_op_group_exchange))

				#for debugging and results screen
				p.postStage_self_individual_exchange = F_Endow - F_GE
				p.postStage_self_ge = F_GE
				p.postStage_op_individual_exchange = str([(A_Endow - A_GE)] + op_IE)
				p.postStage_op_group_exchange = str([A_GE] + op_GE)
				p.postStage_round_points = p.round_payoff



			elif p.participant.vars['Role'] == 'A':
				total_op_individual_exchange = (F_Endow - F_GE ) + sum(op_IE)
				total_op_group_exchange = F_GE + sum(op_GE)

				p.round_payoff = (A_Endow - A_GE) - (0 * total_op_individual_exchange) + (1/2 * (A_GE + total_op_group_exchange))

				#for debugging and results screen
				p.postStage_self_individual_exchange = A_Endow - A_GE
				p.postStage_self_ge = A_GE
				p.postStage_op_individual_exchange = str([(F_Endow - F_GE)] + op_IE)
				p.postStage_op_group_exchange = str([F_GE] + op_GE)
				p.postStage_round_points = p.round_payoff




	round_payoff=models.FloatField(
		doc="this player's earnings this round")

	A_stage1 = models.CharField(
		initial=None,
		choices=['A1', 'A2'],
		verbose_name='Make your decision',
		doc='Player A decision between A1 and A2, Stage 1',
		widget=widgets.RadioSelect())

	F_stage2 = models.CharField(
		initial=None,
		choices=['F1', 'F2'],
		verbose_name='Make your decision',
		doc='Player F decision between F1 and F2, Stage 2',
		widget=widgets.RadioSelect())

	A_stage3 = models.CharField(
		initial=None,
		choices=['A3', 'A4'],
		verbose_name='Make your decision',
		doc='Player A decision between A3 and A4, Stage 3',
		widget=widgets.RadioSelect())

	Nature = models.CharField(
		doc="""'Should nature move, this is nature's move""",
		widget=widgets.RadioSelect())


	terminal_choice = models.CharField(
		doc="""'the terminal node reached by A and F""",
		widget=widgets.RadioSelect())

	def set_terminal_node(self):
		"""explicitly define terminal node reached by A and F in this group"""
		A_tn = None
		F_tn = None
		N_tn = None #nature
		for p in self.group.get_players():
			p.player_role = p.participant.vars['Role']
			if p.participant.vars['Role'] == 'A':
				if p.A_stage1 == "A1": A_tn = "A1"
				elif p.A_stage3 == "A3": A_tn = "A3"
				elif p.A_stage3 == "A4": A_tn = "A4"
			elif p.participant.vars['Role'] == 'F':
				if p.F_stage2 == 'F1': F_tn = 'F1'
				elif p.F_stage2 == 'F2': F_tn = 'F2'

			if p.Nature == 'N1': N_tn = 'N1'
			elif p.Nature == 'N2': N_tn = 'N2'

		TN = None
		if A_tn == "A1": TN = A_tn
		elif F_tn == 'F1': TN = F_tn
		elif A_tn == "A3": TN = A_tn
		else: TN = N_tn

		for p in self.group.get_players():
			p.terminal_choice = TN


	postStage_self_individual_exchange = models.FloatField(
		doc='''"player's individual exchange contribution after stage game"''')

	postStage_self_ge = models.FloatField(
		doc='''"player's group exchange contribution after stage game"''')

	postStage_op_individual_exchange = models.CharField(
		doc='''"player's three other countryparty player's individual after stage game"''')

	postStage_op_group_exchange = models.CharField(
		doc='''"player's three other countryparty player's group exchange after stage game"''')

	postStage_round_points = models.FloatField(
		doc='''"player's final score from stage game"''')






