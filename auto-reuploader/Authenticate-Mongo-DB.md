# MongoDB Authentication Setup for GG Bot Upload Assistant

Starting from GG Bot v3.1.3 onwards, the mongo db backend supports authentication. This allows users to expose mongoDB
port publicly and see the metadata from the local machine using tools such as MongoDB Compass. Also having
authentication is a better practice. This document explains how to use MongoDB with authentication in the GG Bot Upload
Assistant Docker Compose setup.

## Overview

The Docker Compose configuration now includes:

1. A MongoDB container with authentication enabled
2. A mongo-express container for web-based MongoDB management
3. Automated user creation with predefined credentials

## Default Credentials

The setup creates the following users by default:

| User        | Password        | Role                           | Purpose                                            |
|-------------|-----------------|--------------------------------|----------------------------------------------------|
| root        | root_password   | root                           | MongoDB root user created by Docker                |
| admin       | admin_password  | userAdminAnyDatabase           | Admin user for mongo-express and DB administration |
| gg_bot_user | gg_bot_password | readWrite on gg-bot-reuploader | Application user for GG Bot                        |

## Configuration Files

The following files have been modified or created:

1. `docker-compose-*.yml` - Updated MongoDB service to use authentication
2. `mongo-init.js` - JavaScript file to initialize MongoDB users and collections
3. `.mongo_express.env` - Configuration for mongo-express with authentication
4. `reupload.config.env` - Updated to use MongoDB authentication

## Customizing Credentials

You should change the default passwords in:

1. The MongoDB service environment variables in `docker-compose-*.yml` (MONGO_INITDB_ROOT_USERNAME,
   MONGO_INITDB_ROOT_PASSWORD)
2. The `mongo-init.js` file (admin and gg_bot_user passwords)
3. The `.mongo_express.env` file (ME_CONFIG_MONGODB_AUTH_PASSWORD)
4. The `reupload.config.env` file (cache_password)

Make sure to use the same values in all related places.

## Encrypting MongoDB Credentials

For enhanced security, you can encrypt sensitive MongoDB credentials in your configuration files:

1. Mark the MongoDB password in `reupload.config.env` for encryption:
   ```
   cache_username=gg_bot_user
   cache_password=gg_bot_password # ENCRYPT
   ```

2. Use the encryption CLI to encrypt the password:
   ```bash
   python encrypt_cli.py encrypt -i reupload.config.env
   ```

3. Ensure your `PRIVATE_KEY_PATH` is set correctly in your configuration.

For detailed instructions on using encrypted configuration, see the `docs/config_encryption.md` file.

## Accessing mongo-express

mongo-express is available at http://localhost:8081 (or the host/port you've configured).
Use the admin credentials to log in:

- Username: admin
- Password: admin

Should you wish you use mongo-express to connect to the mongoDb then set the `.mongp_express.env` file to the following
values.

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

## Troubleshooting

If you encounter connection issues:

1. Check that the credentials in `reupload.config.env` match those in `mongo-init.js`
2. Verify that MongoDB started properly with authentication enabled
3. Check logs with `docker-compose logs mongo`
4. For a fresh start, remove the MongoDB volumes: `docker-compose down -v` then restart
