## ✨ 特徴

* LLMによる感情的な発言生成
* 昼と夜のゲームサイクルを自動化
* 人狼・村人の役割をランダムに割り当て
* 殺害後の反応、疑いの発言を自動生成
* レーベンシュタイン距離による補正

## 🧠 使用技術一覧
*  **docker** –  環境構築
*  **vLLM** – 高速・省メモリなLLM推論エンジン 
*  **Llama-3-ELYZA-JP-8B-AWQ** – 日本語特化の大規模言語モデル 
*  **Transformers** – モデル＆トークナイザーの総合ライブラリ
*  **PyTorch** – ディープラーニング基盤フレームワーク 
*  **python-Levenshtein** – 文字列編集距離の高速計算ライブラリ 
*  **Python `random` モジュール** – 疑似乱数生成


## 🔧 主な構成


```
- game/
  - game_en.py
  - game_ja.py        
  - game_base.py      # 共通処理
- roles/
  - role.py           # 共通処理
  - wolf.py           # 人狼の挙動
  - villager.py       # 村人の挙動
```


