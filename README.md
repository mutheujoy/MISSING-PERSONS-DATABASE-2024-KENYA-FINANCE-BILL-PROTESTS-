# Lost in Kenya

## Step 1
Create an environment file with the following fields:

```env
POSTGRES_DB=host
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_PORT=5432
VOLUME_NAME=volume_name
APPLICATION_NETWORK=docker_network
APP_PORT
```

## step 2
create an external docker volume to store db data persistently

```env
docker volume create lostinkenya_postgres_data
```
 OR

```env
docker volume create lostinkenya_postgres_data_staging
```

## step 3
run the docker container to bring up the database and flask app

```env
docker-compose up --build -d --no-cache
```

OR 

```env
docker-compose -f docker-compose-staging.yaml up --build -d --no-cache
```

## step 4
type the following on your browser url bar  to access the UI

```env
localhost:5000
```

OR

```env
https://lostinkenya.org
```

OR

```env
https://staging.lostinkenya.org
```
