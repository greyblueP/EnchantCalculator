import json
import os


# 读取附魔表
def Enchanting():
    failname = os.getcwd()+'\\附魔对照表.json'
    with open(failname, 'r', encoding='utf-8')as f:
        Enchanting = json.load(f)
    data = {}
    error = []
    for i in Enchanting:
        if i == '冲突附魔':
            error = Enchanting[i]
        else:
            for j in Enchanting[i]['适用装备']:
                if j not in data:
                    data[j] = []
                data[j].append([Enchanting[i]['魔咒'],
                                Enchanting[i]['最高等级'],
                                Enchanting[i]['权重']])

    return data, error


def choice1(data):
    print('以下是可选择的装备:')
    num = 0
    for i in data:
        num += 1
        print('   '+str(num)+' '+i)
    # 选择装备
    input_equip = input('请输入装备代号或名称:')
    try:
        if int(input_equip) <= len(data) and input_equip.isdigit():
            input_equip = list(data.keys())[int(input_equip)-1]
        if input_equip not in data:
            return False
        else:
            return input_equip
    except:
        return False


def choice2(error, data):
    print('以下是可选择的附魔(满级):')
    num = 0
    for i in data:
        num += 1
        txt = '   '+str(num)+' '+i[0]
        print(txt)
    input_enchant = input('请输入附魔代号或名称(空格间隔):')
    input_enchant = input_enchant.split(' ')
    try:
        for i in range(len(input_enchant)):
            if int(input_enchant[i]) <= len(data) and input_enchant[i].isdigit():
                input_enchant[i] = data[int(input_enchant[i])-1]
            if input_enchant[i] not in data:
                return False
    except:
        return False
    # 查看是否有冲突附魔
    for i in error:
        num = 0
        for j in input_enchant:
            if j[0] in i:
                num += 1
            if num > 1:
                return False
    return input_enchant


def function(input_equip, input_enchant):
    list = {}
    for i in input_enchant:
        list[i[0]] = int(i[1])*int(i[2])
    list = sorted(list.items(), key=lambda x: x[1], reverse=True)
    data = []
    for i, j in list:
        data.append([i, j])
    euqip = [input_equip, 0, 0]  # 装备,附魔次数,花费总等级

    # 第一次 1
    print(
        f'{str(euqip[1]+1)} 【{data[0][1]}】{euqip[0]} + {data[0][0]}'
    )
    euqip[2] += data[0][1]

    euqip[1] += 1
    data.pop(0)

    # 第二次 2
    if len(data) > 1:  # 2+
        print(
            f'{str(euqip[1]+1)} 【{data[-1][1]}】{data[0][0]} + {data[-1][0]} = 附魔书')
        euqip[2] += data[-1][1]

        level = data[-1][1]+data[0][1]+1+1
        print(f'  【{level}】{euqip[0]} + 附魔书')
        euqip[2] += level

        euqip[1] += 1
        data.pop(0)
        data.pop(-1)
    elif len(data) > 0:  # 1
        level = data[0][1]+1
        print(f'{str(euqip[1]+1)} 【{level}】{euqip[0]} + {data[0][0]}')
        euqip[2] += level

        euqip[1] += 1
        data.pop(0)

    # 第三次 4
    if len(data) > 3:  # 4+
        print(
            f'{str(euqip[1]+1)} 【{data[-1][1]}】{data[0][0]} + {data[-1][0]} = 附魔书1')
        euqip[2] += data[-1][1]

        print(f'  【{data[-2][1]}】{data[1][0]} + {data[-2][0]} = 附魔书2')
        euqip[2] += data[-2][1]

        level = data[1][1]+data[-2][1]+1+1
        print(f'  【{level}】附魔书1 + 附魔书2 = 附魔书')
        euqip[2] += level

        level = data[-1][1]+data[-2][1]+data[0][1]+data[1][1]+3+3
        print(f'  【{level}】{euqip[0]} + 附魔书')
        euqip[2] += level

        euqip[1] += 1
        data.pop(0)
        data.pop(1)
        data.pop(-2)
        data.pop(-1)
    elif len(data) == 3:  # 3
        print(
            f'{str(euqip[1]+1)} 【{data[-1][1]}】{data[0][0]} + {data[-1][0]} = 附魔书1')
        euqip[2] += data[-1][1]

        level = data[1][1]+1
        print(f'  【{level}】附魔书1 + {data[1][0]} = 附魔书')
        euqip[2] += level

        level = data[0][1]+data[1][1]+data[-1][1]+3+3
        print(f'  【{level}】{euqip[0]} + 附魔书')
        euqip[2] += level

        euqip[1] += 1
        data.pop(0)
        data.pop(1)
        data.pop(-1)
    elif len(data) == 2:  # 2
        print(
            f'{str(euqip[1]+1)} 【{data[-1][1]}】{data[0][0]} + {data[-1][0]} = 附魔书')
        euqip[2] += data[-1][1]

        level = data[0][1]+data[-1][1]+3+1
        print(f'  【{level}】{euqip[0]} + 附魔书')
        euqip[2] += level

        euqip[1] += 1
        data.pop(0)
        data.pop(-1)
    elif len(data) > 0:
        level = data[0][1]+3
        print(f'{str(euqip[1]+1)} 【{level}】{euqip[0]} + {data[0][0]}')

        euqip[1] += 1
        data.pop(0)

    print(f'共计花费等级{euqip[2]}级'+'\n'+'-'*40)


def _main_():
    # 选择装备
    input_equip = choice1(data)
    while input_equip == False:
        print('输入错误,请重新输入!\n')
        input_equip = choice1(data)
    print('\n你选择了 '+input_equip+'\n'+'-'*40)
    # 选择附魔
    input_enchant = choice2(error, data[input_equip])
    while input_enchant == False:
        print('输入错误或附魔冲突,请重新输入!\n')
        input_enchant = choice2(error, data[input_equip])
    txt = ''
    for i in input_enchant:
        txt += i[0]+i[1]+' '
    print('\n你选择了 '+txt+'\n' + '-'*40)

    function(input_equip, input_enchant)


data, error = Enchanting()
print('注意!以下附魔无法在同一装备上使用:')
for i in range(len(error)):
    txt = '  '+str(i+1)+'.'
    for j in error[i]:
        txt += j+' '
    print(txt)
print('—'*40)
while True:
    _main_()
    x = input('按回车继续')
