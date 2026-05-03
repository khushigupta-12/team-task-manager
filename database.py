import os

DATABASE_URL = os.getenv("DATABASE_URL")

print("DEBUG DATABASE_URL:", DATABASE_URL)  # add this line

if not DATABASE_URL:
    raise Exception("DATABASE_URL not set!")

DATABASE_URL = DATABASE_URL.replace(
    "postgresql://",
    "postgresql+psycopg2://"
)