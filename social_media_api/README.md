# Social Media API — Bookly Capstone Project

A RESTful social media API built with **Django** and **Django REST Framework**.  
This backend supports user registration, authentication, creating posts, commenting, and tagging functionality.

---

## 🚀 Features

### **Accounts**
- User registration
- User login and authentication
- Token-based authentication
- Secure password hashing

### **Posts**
- Create, update, delete posts
- View all posts or retrieve a single post
- Filter posts by tags

### **Comments**
- Add comments to posts
- View comments for specific posts

### **Tags**
- Integrated via `django-taggit`
- Add tags while creating or updating posts

---

## 📦 Installation & Setup

### **1. Clone the repository**
```bash
git clone <your_repo_url>
cd social_media_api


## Follow & Feed

### Follow a User
**POST** `/api/accounts/follow/<user_id>/`  
Requires authentication.

### Unfollow a User
**POST** `/api/accounts/unfollow/<user_id>/`  
Requires authentication.

### Get your Feed
**GET** `/api/feed/`  
Returns posts from users you follow, newest first. Requires authentication.


## Likes & Notifications

### Like a post
POST /api/posts/<post_id>/like/
Auth required.

### Unlike a post
POST /api/posts/<post_id>/unlike/

### Get notifications
GET /api/notifications/
Auth required. Returns user's notifications ordered newest first; unread appear first.

### Mark notification read
POST /api/notifications/<id>/mark-read/
Auth required. Marks a single notification as read.

Notifications are generated:
- when someone likes your post
- when someone comments on your post
- when someone follows you (created in accounts.follow_user)

# Deployment Documentation

## Hosting Platform
Render (https://render.com)

## Deployment Steps
1. Configure environment variables
2. Install dependencies
3. Run migrations
4. Collect static files
5. Start Gunicorn server

## Production Settings
- DEBUG=False
- SSL enforced
- Secure cookies enabled

## Live URL
https://your-app-name.onrender.com

## Maintenance
- Regular dependency updates
- Log monitoring via Render dashboard
