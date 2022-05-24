import matplotlib.pyplot as plt
import numpy as np

list1 = []
f = open("f1.txt", "r")
for line in f.readlines():
    list1.append(float(line.replace("\n", "")))
f.close()

list2 = []
f = open("f2.txt", "r")
for line in f.readlines():
    list2.append(float(line.replace("\n", "")))
f.close()

list3 = []
f = open("f3.txt", "r")
for line in f.readlines():
    list3.append(float(line.replace("\n", "")))
f.close()

list4 = []
f = open("f4.txt", "r")
for line in f.readlines():
    list4.append(float(line.replace("\n", "")))
f.close()

list5 = []
f = open("f5.txt", "r")
for line in f.readlines():
    list5.append(float(line.replace("\n", "")))
f.close()

list6 = []
f = open("f6.txt", "r")
for line in f.readlines():
    list6.append(float(line.replace("\n", "")))
f.close()

list7 = []
f = open("f7.txt", "r")
for line in f.readlines():
    list7.append(float(line.replace("\n", "")))
f.close()

list8 = []
f = open("f8.txt", "r")
for line in f.readlines():
    list8.append(float(line.replace("\n", "")))
f.close()

list9 = []
f = open("f9.txt", "r")
for line in f.readlines():
    list9.append(float(line.replace("\n", "")))
f.close()

N = np.linspace(0, len(list1), len(list1))
plt.figure(figsize=[20,10])
plt.plot(N,list1,label="0.1")
# plt.plot(N,list2,label="0.2")
# plt.plot(N,list3,label="0.3")
# plt.plot(N,list4,label="0.4")
# plt.plot(N,list5,label="0.5")
# plt.plot(N,list6,label="0.6")
# plt.plot(N,list7,label="0.7")
# plt.plot(N,list8,label="0.8")
plt.plot(N,list9,label="0.9")
plt.xlabel("Itérations")
plt.ylabel("Q-value")
plt.title("Q-value en fonction du nombre d'itérations")
plt.legend()
plt.show()