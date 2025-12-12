"""
デモ2: LangChainで外部メモリ検索
- 必要な情報だけを検索して渡す仕組みを実演

使い方:
    python demo2_langchain.py 2-1    # 外部メモリを作成
    python demo2_langchain.py 2-2    # Docker関連を検索
    python demo2_langchain.py 2-3    # フロントエンド関連を検索
    python demo2_langchain.py 2-4    # 検索結果でLLMに質問
    python demo2_langchain.py all    # 全て実行
"""

import sys
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
client = OpenAI()

# 過去のメモ（外部メモリ）
MEMORY_TEXTS = [
    "ユーザーはJavaとSpring Bootでバックエンド開発をしている",
    "最近はマイクロサービスアーキテクチャに関心がある",
    "DockerとWSL2の環境で開発している",
    "Kafkaを使ったイベント駆動設計を勉強中",
    "フロントエンドはReactとTypeScriptを使用"
]

def create_db():
    """ベクトルDBを作成"""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma.from_texts(MEMORY_TEXTS, embeddings)

def demo_2_1():
    """外部メモリを作成"""
    print("=" * 60)
    print("【デモ2-1】外部メモリ（過去の情報）を作成")
    print("=" * 60)
    
    print("📝 外部メモリに保存された情報:")
    print("-" * 60)
    for i, text in enumerate(MEMORY_TEXTS, 1):
        print(f"  {i}. {text}")
    print()
    print("✅ ベクトルDBに保存完了")
    print()

def demo_2_2():
    """質問に関連する情報だけを検索"""
    print("=" * 60)
    print("【デモ2-2】質問に関連する情報だけを検索")
    print("=" * 60)
    
    db = create_db()
    query = "Dockerの開発環境を最適化したい"
    results = db.similarity_search(query, k=2)
    
    print(f"🔍 質問: {query}")
    print("-" * 60)
    print("📋 検索結果（関連度が高い情報）:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}")
    print()

def demo_2_3():
    """別の質問で試す"""
    print("=" * 60)
    print("【デモ2-3】別の質問で検索")
    print("=" * 60)
    
    db = create_db()
    query = "フロントエンドの技術スタックについて教えて"
    results = db.similarity_search(query, k=2)
    
    print(f"🔍 質問: {query}")
    print("-" * 60)
    print("📋 検索結果（関連度が高い情報）:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}")
    print()

def demo_2_4():
    """検索結果を使ってLLMに質問"""
    print("=" * 60)
    print("【デモ2-4】検索結果を使ってLLMに質問")
    print("=" * 60)
    
    db = create_db()
    query = "Dockerの開発環境を最適化したい"
    results = db.similarity_search(query, k=2)
    
    context = "\n".join([doc.page_content for doc in results])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"以下はユーザーに関する情報です:\n{context}"},
            {"role": "user", "content": query}
        ]
    )
    
    print(f"🔍 質問: {query}")
    print("-" * 60)
    print(f"📋 LLMに渡したコンテキスト:")
    print(f"  {context}")
    print("-" * 60)
    print("📥 LLMの応答:")
    print(response.choices[0].message.content)
    print()

def show_help():
    print("""
使い方: python demo2_langchain.py [デモ番号]

デモ番号:
    2-1    外部メモリの内容を表示
    2-2    Docker関連の検索
    2-3    フロントエンド関連の検索
    2-4    検索結果をLLMに渡して回答生成
    all    全て順番に実行
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == "2-1":
        demo_2_1()
    elif arg == "2-2":
        demo_2_2()
    elif arg == "2-3":
        demo_2_3()
    elif arg == "2-4":
        demo_2_4()
    elif arg == "all":
        demo_2_1()
        demo_2_2()
        demo_2_3()
        demo_2_4()
    else:
        show_help()