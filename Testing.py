# code
import sys

"""n = int(input().strip())
ans = []
flag = True
index = 0
for i in range(int(n)):
    m = int(input().strip())
    for j in range(int(m)):
        var = int(input().strip())
        if var[j] == 1 and flag:
            ans.append(i)
            flag = False
    if flag == True:
        ans.append(-1)
    index += 1
    Flag = True

print(ans)
"""
i = 1
sum =0
for j in range(1,1000000):
    sum += 1/j

print(sum)