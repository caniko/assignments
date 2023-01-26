from logging import getLogger
from uuid import UUID

from tortoise import models
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields import DatetimeField, FloatField, IntField, UUIDField

from tibber import TORTOISE_CONFIG

logger = getLogger(__name__)


class RobotWork(models.Model):
    id: UUID = UUIDField(pk=True)

    timestamp = DatetimeField(auto_now_add=True)
    commands: int = IntField(null=False)
    result: int = IntField(null=False)
    duration: float = FloatField(null=False)


RobotWork_Pydantic = pydantic_model_creator(RobotWork, name="RobotWork")


async def first_migration():
    from json import dumps

    from aerich import Command

    logger.info(f"Migrating with config: {dumps(TORTOISE_CONFIG, indent=2)}")

    command = Command(tortoise_config=TORTOISE_CONFIG, app="models")
    await command.init()
    await command.init_db(safe=False)

    logger.info("Migration complete")
