using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using System.Collections.Generic;

public class Wolf : MonoBehaviour
{
    // ■■■ フィールド定義 ■■■

    [Header("基本設定")]
    public GameObject[] spheres; // キャラクターオブジェクトの配列

    [Header("演出用UI")]
    public Image fadePanel;      // 画面暗転用のパネル
    public TextMeshPro winText;  // 勝敗結果表示用のテキスト

    [Header("投票用UI")]
    public GameObject dropdownPanel;    // 投票UI全体の親オブジェクト
    public TMP_Dropdown aliveDropdown;  // 生存者を表示するドロップダウン
    public Button selectButton;         // 投票決定ボタン

    [Header("ログUI")]
    public GameObject logPanel;         // ログUI全体の親オブジェクト
    public RectTransform logContent;    // ScrollViewの中の Content オブジェクト
    public GameObject logMessagePrefab; // ログ1行分のプレハブ

    // 内部でキャラクターデータを管理するための辞書
    private Dictionary<string, PersonData> personDataDict = new Dictionary<string, PersonData>();

    // ゲームのどのフェーズかを判定するためのEnum（列挙型）
    private enum GamePhase { AfterNight, AfterVote }


    // ■■■ 1. Unityの初期化・更新処理 ■■■

    void Start()
    {
        StartCoroutine(InitializeFromStartAPI());
        if (fadePanel != null) fadePanel.color = new Color(0, 0, 0, 0);
        if (winText != null) winText.gameObject.SetActive(false);
        if (dropdownPanel != null) dropdownPanel.SetActive(false);
        if (logPanel != null) logPanel.SetActive(false);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
        {
            Debug.Log("Enterキーが押されました → 夜のターンを開始します");
            StartCoroutine(FadeAndKill());
        }
    }

    // ■■■ 2. メインのゲームフロー進行 ■■■

    IEnumerator InitializeFromStartAPI()
    {
        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:9000/start");
        yield return request.SendWebRequest();
        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("start API取得失敗: " + request.error); yield break; }

        RoleWrapper roles = JsonUtility.FromJson<RoleWrapper>(request.downloadHandler.text);
        Dictionary<string, RoleData> roleDict = roles.ToDictionary();
        int i = 0;
        foreach (var entry in roleDict)
        {
            if (i >= spheres.Length) break;
            GameObject sphere = spheres[i];
            PersonData pd = sphere.GetComponent<PersonData>();
            if (pd != null)
            {
                pd.personName = entry.Key;
                pd.textDisplay.text = entry.Key;
                personDataDict[entry.Key] = pd;
            }
            i++;
        }
    }

    IEnumerator FadeAndKill()
    {
        float duration = 1f;
        float t = 0f;
        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(0, 1, t / duration)); yield return null; }

        yield return new WaitForSeconds(0.5f);

        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:9000/kill");
        yield return request.SendWebRequest();
        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("kill API取得失敗: " + request.error); yield break; }

        KillData killData = JsonUtility.FromJson<KillData>(request.downloadHandler.text);
        List<string> toRemove = new List<string>();
        foreach (var entry in personDataDict)
        {
            if (!killData.alive.Contains(entry.Key)) { Destroy(entry.Value.gameObject); toRemove.Add(entry.Key); }
        }
        foreach (string name in toRemove) { personDataDict.Remove(name); }

        yield return new WaitForSeconds(0.5f);

        t = 0f;
        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(1, 0, t / duration)); yield return null; }

        StartCoroutine(CheckForVictory(GamePhase.AfterNight, killData));
    }

    IEnumerator ProcessVoteAndKill(string name)
    {
        dropdownPanel.SetActive(false);
        float duration = 1f;
        float t = 0f;
        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(0, 1, t / duration)); yield return null; }

        string url = $"http://127.0.0.1:9000/vote_kill?name={UnityWebRequest.EscapeURL(name)}";
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();
        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("vote_kill API送信失敗: " + request.error); }

        if (personDataDict.ContainsKey(name)) { Destroy(personDataDict[name].gameObject); personDataDict.Remove(name); }

        yield return new WaitForSeconds(0.5f);

        t = 0f;
        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(1, 0, t / duration)); yield return null; }

        StartCoroutine(CheckForVictory(GamePhase.AfterVote, null));
    }

    // ■■■ 3. 共通処理（勝利判定・UI操作） ■■■

    IEnumerator CheckForVictory(GamePhase currentPhase, KillData killData)
    {
        Debug.Log("勝利判定を開始します。");
        UnityWebRequest checkRequest = UnityWebRequest.Get("http://127.0.0.1:9000/start");
        yield return checkRequest.SendWebRequest();
        if (checkRequest.result != UnityWebRequest.Result.Success) { Debug.LogError("start API再取得失敗: " + checkRequest.error); yield break; }

        RoleWrapper roles = JsonUtility.FromJson<RoleWrapper>(checkRequest.downloadHandler.text);
        Dictionary<string, RoleData> roleDict = roles.ToDictionary();
        int werewolfCount = 0;
        int nonWerewolfCount = 0;
        foreach (var name in personDataDict.Keys)
        {
            if (roleDict.ContainsKey(name)) { if (roleDict[name].role == "WEREWOLF") werewolfCount++; else nonWerewolfCount++; }
        }
        Debug.Log($"生存者カウント: 人狼={werewolfCount}, 村人側={nonWerewolfCount}");

        string resultMessage = null;
        bool isGameOver = true;
        if (werewolfCount == 0) { resultMessage = "VILLAGER WIN"; }
        else if (werewolfCount >= nonWerewolfCount) { resultMessage = "WEREWOLF WIN"; }
        else { isGameOver = false; }

        if (isGameOver)
        {
            yield return StartCoroutine(ShowResultScreen(resultMessage, true));
        }
        else
        {
            if (currentPhase == GamePhase.AfterNight)
            {
                Debug.Log("ゲームは続行します。リアクション表示の後、投票へ。");
                if (killData != null) { yield return StartCoroutine(ShowKillReactions(killData.kill_reactions)); }
                ShowDropdownPanel();
            }
            else // AfterVote
            {
                Debug.Log("ゲームは続行します。次の夜へ。");
                yield return StartCoroutine(ShowResultScreen("CONTINUE", false));
                StartCoroutine(FadeAndKill());
            }
        }
    }

    IEnumerator ShowResultScreen(string message, bool isGameOver)
    {
        float duration = 1f;
        float t = 0f;
        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(0, 1, t / duration)); yield return null; }

        if (winText != null) { winText.gameObject.SetActive(true); winText.text = message; }

        float waitTime = isGameOver ? 4.0f : 2.0f;
        yield return new WaitForSeconds(waitTime);

        t = 0f;
        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(1, 0, t / duration)); yield return null; }

        if (!isGameOver) { winText.gameObject.SetActive(false); }
    }

    IEnumerator ShowKillReactions(KillReactionsData reactions)
    {
        Debug.Log("ShowKillReactions コルーチンが開始されました。");
        if (logPanel == null)
        {
            Debug.LogError("logPanelが設定されていません！");
            yield break;
        }
        Debug.Log("logPanelをアクティブにします。");
        if (reactions == null) yield break;
        Debug.Log("襲撃後のリアクションをログに表示します。");

        logPanel.SetActive(true);
        foreach (Transform child in logContent) { Destroy(child.gameObject); }
        logContent.anchoredPosition = Vector2.zero;

        Dictionary<string, string> reactionDict = new Dictionary<string, string>
        {
            { "GPT2", reactions.GPT2 }, { "llama3", reactions.llama3 }, { "tinyllama", reactions.tinyllama },
            { "DeepSeek", reactions.DeepSeek }, { "gemma", reactions.gemma }
        };

        foreach (var entry in reactionDict)
        {
            if (personDataDict.ContainsKey(entry.Key) && !string.IsNullOrEmpty(entry.Value))
            {
                GameObject messageInstance = Instantiate(logMessagePrefab, logContent);
                TextMeshProUGUI messageText = messageInstance.GetComponentInChildren<TextMeshProUGUI>();
                if (messageText != null) { messageText.text = $"<color=yellow>{entry.Key}:</color> {entry.Value}"; }
                yield return new WaitForSeconds(1.5f);
            }
        }

        yield return new WaitForSeconds(5.0f);
        logPanel.SetActive(false);
    }

    void ShowDropdownPanel()
    {
        if (dropdownPanel != null) dropdownPanel.SetActive(true);
        if (aliveDropdown != null)
        {
            aliveDropdown.ClearOptions();
            aliveDropdown.AddOptions(new List<string>(personDataDict.Keys));
            aliveDropdown.onValueChanged.RemoveAllListeners();
            aliveDropdown.onValueChanged.AddListener(delegate { OnDropdownValueChanged(); });
        }
        if (selectButton != null) { selectButton.onClick.RemoveAllListeners(); selectButton.onClick.AddListener(OnSelect); }
    }

    public void OnSelect()
    {
        string selectedName = aliveDropdown.options[aliveDropdown.value].text;
        StartCoroutine(ProcessVoteAndKill(selectedName));
    }

    public void OnDropdownValueChanged() { StartCoroutine(RefreshUIPanel()); }

    IEnumerator RefreshUIPanel()
    {
        dropdownPanel.SetActive(false);
        yield return null;
        dropdownPanel.SetActive(true);
    }

    // ■■■ 4. データ構造定義 ■■■

    [System.Serializable]
    public class KillReactionsData { public string GPT2, llama3, tinyllama, DeepSeek, gemma; }

    [System.Serializable]
    public class RoleData { public bool alive; public string role; }

    [System.Serializable]
    public class RoleWrapper
    {
        public RoleData DeepSeek, GPT2, Mistral, gemma, llama3, tinyllama;
        public Dictionary<string, RoleData> ToDictionary()
        {
            return new Dictionary<string, RoleData>
            {
                { "DeepSeek", DeepSeek }, { "GPT2", GPT2 }, { "Mistral", Mistral },
                { "gemma", gemma }, { "llama3", llama3 }, { "tinyllama", tinyllama }
            };
        }
    }

    [System.Serializable]
    public class KillData { public string victim; public List<string> alive; public KillReactionsData kill_reactions; }
}