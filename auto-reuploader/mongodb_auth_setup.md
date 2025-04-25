# MongoDB Authentication Setup

This document explains how to configure GG Bot Upload Assistant to work with a MongoDB server that has authentication enabled.

## Configuration Parameters

In your `.env` file, you'll need to set the following parameters:

```
# MongoDB Connection Settings
cache_type=Mongo
cache_host=your-mongodb-host
cache_port=27017
cache_database=your-database-name

# MongoDB Authentication Settings
cache_username=your-mongodb-username
cache_password=your-mongodb-password
cache_auth_db=admin  # The database where your user credentials are stored
```

## Setting Up MongoDB with Authentication

If you're setting up a new MongoDB server with authentication, here's a quick guide:

### 1. Start MongoDB without Authentication

First, start MongoDB without authentication:

```bash
mongod --dbpath /path/to/data/directory
```

### 2. Connect to MongoDB and Create an Admin User

Connect to the MongoDB server:

```bash
mongo
```

Switch to the admin database and create an admin user:

```javascript
use admin
db.createUser({
  user: "admin",
  pwd: "secure_password",
  roles: [{ role: "userAdminAnyDatabase", db: "admin" }]
})
```

### 3. Create a User for GG Bot Upload Assistant

Create a user specifically for GG Bot Upload Assistant with access to its database:

```javascript
use admin
db.createUser({
  user: "gg_bot_user",
  pwd: "another_secure_password",
  roles: [{ role: "readWrite", db: "gg-bot-upload-assistant" }]
})
```

### 4. Enable Authentication

Restart MongoDB with authentication enabled:

```bash
mongod --dbpath /path/to/data/directory --auth
```

### 5. Update GG Bot Upload Assistant Config

Update your `.env` file with the credentials:

```
cache_username=gg_bot_user
cache_password=another_secure_password
cache_auth_db=admin
```

## Testing the Connection

You can test the MongoDB connection by starting the application. If the connection is successful, you'll see a log message:

```
[Cache] Successfully connected to MongoDB and initialized collections
```

If the authentication fails, you'll see an error message:

```
[Cache] MongoDB authentication failed. Please check your username and password.
```

## Troubleshooting

- Make sure the `cache_auth_db` is set to the database where the user was created
- Check for typos in username and password
- Ensure the MongoDB server is running with authentication enabled
- Verify the user has the appropriate permissions for the database 