Running
---
Go to the app dir and run the commands
> pip3 install -r requirements.txt
> 
> cp ./example.env ./.env
> 
> export $(grep -v '^#' .env | xargs)
> 
> python screanshots.py 

The app will be running at http://0.0.0.0:8080
