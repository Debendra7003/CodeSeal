User Login & SingUp  API

1.Singup: 

    eexample:    {
                "username":"UUSER1234",
                 "email":"example@gmail.com",
                "phone_number":"9087654321",
                "password":"User@1234" (Password will be stored as encrypted)
                }
    Response:
            {
                "message": "Register successful"
            }
    
if someone request without any data the error will be occure:
  Example:
  {
    "message": "Register Failed",
    "errors": {
        "username": ["This field is required."],
        "email": ["This field is required."],
        "phone_number": ["This field is required."]
    }

    -----------------------------------------------------
   2. Login:
     It will take input username as login ID and password for login

     example:
             {
               "username":"UUSER1234",      ess  
                "password":"User@1234"
             }

    After successfully login the response is 
    ex:"message": "Login successful".

if the user input wrong info at time of login it will througing  error 
ex:"error": "Invalid credentials" or "Log in Failed"
