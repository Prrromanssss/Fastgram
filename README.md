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
python instagram/manage.py makemigrations
```
5.2 To apply your migrations run this command
```commandline
python instagram/manage.py migrate
```
