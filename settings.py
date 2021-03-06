import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import decimal

import otree.settings



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True


# don't share this with anybody.
SECRET_KEY = '+q02kxs2*)m+@0#9j*qo%pkpl=2_!hl%$&jdwzqb&746(soy8z'

# To use a database other than sqlite,
# set the DATABASE_URL environment variable.
# Examples:
# postgres://USER:PASSWORD@HOST:PORT/NAME
# mysql://USER:PASSWORD@HOST:PORT/NAME

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}



# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AED '
USE_POINTS = True


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree','mathfilters']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree on GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Here are various games implemented with oTree.
</p>
"""

ROOMS = [
    # {
    #     'name': 'econ101',
    #     'display_name': 'Econ 101 class',
    #     'participant_label_file': '_rooms/econ101.txt',
    # },
    # {
    #     'name': 'live_demo',
    #     'display_name': 'Room for live demo (no participant labels)',
    # },
    {
        'name': 'ssel_b_side',
        'display_name': 'SSEL Desktops B01 - B24',
        'participant_label_file': '_rooms/ssel_b_side.txt',
    },
]


# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # qualification.LocaleRequirement("EqualTo", "US"),
        # qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        # qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {

    'real_world_currency_per_point': 1.0,
    'participation_fee': 30.0,
    'doc': "CSR Testing",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    # 
    # {
    #     'name': 'csr',
    #     'display_name': "CSR: Intructions, RET, VCM, Stage, Payment",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'csr_0_init','csr_0_realeffort','csr_1_quiz_coldPrickle','csr_2_vcm_coldPrickle','csr_3_stageT_coldPrickle',
    #     ],
    #     'real_world_currency_per_point': 1.0,
    #     'ret_time': 120,
    #     'vcm_round_count': 10,
    #     'GE_min':5,
    #     'GE_max':10,
    #
    #     'participation_fee': 30.0,
    #     'final_score_discounter':0.4,
    # },
    {
        'name': 'csr_0_realeffort',
        'display_name': "CSR: RET",
        'num_demo_participants': 1,
        'app_sequence': [
            'csr_0_realeffort',
        ],
        'real_world_currency_per_point': 1.0,
        'ret_time': 120,
        'vcm_round_count': 10,
        'GE_min':5,
        'GE_max':95,

        'participation_fee': 30.0,
        'final_score_discounter':0.4,
        },
    {
        'name': 'csr_1_quiz',
        'display_name': "CSR: Quiz",
        'num_demo_participants': 2,
        'app_sequence': [
            'csr_1_quiz',
        ],
        'real_world_currency_per_point': 1.0,
        'ret_time': 120,
        'vcm_round_count': 10,
        'mpcr':0.5,
        'GE_min':5,
        'GE_max':95,

        'mpcr':0.5,
        'participation_fee': 30.0,
        'final_score_discounter':0.4,
        },
    {
        'name': 'csr_2_vcm',
        'display_name': "CSR: VCM",
        'num_demo_participants': 4,
        'app_sequence': [
            'csr_2_vcm',
        ],
        'real_world_currency_per_point': 1.0,
        'ret_time': 120,
        'vcm_round_count': 4,
        'GE_min':5,
        'GE_max':95,

        'participation_fee': 30.0,
        'final_score_discounter':0.4,
        },
    {
        'name': 'csr_vcm_stage',
        'display_name': "CSR: VCM + Stage - mpcr = .75",
        'num_demo_participants': 4,
        'app_sequence': [
            'csr_2_vcm','csr_3_stageT',
        ],
        'real_world_currency_per_point': 1.0,
        'vcm_round_count': 4,
        'stage_round_count': 4,
        'ret_time': 120,
        'GE_min':5,
        'GE_max':95,
        'participation_fee': 30.0,
        'final_score_discounter':1.0,
        'GE_Low_A':15,
        'GE_Low_F':5,
        'mpcr':0.75,
        'boycott_cost':10,
        'passive_ge_contrib':40,
        'A1_A_mult':1.0,
        'A1_F_mult':1.0,
        'F1_A_mult':1.0,
        'F1_F_mult':3.0, # ensure that (F1_F_mult * (GE_Low_F)) < 20, otherwise things break. 
        'A3_A_mult':1.0,
        'A3_F_mult':1.0,
        'N1_prob':0.75, # be sure to pick these to ensure easy numbers for quiz!

        },

    {
        'name': 'CSR_t1',
        'display_name': "CSR: T1: mpcr = .3; N1_prob = 0.75",
        'num_demo_participants': 4,
        'app_sequence': [
            'csr_0_realeffort', 'csr_1_quiz', 'csr_2_vcm','csr_3_stageT',
        ],
        'real_world_currency_per_point': 1.0,
        'vcm_round_count': 10,
        'stage_round_count': 10,
        'ret_time': 180,
        'GE_min':5,
        'GE_max':95,
        'participation_fee': 30.0,
        'final_score_discounter':1.0,
        'GE_Low_A':15,
        'GE_Low_F':5,
        'mpcr':0.3,
        'boycott_cost':10,
        'passive_ge_contrib':40,
        'A1_A_mult':1.0,
        'A1_F_mult':1.0,
        'F1_A_mult':1.0,
        'F1_F_mult':3.0, # ensure that (F1_F_mult * (GE_Low_F)) < 20, otherwise things break. 
        'A3_A_mult':1.0,
        'A3_F_mult':1.0,
        'N1_prob':0.75, # be sure to pick these to ensure easy numbers for quiz!

        },
    {
        'name': 'CSR_t2',
        'display_name': "CSR: T1: mpcr = .75; N1_prob = 0.75",
        'num_demo_participants': 4,
        'app_sequence': [
            'csr_0_realeffort', 'csr_1_quiz', 'csr_2_vcm','csr_3_stageT',
        ],
        'real_world_currency_per_point': 1.0,
        'vcm_round_count': 10,
        'stage_round_count': 10,
        'ret_time': 180,
        'GE_min':5,
        'GE_max':95,
        'participation_fee': 30.0,
        'final_score_discounter':1.0,
        'GE_Low_A':15,
        'GE_Low_F':5,
        'mpcr':0.75,
        'boycott_cost':10,
        'passive_ge_contrib':40,
        'A1_A_mult':1.0,
        'A1_F_mult':1.0,
        'F1_A_mult':1.0,
        'F1_F_mult':3.0, # ensure that (F1_F_mult * (GE_Low_F)) < 20, otherwise things break. 
        'A3_A_mult':1.0,
        'A3_F_mult':1.0,
        'N1_prob':0.75, # be sure to pick these to ensure easy numbers for quiz!

        },

]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
