//using UnityEngine;
//using UnityEngine.Networking;
//using UnityEngine.UI;
//using TMPro;
//using System.Collections;
//using System.Collections.Generic;

//public class Backup : MonoBehaviour
//{
//    // Inspector����ݒ肷��UI�v�f
//    public GameObject[] spheres;
//    public Image fadePanel;
//    public TextMeshPro winText;
//    public GameObject dropdownPanel;
//    public TMP_Dropdown aliveDropdown;
//    public Button selectButton;

//    // �����ŃL�����N�^�[�f�[�^���Ǘ����邽�߂̎���
//    private Dictionary<string, PersonData> personDataDict = new Dictionary<string, PersonData>();

//    // �Q�[���̂ǂ̃t�F�[�Y���𔻒肷�邽�߂�Enum�i�񋓌^�j
//    private enum GamePhase { AfterNight, AfterVote }

//    // ������ 1. Unity�̏������E�X�V���� ������

//    void Start()
//    {
//        // �Q�[���J�n���ɃT�[�o�[����L�����N�^�[�����擾���ď�����
//        StartCoroutine(InitializeFromStartAPI());

//        // UI�v�f�̏�����Ԃ�ݒ�
//        if (fadePanel != null)
//            fadePanel.color = new Color(0, 0, 0, 0); // �����ɂ���

//        if (winText != null)
//            winText.gameObject.SetActive(false); // ��\���ɂ���

//        if (dropdownPanel != null)
//            dropdownPanel.SetActive(false); // ��\���ɂ���
//    }

//    void Update()
//    {
//        // Enter�L�[�������ꂽ��A��̃^�[�����J�n����
//        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
//        {
//            Debug.Log("Enter�L�[��������܂��� �� ��̃^�[�����J�n���܂�");
//            StartCoroutine(FadeAndKill());
//        }
//    }

//    // ������ 2. ���C���̃Q�[���t���[�i�s ������

//    /// <summary>
//    /// �Q�[���J�n����/start API���Ăяo���A�L�����N�^�[������������
//    /// </summary>
//    IEnumerator InitializeFromStartAPI()
//    {
//        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:9000/start");
//        yield return request.SendWebRequest();

//        if (request.result != UnityWebRequest.Result.Success)
//        {
//            Debug.LogError("start API�擾���s: " + request.error);
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

//                Debug.Log($"�o�^: {entry.Key} �� ��E: {entry.Value.role}, ����: {entry.Value.alive}");
//            }
//            i++;
//        }
//    }

//    /// <summary>
//    /// ��̃^�[���B�Ó]���A/kill API�ŋ]���҂��擾���č폜����B
//    /// </summary>
//    IEnumerator FadeAndKill()
//    {
//        // �Ó]�t�F�[�h
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

//        // /kill API �Ăяo��
//        UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:9000/kill");
//        yield return request.SendWebRequest();

//        if (request.result != UnityWebRequest.Result.Success)
//        {
//            Debug.LogError("kill API�擾���s: " + request.error);
//            yield break;
//        }

//        KillData killData = JsonUtility.FromJson<KillData>(request.downloadHandler.text);

//        // �����҃��X�g�Ɋ܂܂�Ă��Ȃ����́i�]���ҁj���폜
//        List<string> aliveList = killData.alive;
//        List<string> toRemove = new List<string>();

//        foreach (var entry in personDataDict)
//        {
//            if (!aliveList.Contains(entry.Key))
//            {
//                Debug.Log($"�폜�Ώ�: {entry.Key}�ialive�Ɋ܂܂�Ă��Ȃ��j");
//                Destroy(entry.Value.gameObject);
//                toRemove.Add(entry.Key);
//            }
//        }
//        foreach (string name in toRemove)
//        {
//            personDataDict.Remove(name);
//        }

//        yield return new WaitForSeconds(0.5f);

//        // �t�F�[�h�߂�
//        t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(1, 0, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        // ���ʂ̏�������R���[�`�����Ăяo���i��̃^�[����ł��邱�Ƃ�`����j
//        StartCoroutine(CheckForVictory(GamePhase.AfterNight));
//    }

//    /// <summary>
//    /// ���[�^�[���B�I�����ꂽ�L�������Ó]��API�ʒm���폜�����]����B
//    /// </summary>
//    IEnumerator ProcessVoteAndKill(string name)
//    {
//        dropdownPanel.SetActive(false);

//        // �Ó]�t�F�[�h
//        float duration = 1f;
//        float t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(0, 1, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        // API�Ăяo��
//        string url = $"http://127.0.0.1:9000/vote_kill?name={UnityWebRequest.EscapeURL(name)}";
//        UnityWebRequest request = UnityWebRequest.Get(url);
//        yield return request.SendWebRequest();
//        if (request.result != UnityWebRequest.Result.Success) { Debug.LogError("vote_kill API���M���s: " + request.error); }
//        else { Debug.Log("vote_kill API����: " + request.downloadHandler.text); }

//        // �I�u�W�F�N�g�̍폜
//        if (personDataDict.ContainsKey(name))
//        {
//            Destroy(personDataDict[name].gameObject);
//            personDataDict.Remove(name);
//        }

//        yield return new WaitForSeconds(0.5f);

//        // �t�F�[�h�߂�
//        t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(1, 0, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        // ���ʂ̏�������R���[�`�����Ăяo���i���[�^�[����ł��邱�Ƃ�`����j
//        StartCoroutine(CheckForVictory(GamePhase.AfterVote));
//    }

//    // ������ 3. ���ʏ����i��������EUI����j ������

//    /// <summary>
//    /// ���������𔻒肵�A�Q�[���̏I���܂��͑��s�����肷�鋤�ʃR���[�`��
//    /// </summary>
//    IEnumerator CheckForVictory(GamePhase currentPhase)
//    {
//        Debug.Log("����������J�n���܂��B");

//        UnityWebRequest checkRequest = UnityWebRequest.Get("http://127.0.0.1:9000/start");
//        yield return checkRequest.SendWebRequest();

//        if (checkRequest.result != UnityWebRequest.Result.Success)
//        {
//            Debug.LogError("start API�Ď擾���s: " + checkRequest.error);
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
//        Debug.Log($"�����҃J�E���g: �l�T={werewolfCount}, ���l��={nonWerewolfCount}");

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
//            isGameOver = false; // �Q�[�����s
//        }

//        if (isGameOver)
//        {
//            // �Q�[���I�����̉��o
//            yield return StartCoroutine(ShowResultScreen(resultMessage, true));
//        }
//        else
//        {
//            // �Q�[�����s���̏���
//            if (currentPhase == GamePhase.AfterNight)
//            {
//                // ��̌�Ȃ瓊�[��
//                Debug.Log("�Q�[���͑��s���܂��B���[�ցB");
//                ShowDropdownPanel();
//            }
//            else // AfterVote
//            {
//                // ���[�̌�Ȃ玟�̖��
//                Debug.Log("�Q�[���͑��s���܂��B���̖�ցB");
//                yield return StartCoroutine(ShowResultScreen("CONTINUE", false));
//                StartCoroutine(FadeAndKill());
//            }
//        }
//    }

//    /// <summary>
//    /// ���ʕ\���p�̉��o�i�Ó]���e�L�X�g�\���j���s�����ʃR���[�`��
//    /// </summary>
//    IEnumerator ShowResultScreen(string message, bool isGameOver)
//    {
//        // --- 1. �Ó] ---
//        float duration = 1f;
//        float t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(0, 1, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        // --- 2. �e�L�X�g�\�� ---
//        if (winText != null)
//        {
//            winText.gameObject.SetActive(true);
//            winText.text = message;
//        }

//        // --- 3. ���ʂ��v���C���[�Ɍ����邽�߂ɑҋ@ ---
//        // �Q�[���I�����͏�������(4�b)�A�p�����͒Z��(2�b)�ɑ҂�
//        float waitTime = isGameOver ? 4.0f : 2.0f;
//        yield return new WaitForSeconds(waitTime);

//        // --- 4. �Ó]��߂� ---
//        // �ȑO��isGameOver��true���Ƃ����ŏ������I���Ă��܂������A
//        // ����͏�ɈÓ]��߂��悤�ɂ��܂��B
//        t = 0f;
//        while (t < duration)
//        {
//            t += Time.deltaTime;
//            float alpha = Mathf.Lerp(1, 0, t / duration);
//            fadePanel.color = new Color(0, 0, 0, alpha);
//            yield return null;
//        }

//        // --- 5. �e�L�X�g�̌㏈�� ---
//        // �Q�[�������s����ꍇ"����"�e�L�X�g���\���ɂ���
//        if (!isGameOver)
//        {
//            winText.gameObject.SetActive(false);
//        }
//        // �Q�[���I�����́A��ʂ����邭�߂�������������b�Z�[�W���\�����ꂽ�܂܂ɂȂ�܂��B
//    }

//    /// <summary>
//    /// ���[�p�̃h���b�v�_�E���p�l����\������
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

//            // �h���b�v�_�E�������̃{�^���s��΍�
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
//    /// ���[�{�^���������ꂽ�Ƃ��ɌĂ΂��
//    /// </summary>
//    public void OnSelect()
//    {
//        string selectedName = aliveDropdown.options[aliveDropdown.value].text;
//        Debug.Log($"�I�����ꂽ�L����: {selectedName}");
//        StartCoroutine(ProcessVoteAndKill(selectedName));
//    }

//    /// <summary>
//    /// �h���b�v�_�E���̒l���ύX���ꂽ�Ƃ��ɌĂ΂�AUI�̏�Ԃ����t���b�V������
//    /// </summary>
//    public void OnDropdownValueChanged()
//    {
//        Debug.Log("�h���b�v�_�E���̒l���ύX����܂����BUI�����t���b�V�����܂��B");
//        StartCoroutine(RefreshUIPanel());
//    }

//    IEnumerator RefreshUIPanel()
//    {
//        dropdownPanel.SetActive(false);
//        yield return null;
//        dropdownPanel.SetActive(true);
//    }

//    // ������ 4. �f�[�^�\����` ������

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