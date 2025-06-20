using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json; // Newtonsoft.Json���C�u�������g�p����錾

public class Wolf : MonoBehaviour
{
    // ������ �t�B�[���h��` ������

    [Header("��{�ݒ�")]
    public GameObject[] spheres;

    [Header("���o�pUI")]
    public Image fadePanel;
    public TextMeshPro winText;

    [Header("���[�pUI")]
    public GameObject dropdownPanel;
    public TMP_Dropdown aliveDropdown;
    public Button selectButton;

    [Header("���OUI")]
    public GameObject logPanel;
    public RectTransform logContent;
    public GameObject logMessagePrefab;

    private Dictionary<string, PersonData> personDataDict = new Dictionary<string, PersonData>();
    private enum GamePhase { AfterNight, AfterVote }
    private bool isGameFinished = false; // �Q�[�����I�����������Ǘ�����t���O

    // ������ 1. Unity�̏������E�X�V���� ������

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
        if (isGameFinished) return; // �Q�[���I����̓L�[���͂𖳌��ɂ���

        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
        {
            Debug.Log("Enter�L�[��������܂��� �� ��̃^�[�����J�n���܂�");
            StartCoroutine(FadeAndKill());
        }
    }

    // ������ 2. ���C���̃Q�[���t���[�i�s ������

    IEnumerator InitializeFromStartAPI()
    {
        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:5000/start");
        yield return request.SendWebRequest();
        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("start API�擾���s: " + request.error); yield break; }

        // Newtonsoft.Json���g���AJSON�𒼐ځu���O�Ɩ�E�f�[�^�̎����v�ɕϊ�
        var roleDict = JsonConvert.DeserializeObject<Dictionary<string, RoleData>>(request.downloadHandler.text);

        int i = 0;
        foreach (var entry in roleDict) // �����JSON���̑S�L�����N�^�[�����[�v�ł���
        {
            if (i >= spheres.Length) break;
            GameObject sphere = spheres[i];
            PersonData pd = sphere.GetComponent<PersonData>();
            if (pd != null)
            {
                pd.personName = entry.Key; // entry.Key�� "������", "����" �Ȃǂ̖��O�ɂȂ�
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
        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("kill API�擾���s: " + request.error); yield break; }

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
        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("vote_kill API���M���s: " + request.error); }

        if (personDataDict.ContainsKey(name)) { Destroy(personDataDict[name].gameObject); personDataDict.Remove(name); }

        yield return new WaitForSeconds(0.5f);

        t = 0f;
        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(1, 0, t / duration)); yield return null; }

        StartCoroutine(CheckForVictory(GamePhase.AfterVote, null));
    }

    // ������ 3. ���ʏ����i��������EUI����j ������

    IEnumerator CheckForVictory(GamePhase currentPhase, FullKillData killData)
    {
        UnityWebRequest checkRequest = UnityWebRequest.Get("http://127.0.0.1:5000/start");
        yield return checkRequest.SendWebRequest();
        if (checkRequest.result != UnityWebRequest.Result.Success) { Debug.LogError("start API�Ď擾���s: " + checkRequest.error); yield break; }

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

    // ������ 4. �f�[�^�\����` ������

    // ��E�f�[�^���󂯎�邽�߂̃N���X
    [System.Serializable]
    public class RoleData { public bool alive; public string role; }

    // /kill API�̃��X�|���X�S�̂��󂯎�邽�߂̃N���X
    public class FullKillData
    {
        // victim�� string ���� List<string> �ɕύX
        public List<string> victim;

        public List<string> alive;
        public Dictionary<string, string> kill_reactions;

        // Python���Œǉ����ꂽ�V�������ڂ��A���łɒ�`���Ă����Ə����֗��ł�
        public Dictionary<string, string> sus_reactions;
        public int bread_num;
        public string die_role;
        public string divine_role;
    }
}