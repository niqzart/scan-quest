from app.models.goals_db import Goal
from app.models.participants_db import Participant
from app.models.quests_db import Quest
from tests.common.polyfactory_ext import BaseModelFactory


class QuestInputFactory(BaseModelFactory[Quest.InputSchema]):
    __model__ = Quest.InputSchema


class GoalInputFactory(BaseModelFactory[Goal.InputSchema]):
    __model__ = Goal.InputSchema


class ParticipantInputFactory(BaseModelFactory[Participant.InputSchema]):
    __model__ = Participant.InputSchema
