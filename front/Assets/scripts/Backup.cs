//using UnityEngine;
//using UnityEngine.Networking;
//using UnityEngine.UI;
//using TMPro;
//using System.Collections;
//using System.Collections.Generic;
//using Newtonsoft.Json; // Newtonsoft.Json���C�u�������g�p����錾

//public class Wolf : MonoBehaviour
//{
//    // ������ �t�B�[���h��` ������

//    [Header("��{�ݒ�")]
//    public GameObject[] spheres;

//    [Header("���o�pUI")]
//    public Image fadePanel;
//    public TextMeshPro winText;

//    [Header("���[�pUI")]
//    public GameObject dropdownPanel;
//    public TMP_Dropdown aliveDropdown;
//    public Button selectButton;

//    [Header("���OUI")]
//    public GameObject logPanel;
//    public RectTransform logContent;
//    public GameObject logMessagePrefab;
//    public GameObject logOpenButton; // ���O���J���{�^��

//    private Dictionary<string, PersonData> personDataDict = new Dictionary<string, PersonData>();

//    // �Q�[���J�n���̑S�L�����N�^�[�̖�E����ێ����邽�߂̎���
//    private Dictionary<string, RoleData> fullRoleData;
//    private enum GamePhase { AfterNight, AfterVote }
//    private bool isGameFinished = false; // �Q�[�����I�����������Ǘ�����t���O

//    // ������ 1. Unity�̏������E�X�V���� ������

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
//        if (isGameFinished) return; // �Q�[���I����̓L�[���͂𖳌��ɂ���

//        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
//        {
//            Debug.Log("Enter�L�[��������܂��� �� ��̃^�[�����J�n���܂�");
//            StartCoroutine(FadeAndKill());
//        }
//    }

//    // ������ 2. ���C���̃Q�[���t���[�i�s ������

//    IEnumerator InitializeFromStartAPI()
//    {
//        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:5000/start");
//        yield return request.SendWebRequest();
//        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("start API�擾���s: " + request.error); yield break; }

//        // Newtonsoft.Json���g���AJSON�𒼐ځu���O�Ɩ�E�f�[�^�̎����v�ɕϊ�
//        var roleDict = JsonConvert.DeserializeObject<Dictionary<string, RoleData>>(request.downloadHandler.text);

//        this.fullRoleData = roleDict; // �擾������E�����N���X�̃t�B�[���h�ɕۑ�����

//        Debug.Log("---  �Q�[���J�n: /start API ���� ---");
//        foreach (var roleEntry in roleDict)
//        {
//            Debug.Log($"�L�����N�^�[: {roleEntry.Key}, ��E: {roleEntry.Value.role}");
//        }
//        Debug.Log("---  �Q�[���J�n: /start API ����  ---");

//        int i = 0;
//        foreach (var entry in roleDict) // �����JSON���̑S�L�����N�^�[�����[�v�ł���
//        {
//            if (i >= spheres.Length) break;
//            GameObject sphere = spheres[i];
//            PersonData pd = sphere.GetComponent<PersonData>();
//            if (pd != null)
//            {
//                pd.personName = entry.Key; // entry.Key�� "������", "����" �Ȃǂ̖��O�ɂȂ�
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
//        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("kill API�擾���s: " + request.error); yield break; }

//        var fullKillData = JsonConvert.DeserializeObject<FullKillData>(request.downloadHandler.text);

//        Debug.Log("---  ��̃^�[������ (/kill API)  ---");
//        if (fullKillData.victim != null && fullKillData.victim.Count > 0)
//        {
//            // �]���҂Ƃ��̖�E��\��
//            Debug.Log($"�]����: {fullKillData.victim[0]} ({fullKillData.die_role})");
//        }
//        else
//        {
//            Debug.Log("�]���҂͂��܂���ł����B");
//        }
//        // �肢�t��p�����̌��ʂ��\��
//        Debug.Log($"�肢����: {fullKillData.divine_role}");
//        Debug.Log($"�p���z�z���(�p���̐�): {fullKillData.bread_num}");

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
//        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("vote_kill API���M���s: " + request.error); }

//        if (personDataDict.ContainsKey(name)) { Destroy(personDataDict[name].gameObject); personDataDict.Remove(name); }

//        yield return new WaitForSeconds(0.5f);

//        t = 0f;
//        while (t < duration) { t += Time.deltaTime; fadePanel.color = new Color(0, 0, 0, Mathf.Lerp(1, 0, t / duration)); yield return null; }

//        StartCoroutine(CheckForVictory(GamePhase.AfterVote, null));
//    }

//    // ������ 3. ���ʏ����i��������EUI����j ������

//    IEnumerator CheckForVictory(GamePhase currentPhase, FullKillData killData)
//    {
//        var roleDict = this.fullRoleData;
//        if (roleDict == null)
//        {
//            Debug.LogError("��E�f�[�^������������Ă��܂���I");
//            yield break;
//        }

//        // --- 1. �����҂�3�̐w�c�ɕ����ăJ�E���g ---
//        int werewolfTeamCount = 0; // �l�T(WEREWOLF) + ���l(MADMAN)
//        int villagerTeamCount = 0; // ���l�A�R�m�A�肢�t�Ȃǂ̑��l�w�c
//        int foxCount = 0;          // �d��(FOX)
//        int pureWerewolfCount = 0; // ���l��������̂��߂́A�����Ȑl�T�̐�

//        Debug.Log($"--- ������ {currentPhase}��̐����ҏ󋵊m�F ������ ---");
//        foreach (var name in personDataDict.Keys)
//        {
//            if (roleDict.ContainsKey(name))
//            {
//                string role = roleDict[name].role.ToUpper();
//                Debug.Log($"������: {name}, ��E: {role}");

//                if (role == "WEREWOLF") { werewolfTeamCount++; pureWerewolfCount++; }
//                else if (role == "MADMAN") { werewolfTeamCount++; }
//                else if (role == "FOX") { foxCount++; }
//                else { villagerTeamCount++; }
//            }
//        }
//        Debug.Log($"--- ������ {currentPhase}��̐����ҏ󋵊m�F ������ ---");
//        Debug.Log($"�����҃J�E���g: �l�T�w�c={werewolfTeamCount}, ���l�w�c={villagerTeamCount}, �d��={foxCount}");

//        // --- 2. �܂��A���l���l�T�̏��������𖞂����Ă��邩���� ---
//        string normalWinMessage = null;
//        bool normalGameEndConditionMet = false;

//        // a. ���l���������F�l�T���S�ł��Ă��邩�H
//        if (pureWerewolfCount == 0)
//        {
//            normalWinMessage = "VILLAGER WIN";
//            normalGameEndConditionMet = true;
//        }
//        // b. �l�T�w�c���������F�l�T�w�c�̐����A���l�w�c�̐��ȏ�ɂȂ������H (�d�ς͐��Ɋ܂߂Ȃ�)
//        else if (werewolfTeamCount >= villagerTeamCount)
//        {
//            normalWinMessage = "WEREWOLF WIN";
//            normalGameEndConditionMet = true;
//        }

//        // --- 3. �ŏI�I�ȏ��҂����肵�A�Q�[�����I���܂��͑��s���� ---
//        if (normalGameEndConditionMet) // A�܂���B�̏����𖞂������ꍇ (�Q�[������)
//        {
//            isGameFinished = true; // �Q�[���I���t���O�𗧂Ă�

//            Debug.Log($"--- ������ ���s���茋�� ������ ---");
//            // �܂��A�\�ʏ�̏������b�Z�[�W��\��
//            Debug.Log($"����: �Q�[���I�� -> {normalWinMessage}");
//            // �������A���̌�u�d�ρv�̔��肪����
//            yield return StartCoroutine(ShowResultScreen(normalWinMessage, false)); // ��x�A�ʏ�̏�����ʂ�\�����A��ʂ𖾂邭�߂�

//            yield return new WaitForSeconds(2.0f); // �v���C���[�����ʂ�F�����鎞��

//            if (foxCount > 0)
//            {
//                // �������A�d�ς������c���Ă����ꍇ�A�����������I
//                Debug.Log("...�������A�d�ς������c���Ă����I�d�ς������I");
//                yield return StartCoroutine(ShowResultScreen("FOX WINS!", true)); // �ĂшÓ]���A�^�̏��҂�\��
//            }
//            Debug.Log("--- ������ ���s���茋�� ������ ---");
//        }
//        else // �Q�[�����܂������ꍇ
//        {
//            Debug.Log("--- ������ ���s���茋�� ������ ---");
//            Debug.Log("����: �Q�[�����s");
//            Debug.Log("--- ������ ���s���茋�� ������ ---");

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


//    // �P����̃��A�N�V�����ƍl�@�����O�`���ŕ\������
//    IEnumerator ShowReactionsLog(Dictionary<string, string> killReactions, Dictionary<string, string> susReactions)
//    {
//        // �\�����ׂ��f�[�^�������Ȃ���ΏI��
//        if (killReactions == null && susReactions == null) yield break;

//        Debug.Log("���A�N�V�������O�̕\�����J�n���܂��B");
//        logPanel.SetActive(true);
//        logOpenButton.SetActive(true); // �{�^����\������
//        foreach (Transform child in logContent) { Destroy(child.gameObject); } // ���O���N���A
//        logContent.anchoredPosition = Vector2.zero;

//        // --- 1. �P���ւ̃��A�N�V������\�� ---
//        if (killReactions != null)
//        {
//            foreach (var entry in killReactions)
//            {
//                if (personDataDict.ContainsKey(entry.Key) && !string.IsNullOrEmpty(entry.Value))
//                {
//                    Debug.Log("--- ������ Kill Reactions (�P���ւ̔���) ������ ---");
//                    Debug.Log($"[Kill Reaction] {entry.Key}: {entry.Value}");
//                    GameObject messageInstance = Instantiate(logMessagePrefab, logContent);
//                    TextMeshProUGUI messageText = messageInstance.GetComponentInChildren<TextMeshProUGUI>();
//                    if (messageText != null)
//                    {
//                        // ��: ������: �������A�_�l...
//                        messageText.text = $"<color=yellow>{entry.Key}:</color> {entry.Value}";
//                    }
//                    yield return new WaitForSeconds(1.5f);
//                }
//            }
//        }

//        // --- 2. �l�@�p�[�g�ւ̋�؂����\�� ---
//        yield return new WaitForSeconds(1.0f);
//        GameObject separatorInstance = Instantiate(logMessagePrefab, logContent);
//        TextMeshProUGUI separatorText = separatorInstance.GetComponentInChildren<TextMeshProUGUI>();
//        if (separatorText != null)
//        {
//            separatorText.text = "--- �݂�Ȃ̍l�@ ---";
//            separatorText.alignment = TextAlignmentOptions.Center; // ���������ɂ���
//        }
//        yield return new WaitForSeconds(2.0f);


//        // --- 3. �N�����������̍l�@��\�� ---
//        if (susReactions != null)
//        {
//            Debug.Log("--- ������ Suspect Reactions (�l�@) ������ ---");
//            foreach (var entry in susReactions)
//            {
//                if (personDataDict.ContainsKey(entry.Key) && !string.IsNullOrEmpty(entry.Value))
//                {
//                    Debug.Log($"[Sus Reaction] {entry.Key}: {entry.Value}");
//                    GameObject messageInstance = Instantiate(logMessagePrefab, logContent);
//                    TextMeshProUGUI messageText = messageInstance.GetComponentInChildren<TextMeshProUGUI>();
//                    if (messageText != null)
//                    {
//                        // �l�@�͐F��ς���ƌ��₷����������܂���
//                        messageText.text = $"<color=blue>{entry.Key}:</color> {entry.Value}";
//                    }
//                    yield return new WaitForSeconds(1.5f);
//                }
//            }
//        }


//        logPanel.SetActive(false); // ���O�p�l���͕��Ă���
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
//            // logPanel�����݃A�N�e�B�u���ǂ����̋t�̏�Ԃ��Z�b�g����
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

//    // ������ 4. �f�[�^�\����` ������

//    // ��E�f�[�^���󂯎�邽�߂̃N���X
//    [System.Serializable]
//    public class RoleData { public bool alive; public string role; }

//    // /kill API�̃��X�|���X�S�̂��󂯎�邽�߂̃N���X
//    public class FullKillData
//    {
//        // victim�� string ���� List<string> �ɕύX
//        public List<string> victim;

//        public List<string> alive;
//        public Dictionary<string, string> kill_reactions;


//        public Dictionary<string, string> sus_reactions;
//        public int bread_num;
//        public string die_role;
//        public string divine_role;
//    }
//}