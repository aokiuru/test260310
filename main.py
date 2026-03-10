import uvicorn
from fastapi import FastAPI, status, Path
from fastapi.responses import JSONResponse
from sqlalchemy import text, create_engine
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
import os

print(os.getenv("PATH"))
print(os.getenv("USER_ID"))

# DB 연결
# user_id = os.getenv("USER_ID")
# password = os.getenv("DB_PASSWORD")
# # host = "localhost:3307/ex260310"
# host = f"{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
# db_info = f"mysql+pymysql://{user_id}:{password}@{host}"
# engine = create_engine(db_info, connect_args={})
# print(engine)
from utils.database import engine

app = FastAPI()
# [TODO]
# CORS 설정
# https://velog.io/@rhqjatn2398/Access-Control-Allow-Credentials 참고
app.add_middleware(
    CORSMiddleware,
    {
        "allow_origin": ["http://localhost:3000", "http://192.168.0.29"],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    },
)


posts = [
    {"post_id": 1, "title": "포스트 1", "content": "내용 1"},
    {"post_id": 2, "title": "포스트 2", "content": "내용 2"},
    {"post_id": 3, "title": "포스트 3", "content": "내용 3"},
]

# post_id 받아서 특정게시글 가져오는 API


@app.get("/posts/{post_id}")
def get_postbyID(post_id=Path(...)):
    try:
        query = text(
            """
            SELECT post_id, title, content FROM  posts WHERE post_id = :post_id
            """
        )
        with engine.connect() as conn:
            import pandas as pd

            df = pd.read_sql(
                query,
                conn,
                params={"post_id": post_id},
            )
            posts = df.to_dict(orient="records")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"data": posts},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": str(e),
            },
        )


@app.get("/posts")
def get_post():
    try:
        query = text(
            """
            SELECT post_id, title, content FROM  posts
            """
        )
        with engine.connect() as conn:
            import pandas as pd

            df = pd.read_sql(query, conn)
            posts = df.to_dict(orient="records")

        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": posts})
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"error": str(e)}
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
