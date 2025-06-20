using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json; // Newtonsoft.Jsonライブラリを使用する宣言

public class Wolf : MonoBehaviour
{
    // ■■■ フィールド定義 ■■■

    [Header("基本設定")]
    public GameObject[] spheres;

    [Header("演出用UI")]
    public Image fadePanel;
    public TextMeshPro winText;

    [Header("投票用UI")]
    public GameObject dropdownPanel;
    public TMP_Dropdown aliveDropdown;
    public Button selectButton;

    [Header("ログUI")]
    public GameObject logPanel;
    public RectTransform logContent;
    public GameObject logMessagePrefab;

    private Dictionary<string, PersonData> personDataDict = new Dictionary<string, PersonData>();
    private enum GamePhase { AfterNight, AfterVote }
    private bool isGameFinished = false; // ゲームが終了したかを管理するフラグ

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
        if (isGameFinished) return; // ゲーム終了後はキー入力を無効にする

        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
        {
            Debug.Log("Enterキーが押されました → 夜のターンを開始します");
            StartCoroutine(FadeAndKill());
        }
    }

    // ■■■ 2. メインのゲームフロー進行 ■■■

    IEnumerator InitializeFromStartAPI()
    {
        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:5000/start");
        yield return request.SendWebRequest();
        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("start API取得失敗: " + request.error); yield break; }

        // Newtonsoft.Jsonを使い、JSONを直接「名前と役職データの辞書」に変換
        var roleDict = JsonConvert.DeserializeObject<Dictionary<string, RoleData>>(request.downloadHandler.text);

        int i = 0;
        foreach (var entry in roleDict) // これでJSON内の全キャラクターをループできる
        {
            if (i >= spheres.Length) break;
            GameObject sphere = spheres[i];
            PersonData pd = sphere.GetComponent<PersonData>();
            if (pd != null)
            {
                pd.personName = entry.Key; // entry.Keyが "あかね", "けんた" などの名前になる
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

        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:5000/kill");
        yield return request.SendWebRequest();
        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("kill API取得失敗: " + request.error); yield break; }

        var fullKillData = JsonConvert.DeserializeObject<FullKillData>(request.downloadHandler.text);

        List<string> toRemove = new List<string>();
        foreach (var entry in personDataDict)
        {
            if (!fullKillData.alive.Contains(entry.Key)) { Destroy(entry.Value.gameObject); toRemove.Add(entry.Key); }
        }
        foreach (string name in toRemove) { personDataDict.Remove(name); }

        yield return new WaitForSeconds(0.5f);

        t = 0f;
        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(1, 0, t / duration)); yield return null; }

        StartCoroutine(CheckForVictory(GamePhase.AfterNight, fullKillData));
    }

    IEnumerator ProcessVoteAndKill(string name)
    {
        dropdownPanel.SetActive(false);
        float duration = 1f;
        float t = 0f;
        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(0, 1, t / duration)); yield return null; }

        string url = $"http://127.0.0.1:5000/vote_kill?name={UnityWebRequest.EscapeURL(name)}";
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

    IEnumerator CheckForVictory(GamePhase currentPhase, FullKillData killData)
    {
        UnityWebRequest checkRequest = UnityWebRequest.Get("http://127.0.0.1:5000/start");
        yield return checkRequest.SendWebRequest();
        if (checkRequest.result != UnityWebRequest.Result.Success) { Debug.LogError("start API再取得失敗: " + checkRequest.error); yield break; }

        var roleDict = JsonConvert.DeserializeObject<Dictionary<string, RoleData>>(checkRequest.downloadHandler.text);

        int werewolfCount = 0;
        int nonWerewolfCount = 0;
        foreach (var name in personDataDict.Keys)
        {
            if (roleDict.ContainsKey(name)) { if (roleDict[name].role == "WEREWOLF") werewolfCount++; else nonWerewolfCount++; }
        }

        string resultMessage = null;
        bool isGameOver = true;
        if (werewolfCount == 0) { resultMessage = "VILLAGER WIN"; }
        else if (werewolfCount >= nonWerewolfCount) { resultMessage = "WEREWOLF WIN"; }
        else { isGameOver = false; }

        if (isGameOver)
        {
            isGameFinished = true;
            yield return StartCoroutine(ShowResultScreen(resultMessage, true));
        }
        else
        {
            if (currentPhase == GamePhase.AfterNight)
            {
                if (killData != null) { yield return StartCoroutine(ShowKillReactions(killData.kill_reactions)); }
                ShowDropdownPanel();
            }
            else
            {
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

    IEnumerator ShowKillReactions(Dictionary<string, string> reactionDict)
    {
        if (reactionDict == null) yield break;

        logPanel.SetActive(true);
        foreach (Transform child in logContent) { Destroy(child.gameObject); }
        logContent.anchoredPosition = Vector2.zero;

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

    // 役職データを受け取るためのクラス
    [System.Serializable]
    public class RoleData { public bool alive; public string role; }

    // /kill APIのレスポンス全体を受け取るためのクラス
    public class FullKillData
    {
        // victimを string から List<string> に変更
        public List<string> victim;

        public List<string> alive;
        public Dictionary<string, string> kill_reactions;

        // Python側で追加された新しい項目も、ついでに定義しておくと将来便利です
        public Dictionary<string, string> sus_reactions;
        public int bread_num;
        public string die_role;
        public string divine_role;
    }
}