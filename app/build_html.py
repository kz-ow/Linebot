# build_html.py
import pathlib
from app.config import settings

# liff_category.htmlにLIFF_IDを埋め込み
LIFF_HTML_PATHS = {
    "LIFF_ID_CATEGORY": "/app/app/static/liff/liff_category.html",
    "LIFF_ID_DETAIL": "/app/app/static/liff/liff_detail_search.html",
    "LIFF_ID_REGULAR": "/app/app/static/liff/liff_regular.html"
}


# LIFF_IDを環境変数から取得し，htmlに埋め込む
def build_liff_html():
    """
    LIFF_IDを環境変数から取得し，htmlに埋め込む
    """
    for key, path in LIFF_HTML_PATHS.items():
        LIFF_ID = settings.__getattribute__(key)
        html = pathlib.Path(path).read_text(encoding="utf-8")
        html = html.replace("__LIFF_ID__", LIFF_ID)
        pathlib.Path(path).write_text(html, encoding="utf-8")
        print(f"ビルド完了 → {path}")


