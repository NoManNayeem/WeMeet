
# Video Meeting & Chatting Platform Backend

## Project Objective
This project aims to create a minimal backend for a video meeting and chatting platform, similar to Google Meet. The backend is built using Django Rest Framework (DRF) and includes basic features like user management, meeting creation, chatting, and video/screen sharing.

## Features
- **Accounts App**: User registration, login, and profile management.
- **Meeting App**: Users can create meetings, share meeting URLs, and join meetings as either hosts or guests.
- **Chat App**: Real-time chat functionality within the meeting.
- **Meeting Features**: Users can chat, share their camera feed, and share their screen during the meeting.

## Project Structure
```bash
├── accounts
│   ├── migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
├── meeting
│   ├── migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
├── chat
│   ├── migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
├── project_name
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── manage.py
├── requirements.txt
```

## How to Install/Run the Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/project_name.git
   cd project_name
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the API**:
   - The API will be available at `http://127.0.0.1:8000/`.
   - You can use tools like Postman or Curl to interact with the API.


8. ** If using `daphne` **:
```bash
pip install daphne
daphne -p 8000 project_name.asgi:application
```
## Notes
- This project is intended to be minimal. Future expansions might include more advanced features, scalability improvements, and frontend integration with NextJS.
- Ensure you are using the latest versions of Django, DRF, and other dependencies as of 2024 to maintain compatibility and security.

## Documentation
- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Django Rest Framework Documentation](https://www.django-rest-framework.org/)

