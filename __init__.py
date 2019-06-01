def parse(line):
    symbols = '+>()^'
    level = 0
    lst = []
    current_text = ''
    for i in line:
        if i not in symbols:
            current_text += i
        else:
            val = dict(tag=current_text, level=level)
            lst.append(val)
            if i == '>':
                level += 1
            elif i == '^':
                level -= 1
            current_text = ''
    if current_text:
        lst.append(dict(tag=current_text, level=level))
    for i in lst:
        if '*' in i['tag']:
            i['num'] = int(i['tag'].split('*')[1])
            i['tag'] = i['tag'].split('*')[0]
    return lst


def has_mults(arr):
    for i in arr:
        if 'num' in i:
            return i['num']>1
    return False


def delete_mult(arr):
    i=0
    while i<len(arr):
        if 'num' in arr[i]:
            if arr[i]['num']>1:
                break
        i += 1
    num=arr[i]['num']
    level=arr[i]['level']
    start=i
    i += 1
    while i < len(arr):
        if arr[i]['level']>level:
            i += 1
        else:
            break
    end = i
    repeated=[]
    for i in  arr[start:end]:
        repeated.append(i.copy())
    repeated[0].pop('num')
    repeated*=num
    for i in range(end-start):
        arr.pop(start)
    for i in range(len(repeated)):
        arr.insert(start,repeated[-i-1])
    return arr


def delete_mults(arr):
    while has_mults(arr):
        arr=delete_mult(arr)
    return arr


def parse_css(tag):
    tname=''
    tclass=''
    tid=''
    text=''
    mode='name'
    for i in tag:
        if i=='{':
            mode='text'
        elif i=='}':
            mode='name'
        elif i=='#':
            mode='id'
            if not tid=='':
                tid+=' '
        elif i=='.':
            mode='class'
            if not tclass=='':
                tclass+=' '
        else:
            if mode=='id':
                tid+=i
            elif mode=='class':
                tclass+=i
            elif mode=='text':
                text+=i
            else:
                tname+=i

    result=tname
    if not tclass=='':
        result+=' class=\''+tclass+'\''
    if not tid=='':
        result+=' id=\''+tid+'\''
    return result+(('####'+text)if not text=='' else '')

def test_out(arr):
    stack=[]
    for i in arr:
        if not i['tag'].strip()=='':
            level=i['level']
            tag=i['tag']
            tagname=parse_css(tag).split(' ')[0]
            if len(stack)>0:
                while level<=stack[-1][1]:
                    print('\t'*stack[-1][1]+'</'+stack[-1][0]+'>')
                    stack.pop(-1)
            stack.append([tagname.split('####')[0],level])
            print('\t'*level+'<'+parse_css(tag).split('####')[0]+'>')
            if '{' in tag:
                print('\t'*(level+1)+tag.split('{')[1].split('}')[0]) # это НЕ тег
    for i in range(len(stack)):
        tag=stack[-1-i]
        print('\t'*tag[1]+'</'+tag[0]+'>')

text='html>head#s+body>ul.list*2>li.item*3'#input()
parsed=parse(text)
parsed=delete_mults(parsed)
test_out(parsed)

