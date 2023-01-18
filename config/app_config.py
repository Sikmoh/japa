# ---------------------------------------------------
# JWT JSON Web Tokens
# ---------------------------------------------------
JWT_ISSUER = "aerolab.com"
JWT_ALGORITHM = "HS256"

# Default secret used to create all new access JWTs
JWT_SECRET = "0f8014e60a33413b8f1ef6c414a5ed86"

JWT_REFRESH_SECRET = "0f8014e60a33413b8f1ef6c414a7ab21"

# Default secret used to create all new email JWTs
JWT_EMAIL_SECRET = "0h1014e60a33313b8f1ef6c414a5ed19"

# Default secret for password utilities
JWT_PASSWORD_SECRET = "0f8014e60a33413b8f1ef6c414a1de15"

# ---------------------------------------------------

# Default claims payloads for standard tokens
JWT_BASIC_PAYLOAD_CLAIM = ['user_id', 'standard_claim']

# Default claims payload for email JWTs
JWT_EMAIL_PAYLOAD_CLAIM = ['user_id', 'email_claim']

# Default claims payload for email JWTs
JWT_PASSWORD_PAYLOAD_CLAIM = ['user_id', 'password_claim']

# Default claims payload for refresh JWTs
JWT_REFRESH_PAYLOAD_CLAIM = ['user_id', 'refresh_claim']

# --------------------------------------------------

# Number of hours a standard API usage token lasts
JWT_ACCESS_HOURS = 10

# Number of hours an API refresh token lasts
JWT_REFRESH_HOURS = 24

# Number of hours an API password token lasts
JWT_PASSWORD_HOURS = 1

# Number of hours an API email token lasts
JWT_EMAIL_HOURS = 1


MYSQL = {
    'host': "localhost",  # 'localhost' #aerolab-mysql
    'user': "root",
    'password': "00Apassword7",
    'database': "flightdata"
}

REDIS = {
    "host": "localhost",  # 'localhost' #aerolab-redis
    'port': "6379",
    'db': "0",
    'password': "redisrocker"}

SMTP = {
    "host": "smtp-mail.outlook.com",
    "port": 587,
    "sender_email": "mohsikiru@outlook.com",
    "sender_password": "MR93BEAN//93"
}