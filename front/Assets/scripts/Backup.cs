//using UnityEngine;
//using UnityEngine.Networking;
//using UnityEngine.UI;
//using TMPro;
//using System.Collections;
//using System.Collections.Generic;
//using Newtonsoft.Json; // Newtonsoft.Jsonライブラリを使用する宣言

//public class Wolf : MonoBehaviour
//{
//    // ■■■ フィールド定義 ■■■

//    [Header("基本設定")]
//    public GameObject[] spheres;

//    [Header("演出用UI")]
//    public Image fadePanel;
//    public TextMeshPro winText;

//    [Header("投票用UI")]
//    public GameObject dropdownPanel;
//    public TMP_Dropdown aliveDropdown;
//    public Button selectButton;

//    [Header("ログUI")]
//    public GameObject logPanel;
//    public RectTransform logContent;
//    public GameObject logMessagePrefab;
//    public GameObject logOpenButton; // ログを開くボタン

//    private Dictionary<string, PersonData> personDataDict = new Dictionary<string, PersonData>();

//    // ゲーム開始時の全キャラクターの役職情報を保持するための辞書
//    private Dictionary<string, RoleData> fullRoleData;
//    private enum GamePhase { AfterNight, AfterVote }
//    private bool isGameFinished = false; // ゲームが終了したかを管理するフラグ

//    // ■■■ 1. Unityの初期化・更新処理 ■■■

//    void Start()
//    {
//        StartCoroutine(InitializeFromStartAPI());
//        if (fadePanel != null) fadePanel.color = new Color(0, 0, 0, 0);
//        if (winText != null) winText.gameObject.SetActive(false);
//        if (dropdownPanel != null) dropdownPanel.SetActive(false);
//        if (logPanel != null) logPanel.SetActive(false);
//        if (logOpenButton != null) logOpenButton.SetActive(false);
//    }

//    void Update()
//    {
//        if (isGameFinished) return; // ゲーム終了後はキー入力を無効にする

//        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
//        {
//            Debug.Log("Enterキーが押されました → 夜のターンを開始します");
//            StartCoroutine(FadeAndKill());
//        }
//    }

//    // ■■■ 2. メインのゲームフロー進行 ■■■

//    IEnumerator InitializeFromStartAPI()
//    {
//        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:5000/start");
//        yield return request.SendWebRequest();
//        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("start API取得失敗: " + request.error); yield break; }

//        // Newtonsoft.Jsonを使い、JSONを直接「名前と役職データの辞書」に変換
//        var roleDict = JsonConvert.DeserializeObject<Dictionary<string, RoleData>>(request.downloadHandler.text);

//        this.fullRoleData = roleDict; // 取得した役職情報をクラスのフィールドに保存する

//        Debug.Log("---  ゲーム開始: /start API 結果 ---");
//        foreach (var roleEntry in roleDict)
//        {
//            Debug.Log($"キャラクター: {roleEntry.Key}, 役職: {roleEntry.Value.role}");
//        }
//        Debug.Log("---  ゲーム開始: /start API 結果  ---");

//        int i = 0;
//        foreach (var entry in roleDict) // これでJSON内の全キャラクターをループできる
//        {
//            if (i >= spheres.Length) break;
//            GameObject sphere = spheres[i];
//            PersonData pd = sphere.GetComponent<PersonData>();
//            if (pd != null)
//            {
//                pd.personName = entry.Key; // entry.Keyが "あかね", "けんた" などの名前になる
//                pd.textDisplay.text = entry.Key;
//                personDataDict[entry.Key] = pd;
//            }
//            i++;
//        }
//    }

//    IEnumerator FadeAndKill()
//    {
//        float duration = 1f;
//        float t = 0f;
//        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(0, 1, t / duration)); yield return null; }

//        yield return new WaitForSeconds(0.5f);

//        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:5000/kill");
//        yield return request.SendWebRequest();
//        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("kill API取得失敗: " + request.error); yield break; }

//        var fullKillData = JsonConvert.DeserializeObject<FullKillData>(request.downloadHandler.text);

//        Debug.Log("---  夜のターン結果 (/kill API)  ---");
//        if (fullKillData.victim != null && fullKillData.victim.Count > 0)
//        {
//            // 犠牲者とその役職を表示
//            Debug.Log($"犠牲者: {fullKillData.victim[0]} ({fullKillData.die_role})");
//        }
//        else
//        {
//            Debug.Log("犠牲者はいませんでした。");
//        }
//        // 占い師やパン屋の結果も表示
//        Debug.Log($"占い結果: {fullKillData.divine_role}");
//        Debug.Log($"パン配布情報(パンの数): {fullKillData.bread_num}");

//        List<string> toRemove = new List<string>();
//        foreach (var entry in personDataDict)
//        {
//            if (!fullKillData.alive.Contains(entry.Key)) { Destroy(entry.Value.gameObject); toRemove.Add(entry.Key); }
//        }
//        foreach (string name in toRemove) { personDataDict.Remove(name); }

//        yield return new WaitForSeconds(0.5f);

//        t = 0f;
//        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(1, 0, t / duration)); yield return null; }

//        StartCoroutine(CheckForVictory(GamePhase.AfterNight, fullKillData));
//    }

//    IEnumerator ProcessVoteAndKill(string name)
//    {
//        dropdownPanel.SetActive(false);
//        float duration = 1f;
//        float t = 0f;
//        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(0, 1, t / duration)); yield return null; }

//        string url = $"http://127.0.0.1:5000/vote_kill?name={UnityWebRequest.EscapeURL(name)}";
//        UnityWebRequest request = UnityWebRequest.Get(url);
//        yield return request.SendWebRequest();
//        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("vote_kill API送信失敗: " + request.error); }

//        if (personDataDict.ContainsKey(name)) { Destroy(personDataDict[name].gameObject); personDataDict.Remove(name); }

//        yield return new WaitForSeconds(0.5f);

//        t = 0f;
//        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(1, 0, t / duration)); yield return null; }

//        StartCoroutine(CheckForVictory(GamePhase.AfterVote, null));
//    }

//    // ■■■ 3. 共通処理（勝利判定・UI操作） ■■■

//    IEnumerator CheckForVictory(GamePhase currentPhase, FullKillData killData)
//    {
//        var roleDict = this.fullRoleData;
//        if (roleDict == null)
//        {
//            Debug.LogError("役職データが初期化されていません！");
//            yield break;
//        }

//        // --- 1. 生存者を3つの陣営に分けてカウント ---
//        int werewolfTeamCount = 0; // 人狼(WEREWOLF) + 狂人(MADMAN)
//        int villagerTeamCount = 0; // 村人、騎士、占い師などの村人陣営
//        int foxCount = 0;          // 妖狐(FOX)
//        int pureWerewolfCount = 0; // 村人勝利判定のための、純粋な人狼の数

//        Debug.Log($"--- ▼▼▼ {currentPhase}後の生存者状況確認 ▼▼▼ ---");
//        foreach (var name in personDataDict.Keys)
//        {
//            if (roleDict.ContainsKey(name))
//            {
//                string role = roleDict[name].role.ToUpper();
//                Debug.Log($"生存者: {name}, 役職: {role}");

//                if (role == "WEREWOLF") { werewolfTeamCount++; pureWerewolfCount++; }
//                else if (role == "MADMAN") { werewolfTeamCount++; }
//                else if (role == "FOX") { foxCount++; }
//                else { villagerTeamCount++; }
//            }
//        }
//        Debug.Log($"--- ▲▲▲ {currentPhase}後の生存者状況確認 ▲▲▲ ---");
//        Debug.Log($"生存者カウント: 人狼陣営={werewolfTeamCount}, 村人陣営={villagerTeamCount}, 妖狐={foxCount}");

//        // --- 2. まず、村人か人狼の勝利条件を満たしているか判定 ---
//        string normalWinMessage = null;
//        bool normalGameEndConditionMet = false;

//        // a. 村人勝利条件：人狼が全滅しているか？
//        if (pureWerewolfCount == 0)
//        {
//            normalWinMessage = "VILLAGER WIN";
//            normalGameEndConditionMet = true;
//        }
//        // b. 人狼陣営勝利条件：人狼陣営の数が、村人陣営の数以上になったか？ (妖狐は数に含めない)
//        else if (werewolfTeamCount >= villagerTeamCount)
//        {
//            normalWinMessage = "WEREWOLF WIN";
//            normalGameEndConditionMet = true;
//        }

//        // --- 3. 最終的な勝者を決定し、ゲームを終了または続行する ---
//        if (normalGameEndConditionMet) // AまたはBの条件を満たした場合 (ゲーム決着)
//        {
//            isGameFinished = true; // ゲーム終了フラグを立てる

//            Debug.Log($"--- ▼▼▼ 勝敗判定結果 ▼▼▼ ---");
//            // まず、表面上の勝利メッセージを表示
//            Debug.Log($"判定: ゲーム終了 -> {normalWinMessage}");
//            // ただし、この後「妖狐」の判定がある
//            yield return StartCoroutine(ShowResultScreen(normalWinMessage, false)); // 一度、通常の勝利画面を表示し、画面を明るく戻す

//            yield return new WaitForSeconds(2.0f); // プレイヤーが結果を認識する時間

//            if (foxCount > 0)
//            {
//                // しかし、妖狐が生き残っていた場合、勝利を横取り！
//                Debug.Log("...しかし、妖狐が生き残っていた！妖狐も勝利！");
//                yield return StartCoroutine(ShowResultScreen("FOX WINS!", true)); // 再び暗転し、真の勝者を表示
//            }
//            Debug.Log("--- ▲▲▲ 勝敗判定結果 ▲▲▲ ---");
//        }
//        else // ゲームがまだ続く場合
//        {
//            Debug.Log("--- ▼▼▼ 勝敗判定結果 ▼▼▼ ---");
//            Debug.Log("判定: ゲーム続行");
//            Debug.Log("--- ▲▲▲ 勝敗判定結果 ▲▲▲ ---");

//            if (currentPhase == GamePhase.AfterNight)
//            {
//                if (killData != null) { yield return StartCoroutine(ShowReactionsLog(killData.kill_reactions, killData.sus_reactions)); }
//                ShowDropdownPanel();
//            }
//            else
//            {
//                yield return StartCoroutine(ShowResultScreen("CONTINUE", false));
//                StartCoroutine(FadeAndKill());
//            }
//        }
//    }

//    IEnumerator ShowResultScreen(string message, bool isGameOver)
//    {
//        float duration = 1f;
//        float t = 0f;
//        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(0, 1, t / duration)); yield return null; }

//        if (winText != null) { winText.gameObject.SetActive(true); winText.text = message; }

//        float waitTime = isGameOver ? 4.0f : 2.0f;
//        yield return new WaitForSeconds(waitTime);

//        t = 0f;
//        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(1, 0, t / duration)); yield return null; }

//        if (!isGameOver) { winText.gameObject.SetActive(false); }
//    }


//    // 襲撃後のリアクションと考察をログ形式で表示する
//    IEnumerator ShowReactionsLog(Dictionary<string, string> killReactions, Dictionary<string, string> susReactions)
//    {
//        // 表示すべきデータが何もなければ終了
//        if (killReactions == null && susReactions == null) yield break;

//        Debug.Log("リアクションログの表示を開始します。");
//        logPanel.SetActive(true);
//        logOpenButton.SetActive(true); // ボタンを表示する
//        foreach (Transform child in logContent) { Destroy(child.gameObject); } // ログをクリア
//        logContent.anchoredPosition = Vector2.zero;

//        // --- 1. 襲撃へのリアクションを表示 ---
//        if (killReactions != null)
//        {
//            foreach (var entry in killReactions)
//            {
//                if (personDataDict.ContainsKey(entry.Key) && !string.IsNullOrEmpty(entry.Value))
//                {
//                    Debug.Log("--- ▼▼▼ Kill Reactions (襲撃への反応) ▼▼▼ ---");
//                    Debug.Log($"[Kill Reaction] {entry.Key}: {entry.Value}");
//                    GameObject messageInstance = Instantiate(logMessagePrefab, logContent);
//                    TextMeshProUGUI messageText = messageInstance.GetComponentInChildren<TextMeshProUGUI>();
//                    if (messageText != null)
//                    {
//                        // 例: あかね: あああ、神様...
//                        messageText.text = $"<color=yellow>{entry.Key}:</color> {entry.Value}";
//                    }
//                    yield return new WaitForSeconds(1.5f);
//                }
//            }
//        }

//        // --- 2. 考察パートへの区切り線を表示 ---
//        yield return new WaitForSeconds(1.0f);
//        GameObject separatorInstance = Instantiate(logMessagePrefab, logContent);
//        TextMeshProUGUI separatorText = separatorInstance.GetComponentInChildren<TextMeshProUGUI>();
//        if (separatorText != null)
//        {
//            separatorText.text = "--- みんなの考察 ---";
//            separatorText.alignment = TextAlignmentOptions.Center; // 中央揃えにする
//        }
//        yield return new WaitForSeconds(2.0f);


//        // --- 3. 誰が怪しいかの考察を表示 ---
//        if (susReactions != null)
//        {
//            Debug.Log("--- ▼▼▼ Suspect Reactions (考察) ▼▼▼ ---");
//            foreach (var entry in susReactions)
//            {
//                if (personDataDict.ContainsKey(entry.Key) && !string.IsNullOrEmpty(entry.Value))
//                {
//                    Debug.Log($"[Sus Reaction] {entry.Key}: {entry.Value}");
//                    GameObject messageInstance = Instantiate(logMessagePrefab, logContent);
//                    TextMeshProUGUI messageText = messageInstance.GetComponentInChildren<TextMeshProUGUI>();
//                    if (messageText != null)
//                    {
//                        // 考察は色を変えると見やすいかもしれません
//                        messageText.text = $"<color=blue>{entry.Key}:</color> {entry.Value}";
//                    }
//                    yield return new WaitForSeconds(1.5f);
//                }
//            }
//        }


//        logPanel.SetActive(false); // ログパネルは閉じておく
//    }

//    void ShowDropdownPanel()
//    {
//        if (logPanel != null) logPanel.SetActive(false);
//        if (logOpenButton != null) logOpenButton.SetActive(true);
//        if (dropdownPanel != null) dropdownPanel.SetActive(true);
//        if (aliveDropdown != null)
//        {
//            aliveDropdown.ClearOptions();
//            aliveDropdown.AddOptions(new List<string>(personDataDict.Keys));
//            aliveDropdown.onValueChanged.RemoveAllListeners();
//            aliveDropdown.onValueChanged.AddListener(delegate { OnDropdownValueChanged(); });
//        }
//        if (selectButton != null) { selectButton.onClick.RemoveAllListeners(); selectButton.onClick.AddListener(OnSelect); }
//    }

//    public void ToggleLogPanel()
//    {
//        if (logPanel != null)
//        {
//            // logPanelが現在アクティブかどうかの逆の状態をセットする
//            bool isActive = logPanel.activeSelf;
//            logPanel.SetActive(!isActive);
//        }
//    }

//    public void OnSelect()
//    {
//        string selectedName = aliveDropdown.options[aliveDropdown.value].text;
//        StartCoroutine(ProcessVoteAndKill(selectedName));
//    }

//    public void OnDropdownValueChanged() { StartCoroutine(RefreshUIPanel()); }

//    IEnumerator RefreshUIPanel()
//    {
//        dropdownPanel.SetActive(false);
//        yield return null;
//        dropdownPanel.SetActive(true);
//    }

//    // ■■■ 4. データ構造定義 ■■■

//    // 役職データを受け取るためのクラス
//    [System.Serializable]
//    public class RoleData { public bool alive; public string role; }

//    // /kill APIのレスポンス全体を受け取るためのクラス
//    public class FullKillData
//    {
//        // victimを string から List<string> に変更
//        public List<string> victim;

//        public List<string> alive;
//        public Dictionary<string, string> kill_reactions;


//        public Dictionary<string, string> sus_reactions;
//        public int bread_num;
//        public string die_role;
//        public string divine_role;
//    }
//}