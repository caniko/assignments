import asyncio

from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config
from tortoise.contrib.fastapi import register_tortoise

from tibber import MODEL_PATH, POSTGRES_URL, TEST_ENDPOINT_PATH, TORTOISE_CONFIG
from tibber.models import RobotWork, RobotWork_Pydantic
from tibber.schema import RobotMove

app = FastAPI(title="Tibber Developer Test 2022")


@app.post(
    TEST_ENDPOINT_PATH,
    response_model=RobotWork_Pydantic,
    name="Tibber developer test",
    summary="Register robot cleaning job",
    description="The endpoint ",
)
async def tibber_dev_test(robot_move: RobotMove):
    robot_move_obj = await RobotWork.create(**robot_move.info())
    return await RobotWork_Pydantic.from_tortoise_orm(robot_move_obj)


if POSTGRES_URL:
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
    )
else:
    register_tortoise(
        app,
        db_url="sqlite://:memory:",
        modules={"models": [MODEL_PATH]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


def run_app():
    asyncio.run(serve(app, Config()))


if __name__ == "__main__":
    run_app()
