//using UnityEngine;
//using UnityEngine.Networking;
//using UnityEngine.UI;
//using TMPro;
//using System.Collections;
//using System.Collections.Generic;

//public class Backup : MonoBehaviour
//{
//    // Inspectorから設定するUI要素
//    public GameObject[] spheres;
//    public Image fadePanel;
//    public TextMeshPro winText;
//    public GameObject dropdownPanel;
//    public TMP_Dropdown aliveDropdown;
//    public Button selectButton;

//    // 内部でキャラクターデータを管理するための辞書
//    private Dictionary<string, PersonData> personDataDict = new Dictionary<string, PersonData>();

//    // ゲームのどのフェーズかを判定するためのEnum（列挙型）
//    private enum GamePhase { AfterNight, AfterVote }

//    // ■■■ 1. Unityの初期化・更新処理 ■■■

//    void Start()
//    {
//        // ゲーム開始時にサーバーからキャラクター情報を取得して初期化
//        StartCoroutine(InitializeFromStartAPI());

//        // UI要素の初期状態を設定
//        if (fadePanel != null)
//            fadePanel.color = new Color(0, 0, 0, 0); // 透明にする

//        if (winText != null)
//            winText.gameObject.SetActive(false); // 非表示にする

//        if (dropdownPanel != null)
//            dropdownPanel.SetActive(false); // 非表示にする
//    }

//    void Update()
//    {
//        // Enterキーが押されたら、夜のターンを開始する
//        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
//        {
//            Debug.Log("Enterキーが押されました → 夜のターンを開始します");
//            StartCoroutine(FadeAndKill());
//        }
//    }

//    // ■■■ 2. メインのゲームフロー進行 ■■■

//    /// <summary>
//    /// ゲーム開始時に/start APIを呼び出し、キャラクターを初期化する
//    /// </summary>
//    IEnumerator InitializeFromStartAPI()
//    {
//        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:9000/start");
//        yield return request.SendWebRequest();

//        if (request.result != UnityWebRequest.Result.Success)
//        {
//            Debug.LogError("start API取得失敗: " + request.error);
//            yield break;
//        }

//        RoleWrapper roles = JsonUtility.FromJson<RoleWrapper>(request.downloadHandler.text);
//        Dictionary<string, RoleData> roleDict = roles.ToDictionary();

//        int i = 0;
//        foreach (var entry in roleDict)
//        {
//            if (i >= spheres.Length) break;

//            GameObject sphere = spheres[i];
//            PersonData pd = sphere.GetComponent<PersonData>();
//            if (pd != null)
//            {
//                pd.personName = entry.Key;
//                pd.textDisplay.text = entry.Key;
//                personDataDict[entry.Key] = pd;

//                Debug.Log($"登録: {entry.Key} → 役職: {entry.Value.role}, 生存: {entry.Value.alive}");
//            }
//            i++;
//        }
//    }

//    /// <summary>
//    /// 夜のターン。暗転し、/kill APIで犠牲者を取得して削除する。
//    /// </summary>
//    IEnumerator FadeAndKill()
//    {
//        // 暗転フェード
//        float duration = 1f;
//        float t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(0, 1, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        yield return new WaitForSeconds(0.5f);

//        // /kill API 呼び出し
//        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:9000/kill");
//        yield return request.SendWebRequest();

//        if (request.result != UnityWebRequest.Result.Success)
//        {
//            Debug.LogError("kill API取得失敗: " + request.error);
//            yield break;
//        }

//        KillData killData = JsonUtility.FromJson<KillData>(request.downloadHandler.text);

//        // 生存者リストに含まれていない球体（犠牲者）を削除
//        List<string> aliveList = killData.alive;
//        List<string> toRemove = new List<string>();

//        foreach (var entry in personDataDict)
//        {
//            if (!aliveList.Contains(entry.Key))
//            {
//                Debug.Log($"削除対象: {entry.Key}（aliveに含まれていない）");
//                Destroy(entry.Value.gameObject);
//                toRemove.Add(entry.Key);
//            }
//        }
//        foreach (string name in toRemove)
//        {
//            personDataDict.Remove(name);
//        }

//        yield return new WaitForSeconds(0.5f);

//        // フェード戻し
//        t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(1, 0, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        // 共通の勝利判定コルーチンを呼び出す（夜のターン後であることを伝える）
//        StartCoroutine(CheckForVictory(GamePhase.AfterNight));
//    }

//    /// <summary>
//    /// 投票ターン。選択されたキャラを暗転→API通知→削除→明転する。
//    /// </summary>
//    IEnumerator ProcessVoteAndKill(string name)
//    {
//        dropdownPanel.SetActive(false);

//        // 暗転フェード
//        float duration = 1f;
//        float t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(0, 1, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        // API呼び出し
//        string url = $"http://127.0.0.1:9000/vote_kill?name={UnityWebRequest.EscapeURL(name)}";
//        UnityWebRequest request = UnityWebRequest.Get(url);
//        yield return request.SendWebRequest();
//        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("vote_kill API送信失敗: " + request.error); }
//        else { Debug.Log("vote_kill API応答: " + request.downloadHandler.text); }

//        // オブジェクトの削除
//        if (personDataDict.ContainsKey(name))
//        {
//            Destroy(personDataDict[name].gameObject);
//            personDataDict.Remove(name);
//        }

//        yield return new WaitForSeconds(0.5f);

//        // フェード戻し
//        t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(1, 0, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        // 共通の勝利判定コルーチンを呼び出す（投票ターン後であることを伝える）
//        StartCoroutine(CheckForVictory(GamePhase.AfterVote));
//    }

//    // ■■■ 3. 共通処理（勝利判定・UI操作） ■■■

//    /// <summary>
//    /// 勝利条件を判定し、ゲームの終了または続行を決定する共通コルーチン
//    /// </summary>
//    IEnumerator CheckForVictory(GamePhase currentPhase)
//    {
//        Debug.Log("勝利判定を開始します。");

//        UnityWebRequest checkRequest = UnityWebRequest.Get("http://127.0.0.1:9000/start");
//        yield return checkRequest.SendWebRequest();

//        if (checkRequest.result != UnityWebRequest.Result.Success)
//        {
//            Debug.LogError("start API再取得失敗: " + checkRequest.error);
//            yield break;
//        }

//        RoleWrapper roles = JsonUtility.FromJson<RoleWrapper>(checkRequest.downloadHandler.text);
//        Dictionary<string, RoleData> roleDict = roles.ToDictionary();

//        int werewolfCount = 0;
//        int nonWerewolfCount = 0;
//        foreach (var name in personDataDict.Keys)
//        {
//            if (roleDict.ContainsKey(name))
//            {
//                if (roleDict[name].role == "WEREWOLF") werewolfCount++;
//                else nonWerewolfCount++;
//            }
//        }
//        Debug.Log($"生存者カウント: 人狼={werewolfCount}, 村人側={nonWerewolfCount}");

//        string resultMessage = null;
//        bool isGameOver = true;

//        if (werewolfCount == 0)
//        {
//            resultMessage = "VILLAGER WIN";
//        }
//        else if (werewolfCount >= nonWerewolfCount)
//        {
//            resultMessage = "WEREWOLF WIN";
//        }
//        else
//        {
//            isGameOver = false; // ゲーム続行
//        }

//        if (isGameOver)
//        {
//            // ゲーム終了時の演出
//            yield return StartCoroutine(ShowResultScreen(resultMessage, true));
//        }
//        else
//        {
//            // ゲーム続行時の処理
//            if (currentPhase == GamePhase.AfterNight)
//            {
//                // 夜の後なら投票へ
//                Debug.Log("ゲームは続行します。投票へ。");
//                ShowDropdownPanel();
//            }
//            else // AfterVote
//            {
//                // 投票の後なら次の夜へ
//                Debug.Log("ゲームは続行します。次の夜へ。");
//                yield return StartCoroutine(ShowResultScreen("CONTINUE", false));
//                StartCoroutine(FadeAndKill());
//            }
//        }
//    }

//    /// <summary>
//    /// 結果表示用の演出（暗転→テキスト表示）を行う共通コルーチン
//    /// </summary>
//    IEnumerator ShowResultScreen(string message, bool isGameOver)
//    {
//        // --- 1. 暗転 ---
//        float duration = 1f;
//        float t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(0, 1, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        // --- 2. テキスト表示 ---
//        if (winText != null)
//        {
//            winText.gameObject.SetActive(true);
//            winText.text = message;
//        }

//        // --- 3. 結果をプレイヤーに見せるために待機 ---
//        // ゲーム終了時は少し長め(4秒)、継続時は短め(2秒)に待つ
//        float waitTime = isGameOver ? 4.0f : 2.0f;
//        yield return new WaitForSeconds(waitTime);

//        // --- 4. 暗転を戻す ---
//        // 以前はisGameOverがtrueだとここで処理を終えていましたが、
//        // 今回は常に暗転を戻すようにします。
//        t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(1, 0, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        // --- 5. テキストの後処理 ---
//        // ゲームが続行する場合"だけ"テキストを非表示にする
//        if (!isGameOver)
//        {
//            winText.gameObject.SetActive(false);
//        }
//        // ゲーム終了時は、画面が明るく戻った後も勝利メッセージが表示されたままになります。
//    }

//    /// <summary>
//    /// 投票用のドロップダウンパネルを表示する
//    /// </summary>
//    void ShowDropdownPanel()
//    {
//        if (dropdownPanel != null)
//            dropdownPanel.SetActive(true);

//        if (aliveDropdown != null)
//        {
//            aliveDropdown.ClearOptions();
//            List<string> aliveNames = new List<string>(personDataDict.Keys);
//            aliveDropdown.AddOptions(aliveNames);

//            // ドロップダウン操作後のボタン不具合対策
//            aliveDropdown.onValueChanged.RemoveAllListeners();
//            aliveDropdown.onValueChanged.AddListener(delegate { OnDropdownValueChanged(); });
//        }

//        if (selectButton != null)
//        {
//            selectButton.onClick.RemoveAllListeners();
//            selectButton.onClick.AddListener(OnSelect);
//        }
//    }

//    /// <summary>
//    /// 投票ボタンが押されたときに呼ばれる
//    /// </summary>
//    public void OnSelect()
//    {
//        string selectedName = aliveDropdown.options[aliveDropdown.value].text;
//        Debug.Log($"選択されたキャラ: {selectedName}");
//        StartCoroutine(ProcessVoteAndKill(selectedName));
//    }

//    /// <summary>
//    /// ドロップダウンの値が変更されたときに呼ばれ、UIの状態をリフレッシュする
//    /// </summary>
//    public void OnDropdownValueChanged()
//    {
//        Debug.Log("ドロップダウンの値が変更されました。UIをリフレッシュします。");
//        StartCoroutine(RefreshUIPanel());
//    }

//    IEnumerator RefreshUIPanel()
//    {
//        dropdownPanel.SetActive(false);
//        yield return null;
//        dropdownPanel.SetActive(true);
//    }

//    // ■■■ 4. データ構造定義 ■■■

//    [System.Serializable]
//    public class RoleData { public bool alive; public string role; }

//    [System.Serializable]
//    public class RoleWrapper
//    {
//        public RoleData DeepSeek, GPT2, Mistral, gemma, llama3, tinyllama;
//        public Dictionary<string, RoleData> ToDictionary()
//        {
//            return new Dictionary<string, RoleData>
//            {
//                { "DeepSeek", DeepSeek }, { "GPT2", GPT2 }, { "Mistral", Mistral },
//                { "gemma", gemma }, { "llama3", llama3 }, { "tinyllama", tinyllama }
//            };
//        }
//    }

//    [System.Serializable]
//    public class KillData { public string victim; public List<string> alive; }
//}