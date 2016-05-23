def get_rack_full_or_empty(rack):
    result = []
    for i in range(len(rack)):
        if rack[i] == -1:
            result.append(0.0)
        else:
            result.append(1.0)
    return result


def get_rack_same_or_not(rack, order):
    results = []
    for i in range(len(order)):
        result = []
        for j in range(len(rack)):
            if rack[j] == order[i]:
                result.append(1.0)
            else:
                result.append(0.0)
        results.append(result)
    return results


def get_storage_binary(rack):
    result = []
    for i in range(len(rack)):
        if rack[i] == -1:
            result.append(1.0)
        else:
            result.append(0.0)
    return result


def get_storage_ternary(rack, input):
    results = []
    for i in range(len(input)):
        result = []
        for j in range(len(rack)):
            if rack[j] == -1:
                result.append(1.0)
            elif rack[j] == input[i]:
                result.append(0.5)
            else:
                result.append(0.0)
        results.append(result)
    return results


def get_retrieval_binary(rack, output):
    results = []
    for i in range(len(output)):
        result = []
        for j in range(len(rack)):
            if rack[j] == output[i]:
                result.append(1.0)
            else:
                result.append(0.0)
        results.append(result)
    return results


def get_retrieval_2in1(rack, output):
    result = []
    for i in range(len(rack)):
        for j in range(len(output)):
            if rack[i] == output[j]:
                result.append(1.0)
                break
            else:
                result.append(0.0)
    return result


def get_retrieval_ternary(rack, output):
    result = ''
    retrieval = []
    for i in output.split('/'):
        if i[len(i)-1] == 'R':
            retrieval.append(i.split('_')[1])

    for j in rack.split(','):
        boolean = True
        for k in retrieval:
            if j == k:
                result += str(retrieval.index(k))+'.0'
                boolean = False
                break
        if boolean:
             result += '0.5'
        result += ','
    return result[0:len(result)-1]

if __name__ == '__main__':
    print get_storage_ternary()
    print get_retrieval_binary()
    print get_retrieval_2in1()
