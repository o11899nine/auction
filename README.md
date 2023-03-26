# STUDENT SHOWCASE
## Video Demo:
#### https://youtu.be/jBJdAgcce5c

## Description
#### For my final project of CS50's Introduction to Computer Science I created a web application that my students (I'm a CS teacher) can use to showcase their CS projects. I used Python with Flask for the backend and HTML (with Jinja) and CSS for the frontend. To make everything prettier I used the Bootstrap framework. Also, everything is responsive and mobile-friendly.<br /><br />

#### The web application features a user login system. The user's information, such as e-mail address, name and password are stored in an SQL database. The password is hashed for safety. If the user does not have an account yet, they can create one. The info they input is validated by flask-wtforms validators. If all input is OK, their account is created. If not, an appropriate error message is shown. <br /><br />

#### Once logged in, the user is directed to a 'my projects' page, which initially is empty. A user can create a new project by going to the 'new project' page by clicking on the corresponding button in the navbar. To create a new project the user fills in a form with three fields: title, description and link. The description is limited to 1000 characters, the title to 39. Once the user submits their project, the project is shown on their 'my projects' page, as will all their future projects (for-loop in Jinja). <br /><br />


#### The last page of interest is the 'All projects' page. Here users can see all projects submitted by other users. This is the ultimate goal of this application; I want students to show off what they made with pride! They can check out their classmates projects, but it is also a great way to showcase what we do at our school at an open house night.<br /><br />

#### Finally, the user has the option to log out.<br /><br />

## Programmer's notes
### Files
#### **__init__.py**: This is where the app and .sqlite3 database is created and configured. It is only used when the program is first executed.<br /><br />

#### **auth.py**: This is where the user creation and authentication happens. Two forms are created here, which inherit from FlaskForm from the flask_wtf library. These are the forms used on the login and account creation page. The user's email address is validated by the built-in Email() function. Their password is validated using regex.<br /><br />

#### When the user creation form passes all validation, the e-mail address is checked against the database to see if the user alreadu exists. If not, the user is created and their data is put into the database.<br /><br />

#### When the user is logged in, the flask_login library takes care of keeping the user logged in until they choose to log out manually. This way the user can view pages that are for user eyes only by the @login_required decorator.<br /><br />

#### **main.py**: This is where the application's pages are created. The root redirects to a different page bases on whether the user is logged in or not. If the user is logged in, they are directed to the 'my projects' page, else they are prompted to log in. <br /><br />

#### The 'all_projects' function does one simple thing: query the database for a dictionary of all projects and then pass that dictionary to the all_projects.html page so all projects can be shown on that page. Almost the same thing happens on the 'my projects' page, but the query is filtered by the current user's id.<br /><br />

#### The 'new_project' function takes data from the form on the 'new project' page and then enters the new project into the Project table of the dataase. <br /><br />

#### **models.py**: This is where the database's tables are defined for further use in the application. <br /><br />

#### **base.html**: As the name suggests, this is the base html page with all necessary tags and imports to make all other .html pages show on screen properly. All other .html pages extend this page. This is also where the code for the navbar is located. The navbar only shows when a user is logged in. <br /><br />

### Future plans
#### I'm happy with how my application has turned out so far, especially since two months ago I would have struggled with building this while now things went quite smooth. There are still many more features I want to implement before releasing it to the world (or at least my students) and I'll continue working on this project.<br /><br />

