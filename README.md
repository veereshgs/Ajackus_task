# Ajackus_task

After Downloading the project
Do the followings:

    step1 : pip install -r requirements.txt
    

if want seed the json file u can use the following loaddata command 

        python manage.py loaddata seed/admin.json

    step2: python manage.py runserver

using seed we created Admin and here we can create one more user through register api, i.e
Author user
    
    POST Method :-    

        link: http://127.0.0.1:8000/user_register/

After Register U will get JWT token u can use this for create, view , edit and delete API

Now u can login using the login API
        
    POST Method :- 

        link : http://127.0.0.1:8000/login/api/


After login u can go create content by using the below API
    
POST Method :-

        link : http://127.0.0.1:8000/content_api/

    here u need to upload document as well

PUT Method : - for edit 

        link : http://127.0.0.1:8000/content_api/

GET method : for view data with search option
        
        http://127.0.0.1:8000/content_data/   --this is for all data

        http://127.0.0.1:8000/content_data/?search=body1 updated --- this is for searched for perticular data

DELETE Method: 
        
    http://127.0.0.1:8000/content_data/

    in this api u need to pass id 
