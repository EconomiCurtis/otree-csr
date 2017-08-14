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
    name_in_url = 'csr_3_stage'
    players_per_group = 2
    num_rounds = 11
    stage_rounds = 1 # moved to stratagey method, one round only
    automatic_earnings = 0
    endowment_boost = 0
    final_score_discounter = 0.25
    instructions_template = 'csr_3_stageT/instruc.html'
    review_template = 'csr_3_stageT/review.html'

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

		for p in self.get_players():
			p.mpcr     = self.session.config['mpcr']
			p.GE_Low_A  = self.session.config['GE_Low_A']
			p.GE_Low_F  = self.session.config['GE_Low_F']
			p.boycott_cost =self.session.config['boycott_cost']
			p.A1_A_mult = self.session.config['A1_A_mult']
			p.A1_F_mult = self.session.config['A1_F_mult']
			p.F1_A_mult = self.session.config['F1_A_mult']
			p.F1_F_mult = self.session.config['F1_F_mult']
			p.A3_A_mult = self.session.config['A3_A_mult']
			p.A3_F_mult = self.session.config['A3_F_mult']
			p.N1_prob   = self.session.config['N1_prob']
			p.stage_round_count = self.session.config['stage_round_count']
			self.session.vars['stage_round_count'] = self.session.config['stage_round_count']


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
			p.set_round_payoff() # set scores # set scores



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
			p.set_round_payoff() # set scores

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
				p.set_round_payoff() # set scores # set scores

		elif A_player.terminal_choice == 'A4':  #A4
			pass


	def nature_move(self):

		cutoff = int((self.session.config['N1_prob'] * 100 ) // 1)

		if random.randint(0,100) <= cutoff:
			nature_move = 'N1' # self.session.config['N1_prob'] chance of N1
		else: nature_move = 'N2'

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
				p.set_round_payoff() # set scores
		elif F_player.terminal_choice == 'N2':
			for p in self.get_players():
				if p.participant.vars['Role'] == 'A':
					A_GE = 2 * (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score'])
					A_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost
				elif p.participant.vars['Role'] == 'F':
					F_GE = (p.participant.vars['overall_ge_percent'] * p.participant.vars['ret_score'])
					F_Endow = p.participant.vars['ret_score'] + Constants.endowment_boost
			for p in self.get_players():
				p.set_round_payoff() # set scores




class Player(BasePlayer):

	player_role=models.CharField(doc="player role, A or F")


	quiz_01_a = models.FloatField(
	    verbose_name="In A1, Role F's Group Exchange Contribution",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_01_a answer In A1, Role F's Group Exchange Contribution''')
	quiz_01_b = models.FloatField(
	    verbose_name="In A1, Role A's Group Exchange Contribution",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_01_b answer In A1, Role A's Group Exchange Contribution''')
	quiz_01_c = models.FloatField(
	    verbose_name="In A1, Role A's Score",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_01_c answer In A1, Role A's Score''')
	quiz_01_d = models.FloatField(
	    verbose_name="In A1, Role F's Score",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_01_d answer In A1, Role F's Score''')
	quiz_01_e = models.FloatField(
	    verbose_name="In F1, Role A's Score",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_01_c answer In F1, Role A's Score''')
	quiz_01_f = models.FloatField(
	    verbose_name="In F1, Role F's Score",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_01_d answer In F1, Role F's Score''')
	  


	quiz_02_a = models.FloatField(
	    verbose_name="In N1, Role A's Score",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_02_a answer In N1, Role A's Score''')
	quiz_02_b = models.FloatField(
	    verbose_name="In N1, Role F's Score",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_02_b answer In N1, Role F's Score''')
	quiz_02_c = models.FloatField(
	    verbose_name="In N2, Role A's Score",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_02_c answer In N2, Role A's Score''')
	quiz_02_d = models.FloatField(
	    verbose_name="In N2, Role F's Score",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_02_d answer In N2, Role F's Score''')
	quiz_02_e = models.FloatField(
	    verbose_name="The Probability of N1 Occurring",
	    min = 0,
	    max = 999,
	    initial=None,
	    doc='''quiz_02_e answer The Probability of N1 Occurring''')




	ret_score = models.IntegerField(
		doc="player's real effort task score - correct number of RETs mapped to a number.")

	vcm_score = models.FloatField(
		doc="score player received in vcm round.")

	vcm_ge_percent = models.FloatField(
		doc="player's average group exchange contribution in vcm rounds")

	passive_Player_Earnings = models.FloatField(
		doc = ''' The score of this round's passive player.  ''')




	def set_round_payoff(self):
		"""calc player payoffs"""
		''' called inside group functions, eg A1A2_update '''

		for p in self.group.get_players():

			# group exchange
			F_GE = (p.GE_Low_F)
			if ((p.terminal_choice == 'F1') | (p.terminal_choice == 'N1')):
				F_GE = (p.GE_Low_F * p.F1_F_mult)
			GE = p.GE_Low_A + F_GE + 40

			#scores
			A_score = (GE * p.mpcr) + (20 - p.GE_Low_A)
			F_score = (GE * p.mpcr) + (20 - F_GE)

			if ((p.terminal_choice == 'N2') | (p.terminal_choice == 'N1')):
				A_score = (GE * p.mpcr) + (20 - p.GE_Low_A) - p.boycott_cost

			if (p.participant.vars['Role'] == 'A'):
				p.postStage_self_individual_exchange = 20 - p.GE_Low_A
				p.postStage_self_ge = p.GE_Low_A
				p.postStage_op_individual_exchange = str(20 - F_GE)
				p.postStage_op_group_exchange = str(F_GE)
				p.round_payoff = A_score
				p.postStage_round_points = A_score

			elif (p.participant.vars['Role'] == 'F'):
				p.postStage_self_individual_exchange = F_GE
				p.postStage_self_ge = p.GE_Low_F
				p.postStage_op_individual_exchange = str(20 - p.GE_Low_A)
				p.postStage_op_group_exchange = str(p.GE_Low_A)
				p.postStage_round_points = F_score
				p.round_payoff = F_score

	def set_payoff(self, round):
		# in views, determine round to pay
		# similar to VCM
		pass


	def passivePlayerEarnings(self):
		for p in self.group.get_players():

			# group exchange
			F_GE = (p.GE_Low_F)
			if ((p.terminal_choice == 'F1') | (p.terminal_choice == 'N1')):
				F_GE = (p.GE_Low_F * p.F1_F_mult)
			GE = p.GE_Low_A + F_GE + 40

			self.passive_Player_Earnings = (GE * p.mpcr)

			#scores
			return (GE * p.mpcr)




	stage_round_count = models.PositiveIntegerField(
		doc='The stage round number.'
		)

	paid_round=models.PositiveIntegerField(
		doc=''' Paid stage round ''')

	paid_active_round_score=models.FloatField(
		doc=''' Score from paid actie player round''')

	round_payoff=models.FloatField(
		doc="this player's earnings this round")

	GE_Low_A = models.FloatField(
		doc="player A's group exchange contribution at 1X")
	GE_Low_F = models.FloatField(
		doc="player F's group exchange contribution at 1X")

	mpcr = models.FloatField(
		doc="marginal per-capita rate of return to vcm game")

	boycott_cost = models.FloatField(
		doc="cost of boycoff to player A")
	passive_ge_contrib = models.FloatField(
		doc="passive players' total contribution to group exchange")

	A1_A_mult = models.FloatField(
		doc="multiplier on GE of A at node A1")
	A1_F_mult = models.FloatField(
		doc="multiplier on GE of F at node A1")

	F1_A_mult = models.FloatField(
		doc="multiplier on GE of A at node F1")
	F1_F_mult = models.FloatField(
		doc="multiplier on GE of F at node F1")

	A3_A_mult = models.FloatField(
		doc="multiplier on GE of A at node A3")
	A3_F_mult = models.FloatField(
		doc="multiplier on GE of F at node A3")

	N1_prob = models.FloatField(
		doc="Probability of N1, where prob of N2 is (1 - N1_prob)")



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

	followup_1 = models.CharField(
		)

	# Survey questions

	q_birthMonth = models.PositiveIntegerField(
		verbose_name="What is the month of your birth?",
		choices=[1,2,3,4,5,6,7,8,9,10,11,12],
		doc = ''' birth month ''',
		)
	q_birthYear = models.PositiveIntegerField(
		verbose_name="What is the year of your birth?",
		min=1900,
		max = 2016,
		doc = ''' birth year ''',
		)
	q_sex = models.CharField(
		verbose_name="Are you male or female?",
		choices=["male","female"],
		doc = ''' male or female ''',
		)

	q_languages = models.CharField(
		verbose_name = "What language do you speak most often at home?",
		doc = '''languages''',
		)

	q_YearsInUAE = models.PositiveIntegerField(
		verbose_name="How long have you lived in the UAE (in years)?",
		doc = ''' How long have you lived in the UAE (in years)? ''',
		)

	q_nationality = models.CharField(
		verbose_name="What is your nationality?",
		doc = ''' What is your nationality? ''',
		)

	q_major = models.CharField(
		verbose_name="What is your major?",
		doc = ''' What is your major? ''',
		)

	q_part2strat = models.CharField(
		verbose_name="In Part 2, how did you decide how much to contribute to the group exchange?",
		doc = ''' In Part 2, how did you decide how much to contribute to the group exchange? ''',
		widget=widgets.Textarea
		)

	q_part3_A1strat = models.CharField(
		blank = None,
		verbose_name="In Part 3, if you were a Role A player, how did you decide between A1 and A2?",
		doc = ''' In Part 3, if you were a Role A player, how did you decide between A1 and A2? ''',
		widget=widgets.Textarea)
		
	q_part3_F1strat = models.CharField(
		blank = None,
		verbose_name="In Part 3, if you were a Role F player, how did you decide between F1 and F2?",
		doc = ''' In Part 3, if you were a Role F player, how did you decide between F1 and F2? ''',
		widget=widgets.Textarea)
		
	q_part3_A3strat = models.CharField(
		blank = None,
		verbose_name="In Part 3, if you were a Role A player, how did you decide between A3 and A4?",
		doc = ''' In Part 3, if you were a Role A player, how did you decide between A3 and A4? ''',
		widget=widgets.Textarea)

	q_part3_dynamic = models.CharField(
		blank = None,
		verbose_name="In Part 3, how did your strategy change over the many rounds you played?",
		doc = ''' In Part 3, how did your strategy change over rounds? ''',
		widget=widgets.Textarea)
		