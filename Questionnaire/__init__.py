from otree.api import *
import json 
import time

doc = """
This app administers a post-task questionnaire to collect demographics, attitudes  toward AI, motivation,
and perceptions of the AI recommender system. It also calculates and displays the participant's bonus payout 
and environmental reward based on their choice on one randomly chosen trial.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # File location
    sQuestPath = '_static/global/files/questions.json'
    # Message
    sEndMessage = 'The main task of the experiment has ended. Now we will ask you to answer a brief questionnaire. After the questionnaire we will inform you if you have been selected for the bonus payment.'
    # Questions 
    text_file = open(sQuestPath)
    lQuestions = json.load(text_file)['lQuestions']
    lNames      = []
    lNamesQ    = []
    lVars       = []
    for i in range(len(lQuestions)):
        name  = f"Q_{lQuestions[i]['name']}"
        bIsQ  = lQuestions[i]['name'] !=''
        if lQuestions[i].get('blank'):
            bBlank = True
        else:
            bBlank = False
        lNames.append(name)
        if bIsQ:
            lNamesQ.append(name)
            lVars.append([name,bBlank])
        


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    iCorrect = models.IntegerField()
    tree_country = models.StringField(blank=True)

for i in range(len(C.lVars)):
    name, bBlank = C.lVars[i]
    setattr(Player, name, models.StringField(blank=bBlank))



# PAGES
class Questionnaire(Page):
    template_name = 'global/Questionnaire.html'

    form_model = 'player'
    lFields = C.lNamesQ[:]
    # lFields.append('iCorrect')
    form_fields = lFields


    @staticmethod
    def js_vars(player: Player):
        
        return dict(
            lQuestions = C.lQuestions,
            sBodyName = 'page-content',
        )

        
class AfterTask(Page):
    template_name = 'global/AfterTask.html'

class EndMessage(Page):
    template_name = 'global/EndMessage.html'

    @staticmethod
    def vars_for_template(player: Player):
        p = player.participant
        return dict(
            bonus=round(player.participant.vars.get('bonus_amount', 0), 2),
            trees=int(player.participant.vars.get('trees_planted', 0)),
            MessageText = C.sEndMessage,
            country=player.participant.vars.get('tree_country', "a selected location")
        )
    
page_sequence = [AfterTask,Questionnaire,EndMessage]
