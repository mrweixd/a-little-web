# a-little-web
  This is a project that aims to practice making websites.
# Architecture
<img width="700" alt="image" src="https://github.com/user-attachments/assets/ecd44555-d7e7-4467-84bf-c77e22291691">

## Major Component
* User Authentication
  * Registration: Users can create accounts by providing a username, password, and email.
  * Login: Registered users can log in to access additional features.
  * Access Control: Only logged-in users can post articles and comments.
* Article Management
  * Post Articles: Logged-in users can create articles with a title, content, and category selection.
  * Browse Articles: Users can view articles categorized by topics.
  * Article Details: Users can view full articles along with associated comments.
* Comment System
  * Post Comments: Logged-in users can comment on articles.
  * Display Comments: Comments are displayed under each article in chronological order.


## Database schema
* The database has three tables. The first one stores all the account.
  * Users Table: stores user ID, username, password, and email.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/416bf16d-5adb-4a1c-acd1-5be4ba4075a6">

* The second stores the informaton of the articles.
  * Articles Table: stores article ID, title, content, category, author, article ID.

<img width="700" alt="image" src="https://github.com/user-attachments/assets/a031a487-c3ba-4262-8ca0-e8283d226efa">

* The third one stores all the comments.
  * Comments Table: stores content, article ID, author name.
<img width="700" alt="image" src="https://github.com/user-attachments/assets/c81ca470-a2b1-4e8c-9f56-095e4320f36c">


## Main Page
  This is the main page when you launch Python. You can click the left button for the articles or the right button to log in. There is also a navigation bar that you can use to turn to other pages.

![image](https://github.com/user-attachments/assets/ea5279db-2aa7-43cf-ac44-9704e6bc3a88)

## Login and Registration
  This is where you can create an account and log in. You are only allowed to issue an article if you have logged in.
![image](https://github.com/user-attachments/assets/c4beac3f-f034-49ca-be34-442fb73f4a50)
![image](https://github.com/user-attachments/assets/2ed61fa0-f7bc-4c47-bfe1-e3e49b8558b9)

## Issue an article
  You can issue an article on this page. The first part is the topic, followed by the context, then, you can choose which category it should be.
  Notice that, in `main.py`, line 9 and 10, you can put your email and your password. People who post an article will receive an email from that account, telling them that they have successfully posted the article.
```py
SMTP_SERVER = 'smtp.gmail.com'  
SMTP_PORT = 587  
SENDER_EMAIL = 'yourmail@com'  #put your email here
SENDER_PASSWORD = 'yourpassowrd'  #and password
```
![image](https://github.com/user-attachments/assets/f6efe33d-a6ec-4390-82bd-e1271c3fc8f6)

## Category 
  After posting an article, you can see it in its category. You can scroll and take a look at whatever attracts you.
![bandicam2024-11-1115-45-02-804-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/dfd5b22d-49de-43d0-b65f-ca5666e0d416)


## Comments
  If you see something that intrigues you, you can also leave a comment below it!
![bandicam2024-11-1115-53-41-485-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/b8e2fe74-e835-48d1-8231-ee9bc7c3b929)



That's pretty much all this project does. 


