height = float(input('请输入身高(cm):'))
weight = float(input('请输入体重(kg):'))
BMI = float(weight / float((height * height)))
if BMI < 18.5:
    print('过轻')
elif 18.5 <= BMI <= 25:
    print('正常')
elif 25 <= BMI <= 28:
    print('过重')
else:
    print('严重肥胖')
input("按任意键退出")
