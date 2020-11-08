# instagram-rest-api

RESTFUL API of instagram clone also Blog Api.

## [Demo Link](https://inback.herokuapp.com/)

## Specification:

- Registering and logging to user account
- Write a blog (follow author and see all author blog)
- posting photos (follow user , send message, see followed user post)
- commenting and liking photos
- following system
- Forger password , Change password
- Emailing system
- Storing user activity
- Resume Genrate function
- Store user password history in encrpted form(user will be not alllow to change or reset old password)
- all CRUD operations on posts, comments, follows and likes with relevant permissions

## Technology :

- Python
- Django and Django Rest Framework
- Oauth2

## Blog Feature:

- **Registration** = Once you will register you will get an email to confirm your registration https://inback.herokuapp.com/api/1/user/register/
- **Login** = Once you will confirm your registration https://inback.herokuapp.com/api/1/oauth/token/
- **Welcome Email** - After confirmation of your registration you will get an Welcome email from server to know about blog feature
- **Forget Password** = You Will need to type your email then you will get an email to reset your password.https://inback.herokuapp.com/users/password-reset/
- **Update Password** = https://inback.herokuapp.com/api/1/user/change/password/
- **Add Blog** = You can create new blog after successful create blog you will get an email about your blog. https://inback.herokuapp.com/api/1/blog/create/
- **View Blog by Tag_Name**
- **Schedule Blog**
- **Track Email That you seen**
- **View Blog**
- **View Author Profile with his blog list**
- **Like blog only if you will be logged in**
- **View Likers**
- **Follow Author**
- **View Followers**
- **View Followings**
- **Edit Blog**

- **Edit Profile**

## Some Default urls:

- **Registration** = localhost:8000/api/1/user/register/
- **Login** = localhost:8000/api/1/oauth/ For login
- **UpdateUser** = localhost:8000/api/user/updateDelete/
- **ViewUser** localhost:8000/api/user/<slug_username>/
- **BLOG api OR POST** localhost:8000/api/post/
- localhost:8000/api/post/feed/
