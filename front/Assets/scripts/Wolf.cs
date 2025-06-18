using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class Wolf : MonoBehaviour
{

    public GameObject[] spheres;  // 5つの球体を順番に割り当て
    public TextAsset jsonFile;   // JSONファイル（Unity内に配置）
    public Image fadePanel; // ← 黒画像のUI

    private PersonData[] personDataList;  // 球体に付いている PersonData の参照リスト


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
                Debug.Log($"{sphere.name} にデータを割り当て: 名前={person.name}, 年齢={person.age}");
            }
            else
            {
                Debug.LogWarning($"{sphere.name} に PersonData スクリプトが見つかりませんでした。");
            }
        }

        // 初期状態でパネル透明にしておく
        if (fadePanel != null)
            fadePanel.color = new Color(0, 0, 0, 0);
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.KeypadEnter))
        {
            Debug.Log("Enterキーが押されました。暗転開始 → 削除処理へ");
            StartCoroutine(FadeAndDelete());
        }
    }

    IEnumerator FadeAndDelete()
    {
        // 暗転フェード（0 → 1）
        float duration = 1f;
        float t = 0f;
        while (t < duration)
        {
            t += Time.deltaTime;
            float alpha = Mathf.Lerp(0, 1, t / duration);
            fadePanel.color = new Color(0, 0, 0, alpha);
            yield return null;
        }

        yield return new WaitForSeconds(0.5f); // 少し暗転状態を保つ

        // 年齢100の球を削除
        for (int i = 0; i < personDataList.Length; i++)
        {
            if (personDataList[i] != null && personDataList[i].age == 100)
            {
                Debug.Log($"削除対象: {personDataList[i].gameObject.name}（年齢100）");
                Destroy(personDataList[i].gameObject);
                personDataList[i] = null;
            }
        }

        yield return new WaitForSeconds(0.5f); // 少し間を置いてから戻す

        // フェード戻し（1 → 0）
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
