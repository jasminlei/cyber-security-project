# Cyber Security Project - Secondhand Marketplace

A web application demonstrating common security vulnerabilities from the OWASP Top 10 list. This project is built with Django (backend) and Vue.js (frontend).

More information about the OWASP Top 10 vulnerabilities: [OWASP Top 10 (2025)](https://owasp.org/Top10/2025/)

## Installation and setup

### Prerequisites

The following software must be installed on your system:

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** and npm - [Download Node.js](https://nodejs.org/)

### Installation steps

#### 1. Clone the repository

```bash
git clone https://github.com/jasminlei/cyber-security-project.git
cd cyber-security-project
```

#### 2. Backend setup (Django)

Navigate to the server directory:

```bash
cd server
```

**Install Python dependencies:**

```bash
pip install -r requirements.txt
```

> If you encounter issues with `pip`, try using `python -m pip install -r requirements.txt`

**Run database migrations:**

```bash
python manage.py migrate
```

- **Windows:** Use `python` instead of `python3`
- **macOS/Linux:** Use `python3` if you have both Python 2 and 3 installed

**Start the Django development server:**

```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

#### 3. Frontend setup (Vue.js)

Open a new terminal window and navigate to the client directory:

```bash
cd client
```

**Install Node.js dependencies:**

```bash
npm install
```

**Start the Vue development server:**

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Creating a user account

1. Open `http://localhost:5173` in your browser
2. Click "Login" in the navigation bar
3. Change to "Register"
4. Fill in the registration form:
   - Username
   - Email
   - Password
   - Confirm Password
5. Click "Register"
6. You will be automatically logged in

## Using the application

### Browse items

- Click "Browse" to view all marketplace items
- Use the search box to filter items
- Click on any item to view details

### Create a new item

- Click "Add Item" (requires login)
- Fill in the form:
  - Title
  - Description
  - Price
  - Contact information
  - Image URL (optional)
- Click "Create Item"

### Manage your items

- Click "My Items" to see items you've created
- View, edit, or delete your own items

### Like items

- Click the heart icon on any item
