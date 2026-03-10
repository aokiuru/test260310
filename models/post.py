from sqlalchemy import text

from utils.database import engine

# 삽입/조회/수정/삭제


# routes -> 주소 -> 함수(controller) ->
# 넘겨 받은 요청 파라미터 -> service 쪽으로 전달 ->
# service 쪽에서 전달 받은 파라미터를 model쪽으로 전달
# 전달 받은 파라미터(post_id)
def get_post_by_id(post_id):
    # MODEL쪽은 SQL 쿼리를 요청해서 반환하는 것만 담당
    query = text(
        """
            SELECT post_id, title, content FROM posts
            WHERE post_id = :post_id
            """
    )
    with engine.connect() as conn:
        import pandas as pd

        df = pd.read_sql(query, conn, params={"post_id": post_id})
        posts = df.to_dict(orient="records")
    return posts


# 처리 후 동작
# model쪽에서 값을 반환 -> Service 쪽에서 전달 받아서
# 비즈니스 로직 수행(오류 발생 혹은 결과를 전송) ->
# controllers 쪽으로 값을 전달 -> 요청했던 클라이언트 쪽으로
# 결과를 반환
