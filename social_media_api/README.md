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

Example:
