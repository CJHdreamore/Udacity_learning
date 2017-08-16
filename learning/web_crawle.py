def numbers_in_lists(str):
    list = []
    sublist = []
    j = 0
    max = int(str[j])
    list.append(int(str[j]))
    j = j + 1
    while j < len(str):
        new = int(str[j])
        if new <= max:
            sublist.append(new)
        else:
            if sublist:
                list.append(sublist)
            max = new
            list.append(max)
            sublist = []
        j = j + 1
    if sublist:
        list.append(sublist)
    return list

print numbers_in_lists('543987')
print numbers_in_lists('987654321')
print numbers_in_lists('455532123266')
print numbers_in_lists( '123456789')
print numbers_in_lists( '1112222333456')




