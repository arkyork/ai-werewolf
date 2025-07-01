
# LLMの内乱 喋るたびに敵を増やす村
**geek-camp 2025**

## 概要

LLM（大規模言語モデル）に **襲撃対象の選定から台詞生成まで** を一任し、人間プレイヤーが推理に集中できる新感覚の人狼ゲームです。  
役職（ロール）はクラスを継承するだけで自由に追加でき、単なるチャットボットではない“嘘をつく AI”の駆け引きを体験できます。


!["例"](./images/example1.png)

## 特長

- **情けない LLM** が見られる（人間のようにパニックに陥る）
- **擦り付け合いを始める LLM**（村人を装う人狼が必死に演技）
- **推論測度の高速化**：vLLMやローカルLLM対応で、スピードとコストを両立


## かんたんセットアップ

### 実行環境

- Unity 2022.3.24f
- Docker または Docker Desktop
- GPU + CUDA 12.4 以上

### インストール

```bash
git clone https://github.com/arkyork/ai-werewolf
cd ai-werewolf
````

### Python 側の処理（バックエンド）

初回のみ `docker compose build` を実行してください。

```bash
docker compose build
docker compose up -d
docker exec -it python-vllm bash
python main.py
```

## ディレクトリ構成（抜粋）

```
project-root/
├─ backend/                 # Python製のゲームロジック・LLM制御サーバー
│  ├─ app/
│  │  ├─ game/              # ゲーム進行処理（多言語対応）
│  │  │  ├─ __init__.py
│  │  │  ├─ game_base.py
│  │  │  ├─ game_en.py
│  │  │  └─ game_ja.py
│  │  ├─ roles/             # 役職の定義（人狼／占い師など）
│  │  ├─ main.py            # 実行エントリポイント
│  │  └─ sample.py          # サンプル実装・検証用
│  ├─ drafts/               # 開発用の草案ディレクトリ
│  ├─ test_code/            # テストコード
│  ├─ .env.example          # 環境変数サンプル
│  ├─ docker-compose.yml    # Docker構成（frontと統合）
│  ├─ Dockerfile            # backend用 Dockerfile
│  └─ requirements.txt      # Pythonライブラリ一覧
│
├─ front/                   # フロントエンド（観戦・操作UI）
│                           # C#×unity
│
└─ .gitignore               # Git管理から除外するファイル設定
```


## 謝辞



> **Enjoy the chaos — AI が嘘をつくとき、推理は新たなステージへ。**


