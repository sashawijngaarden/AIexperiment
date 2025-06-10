from otree.api import *
import random
import pandas as pd
from collections import Counter
from numpy import random as rnd
import numpy as np
doc = """
This app provides participants with instructions on how to complete the experiment.
It includes an overview of the task, a step-by-step explanation, and comprehensive questions
to ensure understanding before starting the practice trials.
"""


class C(BaseConstants):
    NAME_IN_URL         = 'Intro'
    PLAYERS_PER_GROUP   = None
    NUM_ROUNDS          = 1
    # Setup/Experiment variables 
    iPracticeRounds     = 3
    iOptions            = 21
    # iNumTrials          = 5
    iNumTrials          = iPracticeRounds + 3*iOptions
    # Template variables
    AvgDur              = '30'
    iBonus              = '2 pounds'
    # Figs/Files paths
    figUvA_logo         = 'global/figures/UvA_logo.png'
    path1HL             = 'global/figures/Instructions/examp1HL.png'
    path1NL             = 'global/figures/Instructions/examp1NL.png'
    path2HL             = 'global/figures/Instructions/HL.png'
    path2NL             = 'global/figures/Instructions/SA.png'
    path3               = 'global/figures/Instructions/confidence.png'
    pathGifHL           = 'global/figures/Instructions/Hover_HL.gif'
    pathGifNL           = 'global/figures/Instructions/Hover_NL.gif'
    pathData            = '_static/global/files/Data4Exp.csv'
    imgCandidate        = "global/figures/candidate.png"
    imgNumbers          = "global/figures/numbers/n_"

    # Links 
    # You might want to have different links, for when they submit differen answers
    sLinkReturn         = "https://app.prolific.com/submissions/complete?cc=XXXXX"
    sLinkReturnCal      = "https://app.prolific.com/submissions/complete?cc=YYYYY"
    sLinkOtherBrowser   = "https://YOUR-EXPERIMENT.herokuapp.com/room/room1"
    SubmitLink          = 'https://app.prolific.com/submissions/complete?cc=ZZZZZ'



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    tree_country = models.StringField(blank=True)


# FUNCTIONS
    
def creating_session(subsession):
    # Load Session variables
    if subsession.round_number ==1:
        for player in subsession.get_players():
            p = player.participant
            p.condition = random.choice(['VN', 'VHL', 'SN', 'SHL'])
            



# PAGES


class Instructions(Page):
    form_model = 'player'
    form_fields = ['tree_country']

    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['tree_country'] = player.tree_country

    @staticmethod
    def js_vars(player: Player):
        ## Variables necessary for javascript
        p = player.participant
        return dict(
            lSolutions = [
                'b','c', 'yes' # Solutions to control questions
            ],
        )

    @staticmethod
    def vars_for_template(player: Player):
        p = player.participant
        condition = p.condition
        return dict(
            path1=C.path1HL if condition in ['VHL', 'SHL'] else C.path1NL,
            path2=C.path2HL if condition in ['VHL', 'SHL'] else C.path2NL,
            pathGif=C.pathGifHL if condition in ['VHL', 'SHL'] else C.pathGifNL,
            path5=C.path3
        )

page_sequence = [Instructions]

