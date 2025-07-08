# Prometheus Committee App – Signup and Admin Dashboard

This is a live Flask-based web application built for Prometheus Round 2 selections. It allows users to register via a signup form and enables admins to view all signups through a secure dashboard.

## Live URLs

- **Signup Page**: [https://prometheus-webpage.onrender.com/signup](https://prometheus-webpage.onrender.com/signup)  
  Fill in your name, email, and password to register. The information is stored in a live PostgreSQL database hosted on Render.

- **Admin Login**: [https://prometheus-webpage.onrender.com/admin-login](https://prometheus-webpage.onrender.com/admin-login)  
  Use the admin panel to view the list of all registered users.  

  **Admin Password**: `admin123`  
  (Only a single password field is required.)

---

## Features

### User Signup
- Responsive UI using Bootstrap.
- Captures name, email, and password.
- Redirects to a user profile page after successful signup.

### Admin Dashboard
- Displays a table of all registered users.
- Shows live data fetched directly from the PostgreSQL database.
- No server restart or refresh delay required.

---

## Real-Time Database Integration

- Backend uses Flask-SQLAlchemy.
- Data is stored in a hosted PostgreSQL database on Render.
- The admin dashboard fetches the latest data from the database each time it is accessed.
