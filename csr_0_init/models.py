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
    name_in_url = 'csr_init'
    players_per_group = 4
    task_timer = 30
    num_rounds = 200



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
    pass
