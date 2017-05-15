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
First implementation by Curtis Kephart (curtiskephart@gmail.com) 2017.05
Quiz
"""

class Constants(BaseConstants):
    name_in_url = 'csr_quiz_wg'
    players_per_group = 2
    task_timer = 270
    num_rounds = 5
    instructions_template = 'csr_1_quiz/instruc.html'
    questions = []





class Subsession(BaseSubsession):

    def before_session_starts(self):

        # setup quiz questions.
        questions = [
            {
                'quiz_text':"<h3>Every member of your group has 20 points available to invest.</h3><h3>How many points would <u>you</u> earn if you invest 10 points into the Individual Exchange, and 10 points into the Group Exchange?</h3> <h3>Assume that the other three players each place 10 points in the Group Exchange.</h3><br>",
                'quiz_sol':(10 + 40 * self.session.config['mpcr']),
                'quiz_sol_text':'csr_1_quiz/sol/quiz1sol.html'
            },
            {
                'quiz_text':"<h3>You and every other member of your group has 20 points available to invest.</h4><h3>How many points would <u>each of your group members</u> earn if <b>you</b> invest 10 points into the Individual Exchange, and 10 points into the Group Exchange?</h4><h3>Assume that the other members of your group distribute to the Individual and Group Exchange the same as you.</h4><br>",
                'quiz_sol':(10 + 40 * self.session.config['mpcr']),
                'quiz_sol_text':'csr_1_quiz/sol/quiz2sol.html'
            },
            {
                'quiz_text':"<h3>Every member of your group has 20 points available to invest.</h3><h3>How many points would <u>you</u> earn if you invest all of your points into the Individual Exchange, (0 points into the Group Exchange)?</h3> <h3>Assume that the other three players each place 10 points in the Group Exchange.</h4><br>",
                'quiz_sol':(20 + 30 * self.session.config['mpcr']),
                'quiz_sol_text':'csr_1_quiz/sol/quiz3sol.html'
            },
            {
                'quiz_text':"<h3>Every member of your group has 20 points available to invest.</h3><h3>How many points would <u>you</u> earn if you invest all of your points into the Group Exchange, (0 points into the Individual Exchange)?</h3> <h3>Assume that the other three players each place 10 points in the Group Exchange.</h4><br>",
                'quiz_sol':(50 * self.session.config['mpcr']),
                'quiz_sol_text':'csr_1_quiz/sol/quiz4sol.html'
            },
            {
                'quiz_text':"<h3>Every member of your group has 20 points available to invest.</h3><h3>How many points would <u>you</u> earn if you invest 10 points into the Individual Exchange, and 10 points into the Group Exchange?</h3> <h3>Now assume that the other three players each place all their points in the Group Exchange.</h4><br>",
                'quiz_sol':(10 + 70 * self.session.config['mpcr']),
                'quiz_sol_text':'csr_1_quiz/sol/quiz5sol.html'
            },
        ]


        for i in range(len(questions)): # range here is number of questions
            Constants.questions.extend([questions[i]])

        for i in range(len(Constants.questions)):

            for p in self.get_players():
                if self.round_number == (i+1):
                    p.mpcr = self.session.config['mpcr']  
                    p.quiz_text = Constants.questions[i]['quiz_text']
                    p.quiz_sol = Constants.questions[i]['quiz_sol']
                    p.quiz_sol_text = Constants.questions[i]['quiz_sol_text']


class Group(BaseGroup):
	pass



class Player(BasePlayer):

    mpcr = models.FloatField(
        doc = '''marginal per capital reutrn ''')

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
