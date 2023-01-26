# Tibber Developer Test: Microservice implementation

The repository stores Can H. Tartanoglu's implementation of the Tibber developer test handed out in 2022.

```shell
docker-compose up -d
```
The API URL is `localhost:5000`, making the test endpoint path `localhost:5000/tibber-developer-test/enter-path`. You can also access the OpenAPI docs on `localhost:5000/docs`.

In addition to running through docker-compose with PostgreSQL, the API can also be run in the host machine inside Python:
```python
from tibber import api

api.run_app()
```
This implementation uses `sqlite` instead of PostgreSQL.

## Decisions made in chronological order

### API development
- The examiner has allowed me to use any language of my choosing. I picked Python 3.10.8; latest stable release on `pyenv` on Arch Linux.
- `poetry` as my package manager, making sure upstream dependencies have version locking and developer environment automation.
- `fastapi` as the API framework.
- `toroise-orm`, which uses object relation mapping or ORM, to implement database models. These are migrated using `asyncpg` to PostgreSQL. I use `sqlite` for testing.
- `pytest` for testing, read more in `TESTING.md` can be found in `<repo>/test` directory.

### Containerization
- Packaging API package into a wheel file, `.whl`, for its installation inside its designated container. You can rebuild the `.whl` file with poetry: `poetry build`. Note that I only tested this with Python 3.10, I expect the syntax to be incompatible with <3.10. 
- Using docker-compose healthcheck functionality to signal [postgresql readiness](https://github.com/peter-evans/docker-compose-healthcheck).

### Making the connection configurable
From the assignment: "Ensure that database connection is configurable using environment variable."

I understand that this makes sense for this examination; moreover, I would like to point out what I would design differently when building the app for web deployment.

The current implementation is a security risk as I will have to expose the password on a `.yaml` file. To hide the password, I would use docker secrets or HashiCorp Vault secret in combination with a URL interpolator on the API side. This separates the password, which is a secret, from the other variables (username, host, port, dbname) that aren't secrets.

Docker secrets does hide the value from public; however, it requires manual intervention during definition and rotation. HashiCorp Vault implements an automated rotation in its [static secrets](https://developer.hashicorp.com/vault/tutorials/secrets-management/static-secrets#generate-a-token-for-apps) feature.
