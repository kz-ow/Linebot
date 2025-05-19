import httpx
from typing import List, Optional
from dateutil import parser
from app.config import settings
import deepl

translator = deepl.Translator(auth_key=settings.DEEPL_API_KEY)


async def fetch_latest_news_by_category(
    categories: Optional[dict] = None,
    keywords: Optional[List[str]] = None,
    page_size: int = 5,
    country: str = "us",
) -> List[dict]:
    # --- 1. キーワード前処理（空白トリム） ---
    orig_kws = [kw.strip() for kw in (keywords or []) if kw.strip()]

    # --- 2. 日本語→英語 翻訳（個別翻訳でも一括翻訳でも可） ---
    if orig_kws:
        jp_query = " ".join(orig_kws)
        res = translator.translate_text(
            jp_query,
            target_lang="EN-US",
            source_lang="JA",
        )
        eng_kws = [w.strip() for w in res.text.split() if w.strip()]
    else:
        eng_kws = []

    # --- 3. カテゴリ抽出 ---
    selected = [cat for cat, on in (categories or {}).items() if on]
    category = selected[0] if selected else None

    # --- 4. ニュース取得ヘルパ ---
    async def _fetch(url: str, params: dict):
        params.setdefault("language", "en")
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            return r.json().get("articles", [])

    # --- 5. 動的キーワード緩和アルゴリズム ---
    #    (1) AND/OR ハイブリッド with 全キーワード → (2) OR 全キーワード → (3) 主要キーワードのみ → (4) カテゴリのみ
    search_strategies = []

    if eng_kws:
        # (1) AND/OR ハイブリッド
        main, *related = eng_kws
        if related:
            search_strategies.append(("top-headlines", {
                "q":    f"{main} AND ({' OR '.join(related)})",
                "category": category,
                "pageSize": page_size,
                "country": country,
            }))
        # (2) OR 全キーワード
        search_strategies.append(("everything", {
            "q":        " OR ".join(eng_kws),
            "sortBy":   "publishedAt",
            "pageSize": page_size,
        }))
        # (3) 主要キーワードのみ
        search_strategies.append(("everything", {
            "q":        main,
            "sortBy":   "publishedAt",
            "pageSize": page_size,
        }))
    # (4) カテゴリのみ
    if category:
        search_strategies.append(("top-headlines", {
            "category": category,
            "pageSize": page_size,
            "country":  country,
        }))

    articles = []
    # 順番に試して、ヒットがあったら抜ける
    for endpoint, params in search_strategies:
        params["apiKey"] = settings.NEWS_API_KEY
        url = f"https://newsapi.org/v2/{endpoint}"
        try:
            arts = await _fetch(url, params)
            if arts:
                articles = arts
                break
        except httpx.HTTPStatusError:
            continue

    # --- 6. ポストフィルタ: 元の日本語キーワードを全含有する記事のみ抽出 ---
    def matches_all(jp_kws: List[str], art: dict) -> bool:
        text = " ".join(filter(None, [art.get("title",""), art.get("description","")]))
        return all(kw.lower() in text.lower() for kw in jp_kws)

    filtered = []
    for art in articles:
        if orig_kws and not matches_all(orig_kws, art):
            continue
        filtered.append(art)
        if len(filtered) >= page_size:
            break

    # --- 7. 整形＆ソートして返却 ---
    result = []
    for art in filtered:
        result.append({
            "source":       art["source"]["name"],
            "title":        art["title"],
            "description":  art.get("description", ""),
            "url":          art["url"],
            "image_url":    art.get("urlToImage"),
            "published_at": art.get("publishedAt"),
        })
    result.sort(key=lambda x: parser.isoparse(x["published_at"]), reverse=True)
    return result
