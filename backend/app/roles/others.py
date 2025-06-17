def fomart_others(others,me):
    message = ""
    for other in others:
        if other["name"] == me:
            continue
        message += other["name"]+"の反応："
    return message