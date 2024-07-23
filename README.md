# Lost in Kenya

## Step 1
Create an environment file with the following fields:

```env
POSTGRES_DB=xxxx
POSTGRES_USER=yyyy
POSTGRES_PASSWORD=zzzz
POSTGRES_PORT=5432


## step 2
create an external docker volume to store db data persistently

docker volume create lostinkenya_postgres_data

## step 3
run the docker container to bring up the database and flask app

docker compose up --build -d

## step 4
from your browser type url bar, type `localhost:5000` to access the UI