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

## USER APP API

- **Registration** = /api/1/user/register/
- **Login** = /api/1/oauth/ For login
- **UpdateUser** = /api/1/user/edit/me/
- **All User List** = /api/1/user/list/ (Only Admin can see it)
- **ViewUser Details** api/1/user/<slug_username>/
- **User Blog list** api/1/user/blog/<slug_username>/
- **User follow list** api/1/user/<slug_username>/follow/
- **User get follower** api/1/user/<slug_username>/get-followers/
- **User get following** api/1/user/<slug_username>/get-following/

- **Foget password email** api/1/user/api/sendForgottenPasswordEmail/
- **RESET PASSWORD** api/1/user/api/changeForgottenPassword/
- **UPDATE PASSWORD** api/1/user/change/password/

## BLOG APP API

- **Blog send email preview** = /api/1/blog/email/preview/<int:pk>/
- **Blog send email test** = /api/1/blog/email/test/<int:pk>/

- **Creat blog** = /api/1/blog/create/
- **See blog details** = /api/1/blog/create/<int:pk>/
- **See blog list** = /api/1/blog/
- **See blog liker** = /api/1/blog/<int:pk>/get-likers/
- **Like blog** = /api/1/blog/like/<int:pk>/
- **Add favourite blog** = /api/1/blog/favorite/<int:pk>/

## INSTAGRAM POST APP API

- **See all feed** = /api/1/post/feed/
- **Comment on post** = /api/1/post/comment/<uuid:post_id>/
- **Manage Comment on post** = /api/1/post/comment/<int:comment_id>/
- **See like bview on post** = /api/1/post/like/<uuid:post_id>/
- **See comment like bview on post** = /api/1/post/comment/like/<int:comment_id>/
- **get post likers** = /api/1/post/<uuid:post_id>/get-likers/
