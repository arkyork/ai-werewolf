//using System.Collections.Generic;
//using UnityEngine;

//public static class Json
//{
//    [System.Serializable]
//    private class Wrapper
//    {
//        public List<string> keys;
//        public List<RoleData> values;
//    }

//    public static Dictionary<string, RoleData> FromJson<T>(string json)
//    {
//        json = json.Replace("{", "{\"keys\":[")
//                   .Replace(":", "],\"values\":[")
//                   .Replace("}", "]}");

//        Wrapper wrapper = JsonUtility.FromJson<Wrapper>(json);
//        Dictionary<string, RoleData> dict = new Dictionary<string, RoleData>();

//        for (int i = 0; i < wrapper.keys.Count; i++)
//        {
//            dict[wrapper.keys[i]] = wrapper.values[i];
//        }

//        return dict;
//    }
//}
