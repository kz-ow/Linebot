# モジュールのインポートを保護
from janome.tokenizer import Tokenizer
from gensim.models import KeyedVectors
import numpy as np

# トークナイザーと単語ベクトルモデルの初期化
tokenizer = Tokenizer() if Tokenizer else None
try:
    wv = KeyedVectors.load("ja_word2vec.kv") if KeyedVectors else None
except Exception:
    wv = None


# 単語リストからベクトル平均を取得
def avg_vec(words: list[str]) -> np.ndarray | None:
    if not wv:
        return None
    vs = [wv[w] for w in words if w in wv]
    return np.mean(vs, axis=0) if vs else None


def extract_keywords(
    text: str,
    top_k: int = 5,
    threshold: float = 0.4
) -> tuple[list[str], str]:
    """
    1) 形態素解析で名詞 top_k を抽出
    2) 辞書マッチとベクトル類似度でカテゴリ推定
    戻り値: (keywords, category)
    """
    # トークナイザーがなければ終了
    if not tokenizer:
        return [], "general"

    # 名詞を抽出
    tokens = tokenizer.tokenize(text)
    nouns = [t.surface for t in tokens if t.part_of_speech.split(',')[0] == "名詞"]

    # 上位 top_k のキーワードを取得
    seen = set()
    keywords: list[str] = []
    for w in nouns:
        if w not in seen:
            seen.add(w)
            keywords.append(w)
        if len(keywords) >= top_k:
            break
    
    # キーワード AND キーワードのstringを作成
    print(f"キーワード: {keywords}")
    
    return keywords
