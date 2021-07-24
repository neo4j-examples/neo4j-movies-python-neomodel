# neo4j-movies-python-neomodel

## How to setup locally

### Install dependencies

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Create the Neo4j database with correct data

Go to [Neo4j's Sandbox](https://sandbox.neo4j.com/) and create a new project, select Movies under Pre Built Data. Go to `Connection details` and grab your credentials to add it to the following environment variable:

```shell
export NEO4J_BOLT_URL=bolt://neo4j:password@host-or-ip:port
```

Run migrations and create your superuser (for the admin, this is using an SQLite database)

```
./manage.py migrate
./manage.py createsuperuser
```

### Run the server

```shell
python manage.py runserver
```

Now you should be able to access http://localhost:8000 and play with the app.

## Using the Admin with the Sandbox Dataset

Since the Movies dataset in the sandbox is a toy dataset, we need to make some minor changes to get it to work with our Django Admin. 
Primarily, we need to add unique ids to our nodes so we can open their detail view:

``` Example Movie Node
{
  "identity": 0,
  "labels": [
    "Movie"
  ],
  "properties": {
"tagline": "Welcome to the Real World",
"title": "The Matrix",
"released": 1999
  }
}
```

For simplicity, do:

```
MATCH (n) 
SET n.uuid = toString(id(n))
```

Now you can log into the admin with your superuser and take a look at your Move and Person nodes. 

## How to deploy to Heroku

Go to your Heroku dashboard and create a new app and add its git remote to your local clone of this app.

Go your Heroku's app's settings and add the `NEO4J_BOLT_URL` environment variable with the correct credentials:

```NEO4J_BOLT_URL="bolt://neo4j:password@host-or-ip:port"```

Now you can push to Heroku:

```shell
git push heroku master
```

And thats all you need :)
