using System;

[Serializable]
public class Person
{
    public string name;
}

[Serializable]
public class PersonList
{
    public Person[] people;
}
