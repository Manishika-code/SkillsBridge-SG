# SkillsBridge SG
## Setup guide
1. prerequisites
- Python 3.11+
- pip and venv (come with Python)

2. create & activate virtualenv
```
# mac/linux
python -m venv .venv
source .venv/bin/activate

# windows (powershell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

4. run the dev server
```
python manage.py runserver
```

5. check server is running
visit http://127.0.0.1:8000/admin and http://127.0.0.1:8000/api/
