# Encrypted Configuration

This document explains how to use encrypted configuration values in GG Bot Upload Assistant to protect sensitive information like API keys and passwords.

## Overview

GG Bot Upload Assistant supports encrypted configuration values in config.env files, allowing you to protect sensitive information such as:

- API keys
- Tracker passkeys
- MongoDB authentication credentials
- Other sensitive data

The encryption uses RSA public/private key pairs to securely store sensitive values in your configuration files.

## How Encryption Works

1. You mark sensitive values in your config.env file with a special marker (`# ENCRYPT`)
2. You use the encryption CLI tool to encrypt those values
3. The values are encrypted with a public key and stored with an `ENC::` prefix
4. When the application runs, it uses a corresponding private key to decrypt the values

## Setup

### 1. Generate Key Pair

First, generate an RSA key pair:

```bash
python encrypt_cli.py generate-keys
```

This will create:
- `keys/private_key.pem` - Keep this secure and don't share it
- `keys/public_key.pem` - You can use this to encrypt values

You can specify custom paths for the keys:

```bash
python encrypt_cli.py generate-keys --private-key /path/to/my_private_key.pem --public-key /path/to/my_public_key.pem
```

### 2. Mark Sensitive Values for Encryption

In your config.env file, mark any sensitive values with `# ENCRYPT` at the end of the line:

```
# API Keys
TMDB_API_KEY=my_secret_api_key # ENCRYPT
BHD_API_KEY=another_secret_key # ENCRYPT

# MongoDB authentication
cache_username=gg_bot_user
cache_password=my_secure_password # ENCRYPT
```

### 3. Encrypt the Configuration

Use the encryption CLI to encrypt the marked values:

```bash
python encrypt_cli.py encrypt -i config.env -o config.env.encrypted
```

This will create a new file with encrypted values:

```
# API Keys
TMDB_API_KEY=ENC::A8fG7dH6jK9lM2nP5qR8tU1vW4xZ7yA3bC6dE9fG2hJ5kL8mN1pQ4rS7tU0
BHD_API_KEY=ENC::B9gH8eJ7kL0mN3pQ6rT9uV2wX5yZ8aB4cD7eF0gH3jK6lM9nP2qR5sT8uV1

# MongoDB authentication
cache_username=gg_bot_user
cache_password=ENC::C0hI9fJ8kL1mN4pQ7rT0uV3wX6yZ9aB5cD8eF1gH4jK7lM0nP3qR6sT9uV2
```

If you want to overwrite the original file (with a backup):

```bash
python encrypt_cli.py encrypt -i config.env
```

### 4. Set Private Key Path in Configuration

The application needs to know where to find your private key. Add this to your config.env file:

```
PRIVATE_KEY_PATH=/path/to/private_key.pem
```

You can also let the encrypt CLI add this for you:

```bash
python encrypt_cli.py encrypt -i config.env --private-key /path/to/private_key.pem
```

## Using Encrypted Configuration

Once you've encrypted your configuration and set up the private key path, GG Bot Upload Assistant will automatically decrypt the values when needed.

### Docker Setup

For Docker environments, you need to:

1. Mount your private key file into the container
2. Set the `PRIVATE_KEY_PATH` environment variable to the mounted location

Example in docker-compose.yml:

```yaml
gg-bot-auto-uploader:
  image: noobmaster669/gg-bot-uploader:${GG_BOT_REUPLOADER_VERSION}
  volumes:
    - ${BASE_PATH}/data/downloads:/downloads
    - /path/to/private_key.pem:/app/private_key.pem
  environment:
    - PRIVATE_KEY_PATH=/app/private_key.pem
  env_file:
    - reupload.config.env
```

## Security Recommendations

1. **Never share your private key**: Keep your private key in a secure location and never commit it to version control
2. **Set appropriate file permissions**: Ensure your private key and encrypted config files have restricted permissions
3. **Regular key rotation**: Periodically generate new key pairs and re-encrypt your sensitive data
4. **Backup your keys**: Ensure you have secure backups of your private key, as losing it means losing access to encrypted values

## Command Reference

### Generate Keys

```bash
python encrypt_cli.py generate-keys [--private-key PATH] [--public-key PATH] [--force]
```

Options:
- `--private-key`: Path to save the private key (default: private_key.pem)
- `--public-key`: Path to save the public key (default: public_key.pem)
- `--force`: Overwrite existing key files without prompting

### Encrypt Configuration

```bash
python encrypt_cli.py encrypt -i INPUT_FILE [-o OUTPUT_FILE] [-k PUBLIC_KEY] [--private-key PRIVATE_KEY]
```

Options:
- `-i, --input`: Path to the input config.env file
- `-o, --output`: Path to write the output file (if omitted, overwrites the input with backup)
- `-k, --public-key`: Path to the public key (default: public_key.pem)
- `--private-key`: Path to the private key to update in the configuration

## Troubleshooting

1. **Decryption errors in logs**: Ensure your private key path is correct and the file is readable
2. **Application uses default values**: This happens when decryption fails, check your private key
3. **"Value too large for encryption"**: RSA encryption has size limitations, extremely long values may need alternative encryption methods 