# YaCut

**YaCut** is a URL shortening service.
Additional feature: uploading files to Yandex.Disk with the generation of short links for downloading them.

## TECH STACK

![Python](https://img.shields.io/badge/python-black?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=blue)
![aiohttp](https://img.shields.io/badge/aiohttp-black?style=for-the-badge&logo=aiohttp&logoColor=blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-black?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00)
![SQLite](https://img.shields.io/badge/SQLite-black?style=for-the-badge&logo=sqlite&logoColor=blue)

![bootstrap](https://img.shields.io/badge/bootstrap-black.svg?style=for-the-badge&logo=bootstrap&logoColor=9370DB)
![HTML5](https://img.shields.io/badge/html5-black.svg?style=for-the-badge&logo=html5&logoColor=D2691E)
![CSS](https://img.shields.io/badge/CSS-black?style=for-the-badge&logo=css&logoColor=9370DB)

![Swagger](https://img.shields.io/badge/Swagger-black?style=for-the-badge&logo=swagger&logoColor=85EA2D)
![pytest](https://img.shields.io/badge/pytest-black.svg?style=for-the-badge&logo=pytest&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-black?style=for-the-badge&logo=postman&logoColor=FF6C37)
![Git](https://img.shields.io/badge/git-black.svg?style=for-the-badge&logo=git&logoColor=orange)

## How to Run the Project

###

#### Clone the repository and navigate into it

```bash
git clone https://github.com/briliov/async-yacut.git
```

```bash
cd async-yacut
```

#### Create and activate a virtual environment

```bash
python3 -m venv venv
```

##### Linux | Mac

```bash
source venv/bin/activate
```

#### Windows

```bash
source venv/scripts/activate
```

#### Install dependencies from requirements.txt

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

#### Create a `.env` file in the project directory with the following environment variables

```text
# Flask
FLASK_APP=yacut
FLASK_DEBUG=1
SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///db.sqlite3

# Yandex.Disk API credentials
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
REDIRECT_URI=https://oauth.yandex.ru/verification_code
YANDEX_DISK_AUTH_TOKEN=your_yandex_disk_token_here
```

#### Create the database and apply migrations

```bash
flask db upgrade
```

#### Run the project

```bash
flask run
```

## How to Run Tests

### 

#### To run the tests, execute the following command

```bash
pytest
```

## API Testing

To test the API endpoints, use the Postman collection located in the `postman_collection/` directory.

* **`POST /api/id/`** — create a new short link.
* **`GET /api/id/<short_id>/`** — retrieve the original link by its short ID.

Import the `.json` file from the `postman_collection` folder into Postman and execute the requests.

---

### Author  [Egor Briliov](https://github.com/briliov)
