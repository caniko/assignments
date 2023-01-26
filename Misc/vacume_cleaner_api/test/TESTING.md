# Test suite for Tibber Developer Test
The following stores the unit and integration test(s) for `tibber`, the package I developed for the Tibber Developer Test. I place every test in their Python file counterpart under the parent directory, `test`.

## Running the tests
I used poetry to manage the package, it installs `pytest` when installed through poetry. You need to install `pytest` along with the other dependencies. To run the tests, in the root repository directory:

```shell
pytest .
```

Should you not want to use `poetry`, and just `pip`, you can install all the testing dependencies (don't forget to make a virtual python environment):

```shell
pip install fastapi tortoise-orm[psycopg] pytest httpx asgi-lifespan
```

## For the next developer
I use [`pytest.raises`](https://docs.pytest.org/en/latest/reference/reference.html#pytest.raises) to test for instances that should raise an exception. The reason for the exception can be found as a comment above the respective line of code.
