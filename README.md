# TSG Inventory and Computer Laboratory Monitoring System

A comprehensive system for managing inventory and monitoring computer laboratory resources.

## Features

- Inventory Management
- Computer Laboratory Monitoring
- User Authentication
- Asset Tracking
- Maintenance Scheduling
- Reports Generation

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `inventory/` - Main application for inventory management
- `tsg_ims/` - Project configuration
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files

## Technologies Used

- Python 3.11+
- Django 5.2+
- SQLite3
- Bootstrap 5
- HTML5/CSS3
- JavaScript #   I M S  
 #   T S G _ I n v e n t o r y - M a n a g e m e n t - S y s t e m  
 