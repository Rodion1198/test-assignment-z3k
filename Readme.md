## Local Setup

### Pre-requirements

1. docker
2. docker-compose
3. make (CLI)

---

### Setup

1. (only once) Create .env file with environment variables from the template.
   Edit the created `.env` file with your parameters:

```bash
cp .env.example .env
# edit .env file as you need
```

2.  Launch the project

```bash
make run-build
```

3. (only once or by request) Apply migrations

```bash
make mm
```

4. (only once) Setup Static Files

```bash
make bash
python manage.py collectstatic --noinput
exit
```

5. (only once or by request) Create a superuser for the Admin panel. Specify your own credentials

```bash
make bash
python manage.py create_default_superuser --username admin --password admin123 --email admin@admin.com
exit
```

## API

The API is available at `http://localhost:8000/swagger`.

You can use Postman [collection](https://www.postman.com/joint-operations-administrator-42085091/workspace/zone3k/collection/21366085-2808c7e7-7936-409a-ace8-cf4b87a63b9b?action=share&creator=21366085
) to interact with API.
