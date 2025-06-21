from roles.wolf import Wolf

baker = Wolf()
print(baker.react_prompt_en("111"))
print(baker.react_prompt_ja("111"))
print(baker.sus_prompt_ja("111","111",{"1":"1"}))
print(baker.sus_prompt_en("111","111",{"1":"1"}))