from sqlalchemy import create_engine
import os

user_id = os.getenv("USER_ID")
password = os.getenv("DB_PASSWORD")
# host = "localhost:3307/ex260310"
host = f"{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
db_info = f"mysql+pymysql://{user_id}:{password}@{host}"
engine = create_engine(db_info, connect_args={})
