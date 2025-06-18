using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class Wolf : MonoBehaviour
{

    public GameObject[] spheres;  // 5�̋��̂����ԂɊ��蓖��
    public TextAsset jsonFile;   // JSON�t�@�C���iUnity���ɔz�u�j
    public Image fadePanel; // �� ���摜��UI

    private PersonData[] personDataList;  // ���̂ɕt���Ă��� PersonData �̎Q�ƃ��X�g


    // Start is called before the first frame update
    void Start()
    {
        PersonList list = JsonUtility.FromJson<PersonList>(jsonFile.text);

        personDataList = new PersonData[spheres.Length];
        for (int i = 0; i < list.people.Length && i < spheres.Length; i++)
        {
            GameObject sphere = spheres[i];
            Person person = list.people[i];

            PersonData pd = sphere.GetComponent<PersonData>();
            if (pd != null)
            {
                pd.ApplyData(person);
                personDataList[i] = pd;
                Debug.Log($"{sphere.name} �Ƀf�[�^�����蓖��: ���O={person.name}, �N��={person.age}");
            }
            else
            {
                Debug.LogWarning($"{sphere.name} �� PersonData �X�N���v�g��������܂���ł����B");
            }
        }

        // ������ԂŃp�l�������ɂ��Ă���
        if (fadePanel != null)
            fadePanel.color = new Color(0, 0, 0, 0);
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
        {
            Debug.Log("Enter�L�[��������܂����B�Ó]�J�n �� �폜������");
            StartCoroutine(FadeAndDelete());
        }
    }

    IEnumerator FadeAndDelete()
    {
        // �Ó]�t�F�[�h�i0 �� 1�j
        float duration = 1f;
        float t = 0f;
        while (t < duration)
        {
            t += Time.deltaTime;
            float alpha = Mathf.Lerp(0, 1, t / duration);
            fadePanel.color = new Color(0, 0, 0, alpha);
            yield return null;
        }

        yield return new WaitForSeconds(0.5f); // �����Ó]��Ԃ�ۂ�

        // �N��100�̋����폜
        for (int i = 0; i < personDataList.Length; i++)
        {
            if (personDataList[i] != null && personDataList[i].age == 100)
            {
                Debug.Log($"�폜�Ώ�: {personDataList[i].gameObject.name}�i�N��100�j");
                Destroy(personDataList[i].gameObject);
                personDataList[i] = null;
            }
        }

        yield return new WaitForSeconds(0.5f); // �����Ԃ�u���Ă���߂�

        // �t�F�[�h�߂��i1 �� 0�j
        t = 0f;
        while (t < duration)
        {
            t += Time.deltaTime;
            float alpha = Mathf.Lerp(1, 0, t / duration);
            fadePanel.color = new Color(0, 0, 0, alpha);
            yield return null;
        }
    }
}
