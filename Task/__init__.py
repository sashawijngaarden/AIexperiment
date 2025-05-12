from otree.api import *
import numpy.random as rnd  
import random 
import pandas as pd 

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Task'
    PLAYERS_PER_GROUP = None
    NUM_RROUNDS = 3 # Real Rounds
    NUM_PROUNDS = 3 # Practice Rounds
    NUM_ROUNDS = NUM_PROUNDS + NUM_RROUNDS
    # List of attributes (id)
    ATTR_ID     = ['P','Q','S','N']
    ATTR_NAMES  = ['Price','Quality','Sustainability','Advice']
    # Template vars
    COL_NAMES   = ['A','B']
    # Paths 
    PATH_TRIALS = '_static/global/files/myTrials.csv'
    IMG_PRICE      = "global/figures/P/"
    IMG_S            = "global/figures/S/S"
    IMG_Q            = "global/figures/Q/Q"

    # In between round messages
    BetweenTrialMessages = {
        "1": f"Now you will have {NUM_PROUNDS} practice rounds.", 
        str(int(NUM_PROUNDS+1)): "The practice rounds are over."
        }
    # Confidence page
    iLikertConf     = 7
    sConfQuestion   = f"From 1 to {iLikertConf}, how confident are you on your choice?"
    sLeftConf       = "Very unsure"
    sRightConf      = "Very sure"




class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # DVs
    sChoice     = models.StringField()
    dRT_dec     = models.FloatField()
    iConfidence = models.IntegerField()
    dRT_conf    = models.FloatField()
    dTime2first = models.FloatField()
    # Attention variables
    sNames      = models.LongStringField()
    sDT         = models.LongStringField()

    # # Timestamps
    sStartDec   = models.StringField()
    sEndDec     = models.StringField()
    sStartCross = models.StringField()
    sEndCross   = models.StringField()
    sStartConf = models.StringField()
    sEndConf   = models.StringField()


    # Others 
    sBetweenBtn = models.StringField()
    sustRight = models.BooleanField() # true if sustainable product on the right


    # Trial Attributes
    originalTrial = models.IntegerField()
    P1 = models.FloatField()
    P2 = models.FloatField()
    Q1 = models.IntegerField()
    Q2 = models.IntegerField()
    S1 = models.IntegerField()
    S2 = models.IntegerField()
    Advice = models.StringField()

def creating_session(subsession):
    # Load Session variables
    s = subsession.session 
    if subsession.round_number==1:
        for player in subsession.get_players():
            p = player.participant
            # randomly assign condition to participant
            p.condition = random.choice(['VN', 'VHL', 'SN', 'SHL']) 
            #### Randomize trials of main task
            dbTrials = pd.read_csv(C.PATH_TRIALS, sep=';')
            dbPractice  = dbTrials.iloc[:C.NUM_PROUNDS]  # Keep the first NUM_PROUNDS rows unchanged
            dbReal      = dbTrials.iloc[C.NUM_PROUNDS:].sample(frac=1).reset_index(drop=True)
            dbTrials = pd.concat([dbPractice, dbReal], ignore_index=True)
            ### Randomize side of products
            dbTrials['sustRight'] = rnd.choice([True, False], size=len(dbTrials))
            p.dbTrials = dbTrials
            # print(dbTrials)
            
            #### Order of attributes
            lPos = [None, None, None, None]
            # Random N position (first or last)
            if random.choice([True, False]):
                lPos[0] = 'N'
                n_positions = [1, 2, 3]
            else:
                lPos[3] = 'N'
                n_positions = [0, 1, 2]
            # Random P position (second or third)
            if random.choice([True, False]):
                p_index = 1 # second position
            else:
                p_index = 2 # third position
            lPos[p_index] = 'P'
            # Randomly assign Q and S to remaining spots
            remaining_indices = [i for i in n_positions if lPos[i] is None]
            q_s = ['Q', 'S']
            random.shuffle(q_s)
            for idx, val in zip(remaining_indices, q_s):
                lPos[idx] = val
            p.lPos = lPos # store final order as participant variable

            #### Select trial for payment (from the first round after practice rounds to the last)
            p.iSelectedTrial = random.randint(C.NUM_PROUNDS+1,C.NUM_ROUNDS)

    for player in subsession.get_players():
        p = player.participant
        player.sBetweenBtn = random.choice(['left','right'])
        row = int(player.round_number-1)
        db = p.dbTrials
        trialValues = db.iloc[row].astype(object).to_dict()
        print(trialValues)
        player.originalTrial    = trialValues['Trial']
        player.P1               = trialValues['P1']
        player.P2               = trialValues['P2']
        player.Q1               = trialValues['Q1']
        player.Q2               = trialValues['Q2']
        player.S1               = trialValues['S1']
        player.S2               = trialValues['S2']
        col_name                = f'Advice-{p.condition}'
        player.Advice            = trialValues[col_name]
        player.sustRight        = trialValues['sustRight']
        ## function that retrieves data from csv to player variables. 

def numToFloat(value):
    formatted = f"{value:.1f}"  # Ensures one decimal
    return f"{formatted.replace('.', '_')}"

def attributeList(player):
    lPos = player.participant.lPos

    lAttributes = []
    lOrder      = []
    for i in range(len(C.ATTR_ID)):
        id                  = C.ATTR_ID[i]      
        name                = C.ATTR_NAMES[i]  
        # Store the order of the list
        lOrder.append(lPos.index(id))

        lPaths = []
        values = []
        path = []
        match id:
            case 'P': 
                values  = [numToFloat(player.P1),numToFloat(player.P2)]
                path    = C.IMG_PRICE
            case 'Q':
                values  = [player.Q1, player.Q2]
                path    = C.IMG_Q
            case 'S':
                values  = [player.S1,player.S2]
                path    = C.IMG_S
            case 'N':
                values  = [player.Advice]
                path    = None
        if player.sustRight:
            print(f'reverse {values}{values[::-1]}')
            values = values[::-1]
        if id == 'N':
            # For advice, just keep text as it is
            lPaths = values
        else:
            for v in values:
                lPaths.append(f"{path}{v}.png")
       
        # Create object with all the relevant variables
        Attr = {
            'id'        : id,
            'name'      : name,
            'lValues'    : lPaths,
        }
        lAttributes.append(Attr)
    
    lFinal = [ lAttributes[x] for x in lOrder]
    return lFinal

# PAGES

class Decision(Page):
    form_model      = 'player'
    # form_fields     = [ 'sChoice']
    form_fields     = [ 'sStartDec','sEndDec', 'dRT_dec', 'sNames', 'sDT' , 'dTime2first', 'sChoice']
    
    @staticmethod
    def vars_for_template(player: Player):
        # Order of attributes (from participant var)
        p = player.participant
        lPos = p.lPos     
        # Candidates values          
        # lValues = [rnd.randint(0,6,len(C.COL_NAMES)) for _ in range(len(C.ATTR_ID))]
        return dict(
            lAttr = attributeList(player),
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        p = player.participant
        
        if player.round_number == p.iSelectedTrial: 
            p.sChoice = player.sChoice   
            print(f"Decision in selected trial recorded: {p.sChoice}")

class PracticeDone(Page):
    template_name = '_templates/global/PracticeDone.html'

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_PROUNDS

class FixCross(Page):
    form_model = 'player'
    form_fields = [ 'sStartCross','sEndCross' ]
    template_name = 'global/FixCross.html'


class SideButton(Page):
    form_model = 'player'
    form_fields = [ 'sStartCross','sEndCross' ]
    template_name = 'global/SideButton.html'

    @staticmethod
    def js_vars(player: Player):
        
        return dict(
            sPosition = player.sBetweenBtn
        )


class Confidence(Page):
    form_model      = 'player'
    form_fields     = [ 'sStartConf','sEndConf', 'dRT_conf','iConfidence']
    template_name   = 'global/Confidence.html'
    
    # Skip confidence at last practice trial to show message
    @staticmethod
    def is_displayed(player):
        return player.round_number != C.NUM_PROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        p = player.participant
        return dict(
            lScale = list(range(1,C.iLikertConf+1))
        )



page_sequence = [SideButton, Decision, Confidence, PracticeDone]