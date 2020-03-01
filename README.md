# flask-backend
A backend service based on python and flask

How to Run:

1. git clone git@github.com:IamAbhiKaushik/flask-backend.git
2. cd flask-backend
3. `docker build -t flask-backend:latest .`
4. `docker run -d -p 5000:5000 flask-backend`
5. Go to `http://localhost:5000` in your browser for accessing backend API services.

## To run a mongo container, run the below command:
```
docker run -d \
  -e MONGO_INITDB_DATABASE=db \
  -p 27017:27017 mongo
```

## To go inside any running docker container: `docker exec -it <container ID> /bin/bash`


# New Update: V02
1. Added docker-compose file and mongo db base code
2. To run the code.. 
`docker-compse build`
`docker-compose up` 

Visit http://0.0.0.0:5000/ or http://localhost:5000 to verify Flask running

Visit `http://localhost:5000/add_url` or `http://localhost:5000/find_url` to test mongo running


Helpful URLs: 
1. https://medium.com/datadriveninvestor/writing-a-simple-flask-web-application-in-80-lines-cb5c386b089a
2. https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/

3. https://runnable.com/docker/python/dockerize-your-flask-application
4. https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
5. https://docs.mongodb.com/manual/core/index-unique/