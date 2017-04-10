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
CSR Experiment - quiz for cold prickle treatment, vcm round
Designed by Chetan Dave and Alicja Reuben.
First implementation by Curtis Kephart (curtiskephart@gmail.com) 2016.11
Quiz
"""

class Constants(BaseConstants):
    name_in_url = 'csr_quiz_cp'
    players_per_group = 4
    task_timer = 270
    num_rounds = 14    
    instructions_template = 'csr_1_quiz_coldPrickle/instruc.html'



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
	pass



class Player(BasePlayer):
    user_text = models.CharField(
    	doc="user's transcribed text")
    is_correct = models.BooleanField(
    	doc="did the user get the task correct?")
    final_score = models.IntegerField(
    	doc="player's total score up to this round")


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

    quiz_03 = models.PositiveIntegerField(
        verbose_name='Your earnings:',
        min = 0,
        max = 999,
        initial=None,
        doc='quiz answer')
      
    quiz_04 = models.FloatField(
        verbose_name='Your earnings:',
        min = 0,
        max = 999,
        initial=None,
        doc='quiz answer')
      
    quiz_05 = models.FloatField(
        verbose_name='Your earnings:',
        min = 0,
        max = 999,
        initial=None,
        doc='quiz answer')
      
    quiz_06= models.FloatField(
        verbose_name='Your earnings:',
        min = 0,
        max = 999,
        initial=None,
        doc='quiz answer')
      
    quiz_07 = models.FloatField(
        verbose_name='Your earnings:',
        min = 0,
        max = 999,
        initial=None,
        doc='quiz answer')
      





