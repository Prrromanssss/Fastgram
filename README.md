# Fastgram

![flake8 tests](https://github.com/Prrromanssss/Fastgram/actions/workflows/flake8-linter.yml/badge.svg)



## Deployment instructions


### 1. Cloning project from GitHub

1.1 Run this command
```commandline
git clone https://github.com/Prrromanssss/Fastgram.git
```

### 2. Creation and activation venv

2.1 First of all, from root directory run this commands to activate venv
#### Mac OS / Linux
```commandline
python3 -m venv venv
source venv/bin/activate
```
#### Windows
```commandline
python -m venv venv
.\venv\Scripts\activate
```

### 3. Installation all requirements

3.3 Run this command 
```commandline
pip install -r requirements.txt
```

### 4. Generate file with virtual environment variables (.env)

4.1 Generate file '.env' in root directory with structure specified in the 'examples/env_example.txt' file

### 5. Making migrations

5.1 To make migrations run this command

```commandline
python fastgram/manage.py makemigrations
```
5.2 To apply your migrations run this command
```commandline
python fastgram/manage.py migrate
```

### 6. Database setup

6.1.1 To load data for database from the fixtures run this command
```commandline
python fastgram/manage.py loaddata data.json
```

### 7. Authorizing admin user

7.1.1 If you have loaded data from the fixtures, run this command to authorize admin user
```commandline
python fastgram/manage.py createsuperuser
```

### 8. Running project

8.1 Run this command
```commandline
python fastgram/manage.py runserver
```
8.2 After running server follow link
'127.0.0.1:8000/admin' or 'localhost:8000/admin'


***

## ER-diagram
![Image of the ER-diagram](https://github.com/Prrromanssss/Fastgram/raw/main/media-for-README/ER-diagram.png)
***
