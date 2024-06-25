A collective of photographers is looking for a way to show and share their work to a wide audience. 
They want to be able to put their photos online and create posts about them on a blog. 
They called on you as a Django developer, and asked you to create a web application that allows them to do just that. 
They need to have two types of users, subscribers and creators. Only creators should be able to create content. 
This content should then be shared in a social feed, and subscribers should be able to choose which creators they want.

Our project includes two applications: 
one, called authentication, which will manage authentication and accounts, 
and the other, blog, which will host our logic for sharing blog posts and photos.


# Envirements :

Links
* [git clone git@github.com:m-dahmani/FotoBlog.git](git clone git@github.com:m-dahmani/FotoBlog.git "more info")
* 
* https://www.linkedin.com/in/mohamed-d-a74627a9/


### → git clone git@github.com:m-dahmani/FotoBlog.git

### → python3 -m venv env

### → source env/bin/activate

### → pip install -r requirements.txt 

### → python manage.py showmigrations

### → python manage.py migrate

### → python manage.py createsuperuser

* Username: admin
  Email address: 
  * Password (again):
     * Password must contain a number
     * Bypass password validation and create user anyway? [y/N]: y

#### Superuser created successfully.


#### → python manage.py runserver 0.0.0.0:8000