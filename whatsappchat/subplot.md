subplot means ek hi plot mein kayi sare figures or graph bana do
aurt sabko index de do.

import matplotlib.pyplot as plt
x=[1,2,3,4]
y=[1,2,3,4]
plt.subplot(2,2,1)     
# subplot(nrows , ncols, index)
plt.plot(x,y,color='r')


plt.subplot(2,2,2)
plt.pie([1],colors='r')
# 1 is radius

x1=[10,20,30,40]
plt.subplot(2,2,3)
plt.pie(x)

x2=["a","s","d","f"]
y2=[10,20,30,40]
plt.subplot(2,2,4)
plt.bar(x2,y2)

plt.show