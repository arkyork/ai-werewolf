using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using static Wolf;

public class PersonData : MonoBehaviour
{
    public string personName;
    public int age;

    public TextMeshPro textDisplay; // 頭上表示用（TextMeshPro）

    public void ApplyData(Person data)
    {
        personName = data.name;
        age = data.age;

        if (textDisplay != null)
        {
            textDisplay.text = personName;
        }
    }
}
