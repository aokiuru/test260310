'''
pip install sqlalchemy
sqlalchemy: python에서 RDBS 연결하는 패키지
'''
from sqlalchemy import create_engine, text

user_id = "aokiuru"
password = "1111"
host = "localhost:3307/ex260310"
db_info = f"mysql+pymysql://{user_id}:{password}@{host}"

engine = create_engine(db_info, connect_args={}) 
conn = engine.connect()
# conn.execute(sql구문)

conn.execute("SELECT * FROM posts") # 오류
rows = conn.execute(text("SELECT * FROM posts"))
rows.fetchall()

import pandas as pd
df = pd.read_sql(
    text("SELECT * FROM posts"),
    conn)
df["created_at"] = df["created_at"].astype(str)
df["updated_at"] = df["updated_at"].astype(str)

df.to_dict(orient= "records")
conn.close()    # DB 연결 종료

df = None
# conn = engine.connect()
# with 구문 내에서만 conn 동작하고 자연스럽게 닫힘 
with engine.connect() as conn:
    df = pd.read_sql(text("SELECT * FROM posts"),conn)
df

# with engine.begin() as conn:
    # sql query1
    # sql query2  오류발생
    # sql query3
    # begin: 오류발생시 1,2,3 모두를 취소(롤백)

with engine.connect() as conn:
    # sql 인젝션: 의도적으로 sql 구문을 수정해서 데이터를
    # 탈취하는 해킹 기법
    # f"SELECT * FROM posts where post_id = {num}"
    # where 1 = 1 ; & 다른 데이터 추출 SQL 추가로 기재
    # 데이터 탈취하는 형태
    # 오답
    num = 3
    df = pd.read_sql(
        text(f"SELECT * FROM posts where post_id = {num}"),
        conn)
    # 하단의 방식으로 SQL 인젝션 방지
with engine.connect() as conn:
    num = 1
    df = pd.read_sql(
        text("SELECT * FROM posts where post_id = :num"),
        conn, params =  {"mun":num})

with engine.connect() as conn:
    num = 1
    row = conn.execute(
        text("SELECT * FROM posts where post_id = :num"),
        {"num":num})
row.fetchall()











