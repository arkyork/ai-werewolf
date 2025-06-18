def fomart_others(others,me):
    message = ""
    for key,value in others.items():
        if me == key:
            continue
        message += key +"の反応："+value
    return message