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

# </standard imports>



author = 'Curtis Kephart'

doc = """
CSR Experiment
This experiment ...
Designed by Chetan Dave and Alicja Reuben.
First implementation by Curtis Kephart (curtiskephart@gmail.com) 2016.11
"""

class Constants(BaseConstants):
    name_in_url = 'csr_realEffort'
    players_per_group = None
    task_timer = 120
    num_rounds = 126


    reference_texts = [
        'uIzR',
        'o8sA',
        'dWg5',
        '6kdA',
        'ep7o',
        'zflY',
        'CwNg',
        'OhZn',
        'Xw0w',
        'GJcR',
        'OJ2D',
        'kJ03',
        'L5O8',
        '1MUj',
        'GleS',
        '4gKx',
        'mSol',
        'oWKd',
        'OFFz',
        'CdsT',
        'Mf4U',
        'sUhJ',
        '1Ltw',
        '2mrm',
        'f5UI',
        'hNqN',
        'boJa',
        '2Pqv',
        'vLuq',
        'IYYP',
        'sy3O',
        'M9X6',
        'qflm',
        'ovAU',
        '7PaW',
        'YB4F',
        '2NFP',
        'h6QM',
        'xLkH',
        'izif',
        'r7Ml',
        'ERJ8',
        'geTe',
        'L15N',
        'uTKl',
        'wRuQ',
        'MFNc',
        'YS4B',
        '80uw',
        'syXc',
        'QgvI',
        'a5bk',
        'MqCQ',
        'E0Qi',
        'NzsZ',
        '1maT',
        'mN28',
        'BJet',
        'xBhz',
        'rkn7',
        '5r3d',
        'uTM0',
        'pYQD',
        'Rkn1',
        'FJIv',
        'pZMh',
        'GobN',
        'oVis',
        '3V4w',
        'zWtd',
        '5OZz',
        'ArfP',
        'IdzS',
        'mC9T',
        '7cIv',
        'TjcG',
        'fZ15',
        'NlsB',
        'tPX4',
        '3O3c',
        'HLTg',
        'de14',
        'MbqN',
        'xywd',
        'Z3Vz',
        'XS7V',
        'ErGB',
        'HlTl',
        '9Dmt',
        'LCwT',
        'y97e',
        '6PTp',
        'vCVC',
        'MG3S',
        'kzpF',
        'Y90ZQ4gFs287',
        'WSx7IJ8YMeAF',
        '6gt6k1dZfDdL',
        '8gkmGZY36lBI',
        'tz4hJ6NVBPBq',
        'SY3BOD92q0Uc',
        'FAojzXfsCvsc',
        '7Hoep0BQ5EgX',
        'TXVUwqGND0Hw',
        'Ig6hl84vsv05',
        'Lk5bKpQ13kTv',
        'bRsi7Cbd4gPs',
        'jY3X0XKXib1R',
        'e3Hs759fdegV',
        'NMtMkEyyyly3',
        'O2lG0j7cMaRk',
        'rkegxeTnoxM8',
        'Cs7Yn0FOgqFi',
        'GpZTwpsLUq0h',
        'EJB4YDNxKcQV',
        'zRAyc20FFGiM',
        'GSyitZNp3aCa',
        'fZPnL4W4Rk8U',
        'Cuw7jF0ERvtk',
        '7JAOg5tGMBic',
        'BXVXpjlFuIl6',
        '7zQTu9YeU0hn',
        'M8XxBg30iMjq',
        'Bv4jsM4PphLB',
        '3wdvp9cQMEKU',
        'V4x7BM8oqpMN',
	]




class Subsession(BaseSubsession):
	def before_session_starts(self):

		# how long is the real effort task time?
		# refer to settings.py settings.
		for p in self.get_players():
		    if 'ret_time' in self.session.config:
		        p.ret_timer = self.session.config['ret_time']
		    else:
		        p.ret_timer = Constants.task_timer


class Group(BaseGroup):
	pass

class Player(BasePlayer):


	ret_timer = models.PositiveIntegerField(
	    doc="""The length of the real effort task timer."""
	)
	user_text = models.CharField(
		doc="user's transcribed text")
	is_correct = models.BooleanField(
		doc="did the user get the task correct?")
	ret_final_score = models.IntegerField(
		doc="player's total score up to this round")
	round_payoff = models.FloatField(
		doc="total number of correct real effort tasks, completed before timer expired")




	def set_final_score(self):
		correct_cnt = 0
		for p in self.in_all_rounds():
			if p.round_payoff != None:
				correct_cnt = correct_cnt + p.round_payoff
			else:
				correct_cnt = correct_cnt + 0

		if correct_cnt == None:
			self.ret_final_score = 20
		elif (correct_cnt < 10):
			self.ret_final_score = 2 + (2 * correct_cnt)
		else:
			self.ret_final_score = 20
