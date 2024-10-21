from app.models.quests_db import Quest
from tests.common.polyfactory_ext import BaseModelFactory


class QuestInputFactory(BaseModelFactory[Quest.InputSchema]):
    __model__ = Quest.InputSchema
