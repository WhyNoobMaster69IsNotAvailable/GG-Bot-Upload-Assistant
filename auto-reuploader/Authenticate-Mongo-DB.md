Starting from GG Bot v3.1.3 onwards, the mongo db backend supports authentication. This allows users to expose mongoDB port publically and see the metadata from the local machine using tools such as MongoDB Compass. Also having authentication is a better practice.

## 1. Configure MongoDB with authentication.

To configure mongo with authentication, first you'll need to copy the mongo folder within the `samples/reuploader` folder to the location of your reuploader config location.
> The reuplaoder config location is the folder containing your `docker-compose.yml` file

The mongo db config folder contains the following files
- .mongo.env
- init-mongo.js
  > Do not edit the `init-mongo.js` file unless you know what you are dealing with.

The username and password for your database is configured in the .mongo.env file.

### Properties
- `MONGO_INITDB_ROOT_USERNAME`: Root user name. Set this to any value you like. This is not the user that gg bot will be using.
- `MONGO_INITDB_ROOT_PASSWORD`: The password for the root user. Set this to something secure.
- `MONGO_INITDB_DATABASE`: The init database. Default value is admin. <strong>Do not change this.</strong>
- `MONGO_DB_NAME`: The database that gg-bot will be using. Default value is set
- `MONGO_DB_USERNAME`: The username for ggbot user. This user needs to be configured in the uploader.
- `MONGO_DB_PASSWORD`: The password for ggbot mongo user.


Once the `.mongo.env` file has been configured, the values of `MONGO_DB_USERNAME` and `MONGO_DB_PASSWORD` should be set to the properties `cache_username` and `cache_password` in reupload.config.env

## Sample proper config
```
# .mongo.env
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin123
MONGO_INITDB_DATABASE=admin
MONGO_DB_NAME=gg-bot-reuploader
MONGO_DB_USERNAME=ggbot_user
MONGO_DB_PASSWORD=ggbot_password
```

```
# reupload.config.env
cache_type=Mongo
cache_host=mongo
cache_port=27017
cache_database=gg-bot-reuploader
cache_username=ggbot_user
cache_password=ggbot_password
```

Should you wish you use mongo-express to connect to the mongoDb then set the `.mongp_express.env` file to the following values.

```
# .mongo_express.env
ME_CONFIG_MONGODB_SERVER=mongo
ME_CONFIG_MONGODB_PORT=27017

ME_CONFIG_MONGODB_ENABLE_ADMIN=true

ME_CONFIG_MONGODB_AUTH_DATABASE=admin
ME_CONFIG_MONGODB_AUTH_USERNAME=admin
ME_CONFIG_MONGODB_AUTH_PASSWORD=admin123

ME_CONFIG_BASICAUTH_USERNAME=mongo_express_user
ME_CONFIG_BASICAUTH_PASSWORD=mongo_express_password
```
