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



## Current endpoints setup
| Method | Endpoint                        | Description                                                          |
| ------ | ------------------------------- | -------------------------------------------------------------------- |
| `GET`  | `/api/courses/`                 | List all courses (filterable by `level`, `provider`, `skills_name`) |
| `GET`  | `/api/courses/{id}/`            | Retrieve a specific course                                           |
| `GET`  | `/api/skills/`                  | List all skills                                                      |
| `GET`  | `/api/skills/{id}/`             | Retrieve a specific skill                                            |
| `GET`  | `/api/industries/`              | List all industries                                                  |
| `GET`  | `/api/industries/{id}/`         | Retrieve a specific industry                                         |
| `GET`  | `/api/industries/{id}/context/` | Get industry metrics 
| `GET`    | `/api/plans/`      | List current user’s saved plans (needs JWT)                       |
| `POST`   | `/api/plans/`      | Create new plan (needs JWT). Body: `{ "name": "My Career Plan" }` |
| `GET`    | `/api/plans/{id}/` | Get details of a specific plan                                    |
| `PATCH`  | `/api/plans/{id}/` | Update a plan                                                     |
| `DELETE` | `/api/plans/{id}/` | Delete a plan                                                     ||
| `GET`  | `/api/evidence/?entity=course&id={course_id}`     | how evidence panel for a course                           |
| `GET`  | `/api/evidence/?entity=industry&id={industry_id}` | Show evidence panel for an industry                        |
| `POST` | `/api/compare/`                                   | Compare up to 2 courses. Body: `{ "courseIds": ["id1","id2"] }` |
| `POST` | `/api/auth/register/` | Register a new user (`username`, `email`, `password`, optional `role`)     |
| `POST` | `/api/token/`         | Login → returns `{access, refresh}` JWT tokens                             |
| `POST` | `/api/token/refresh/` | Refresh an expired access token using refresh token                        |
| `GET`  | `/api/auth/me/`       | Get current logged-in user profile (needs `Authorization: Bearer <token>`) |
