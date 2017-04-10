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
CSR Experiment - quiz for warm glow treatment vcm game
Designed by Chetan Dave and Alicja Reuben.
First implementation by Curtis Kephart (curtiskephart@gmail.com) 2017.01
Quiz
"""

class Constants(BaseConstants):
    name_in_url = 'csr_quiz_wg'
    players_per_group = 2
    task_timer = 270
    num_rounds = 5
    instructions_template = 'csr_1_quiz/instruc.html'

    questions = [
        {
            'quiz_text':"<h3>Each member of your group has 20 points available to invest.</h3> <h3>How many points would <b>you</b> earn if you invest 10 points into the Individual Exchange, and 10 points into the Group Exchange?</h3> <h3>Assume that the other player places 10 points in the Group Exchange.</h3>",
            'quiz_sol':1,
            'quiz_sol_text':"quiz_sol_text 1"
        },
        {
            'quiz_text':"quiz question text 2",
            'quiz_sol':2,
            'quiz_sol_text':"quiz_sol_text 2"
        },
    ]




class Subsession(BaseSubsession):

    # setup quiz questions.
    def before_session_starts(self):
    	for p in self.get_players():
    	    for i in range(len(Constants.questions)):
                if self.round_number == (i+1):
                    p.quiz_text = Constants.questions[i]['quiz_text']
                    p.quiz_sol = Constants.questions[i]['quiz_sol']
                    p.quiz_sol_text = Constants.questions[i]['quiz_sol_text']

class Group(BaseGroup):
	pass



class Player(BasePlayer):
    is_correct = models.BooleanField(
    	doc="did the user get the task correct?")
    final_score = models.IntegerField(
    	doc="player's total score up to this round")
    quiz_text = models.CharField(
    	doc="quiz question")
    quiz_sol = models.IntegerField(
    	doc="solution")
    quiz_user_answer = models.PositiveIntegerField(
        verbose_name='Your answer:',
        min = 0,
        max = 999,
        initial=None,
        doc='quiz answer')
    quiz_sol_text = models.CharField(
    	doc="solution text")
