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


def parse_css(tag,prev,arr,index):
    prev=prev.split('#')[0].split('.')[0].split('{')[0]
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
    custom=''
    if '[' in tname:
        if ']' in tname:
            start=0
            while not tname[start]=='[':
                start += 1
            end = 0
            while not tname[end] == ']':
                end += 1
            cur=start+1
            mod='name'
            while cur<end:
                if tname[cur]=='=':
                    mod='quote'
                elif tname[cur]==' ':
                    if mod=='val':
                        tname = tname[:cur] + '\'' + tname[cur:]
                        end+=1
                    mod='name'
                elif tname[cur] in ['"','\'']:
                    mod='name'
                elif mod=='quote':
                    if not tname[cur] in ['\'','"']:
                        tname=tname[:cur]+'\''+tname[cur:]
                        end+=1
                    mod='val'
                cur+=1
            tname=tname.replace('[',' ')
            tname=tname.replace(']','')
    result=tname
    if result=='':
        if prev=='table':
            result='tr'
            arr[index]['tag']='tr'
        elif prev=='tr':
            result='td'
            arr[index]['tag'] = 'td'
        elif prev=='ul':
            result='li'
            arr[index]['tag'] = 'li'+('' if tclass=='' else ('.'+tclass))
        elif prev=='em':
            result='span'
            arr[index]['tag'] = 'span'
        else:
            result='div'
    if not tclass=='':
        result+=' class=\''+tclass+'\''
    if not tid=='':
        result+=' id=\''+tid+'\''
    return result+(('####'+text)if not text=='' else '')

def test_out(arr):
    stack=[]
    index=0
    print(arr)
    for i in arr:
        if not i['tag'].strip()=='':
            level=i['level']
            tag=i['tag']
            if index==0:
                prev = ''
            else:
                prev=''
                pindex=index
                while pindex>0:
                    pindex-=1
                    if arr[pindex]['level']<level:
                        prev=arr[pindex]['tag']
                        break
            tagname=parse_css(tag,prev,arr,index).split(' ')[0].split('[')[0]
            if len(stack)>0:
                while level<=stack[-1][1]:
                    print('\t'*stack[-1][1]+'</'+stack[-1][0]+'>')
                    stack.pop(-1)
            stack.append([tagname.split('####')[0],level])
            print('\t'*level+'<'+parse_css(tag,prev,arr,index).split('####')[0]+'>')
            if '{' in tag:
                print('\t'*(level+1)+tag.split('{')[1].split('}')[0]) # это НЕ тег
        index+=1
    for i in range(len(stack)):
        tag=stack[-1-i]
        print('\t'*tag[1]+'</'+tag[0]+'>')

text='html>head+body>a[name="d" b=98 c=6 q=12 ]*2'#input()
parsed=parse(text)
parsed=delete_mults(parsed)
test_out(parsed)

