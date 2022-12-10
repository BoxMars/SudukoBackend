def generateFromStr(src):
    src.replace('\t', ' ')
    l=src.split('\n')
    for i in range(len(l)):
        l[i]=l[i].split("\t")
    print(*l)
    return l


if __name__ == '__main__':
    generateFromStr()
