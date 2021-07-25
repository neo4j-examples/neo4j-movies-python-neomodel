# Resonate Tag Charts

## How to setup locally

### Install dependencies

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Create the Neo4j database and import your data (TODO)


### Add export the NEO4J_BOLT_URL

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


## How to deploy to Heroku

Go to your Heroku dashboard and create a new app and add its git remote to your local clone of this app.

Go your Heroku's app's settings and add the `NEO4J_BOLT_URL` environment variable with the correct credentials:

```NEO4J_BOLT_URL="bolt://neo4j:password@host-or-ip:port"```

Now you can push to Heroku:

```shell
git push heroku master
```

And thats all you need :)
