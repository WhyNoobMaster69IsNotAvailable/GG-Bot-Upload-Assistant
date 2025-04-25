// MongoDB initialization script
// This script will be run when the MongoDB container is first initialized
// It creates an admin user and a user for the GG Bot application

// Create admin user
db = db.getSiblingDB('admin');
db.createUser({
  user: 'admin',
  pwd: 'admin_password',
  roles: [
    { role: 'userAdminAnyDatabase', db: 'admin' },
    { role: 'readWriteAnyDatabase', db: 'admin' }
  ]
});

// Create user for GG Bot application
db.createUser({
  user: 'gg_bot_user',
  pwd: 'gg_bot_password',
  roles: [
    { role: 'readWrite', db: 'gg-bot-reuploader' }
  ]
});

print('MongoDB users created.');
