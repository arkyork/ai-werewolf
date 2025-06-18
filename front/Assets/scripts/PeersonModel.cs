using System;

[Serializable]
public class Person
{
    public string name;
    public int age;
}

[Serializable]
public class PersonList
{
    public Person[] people;
}
