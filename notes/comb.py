
def combo(param_list, integer):
    temp_list = []
    return_list = []
    if integer < 1:
        raise ValueError('Invalid value!')
    if integer == 1:
        return [[param] for param in param_list]
    while integer <= len(param_list):
        temp_list = param_list[:integer - 1]
        # print(temp_list)
        length = len(param_list)
        element = integer - 1
        while element < length:
            temp_list.append(param_list[element])
            # print(temp_list)
            return_list.append(temp_list)
            temp_list = param_list[:integer-1]
            element += 1
        param_list.pop(0)
    return return_list

if __name__ == '__main__':
    print(combo(['a','b','c','d','e','f','g'], -1))
