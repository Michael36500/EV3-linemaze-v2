from  main import main
from tqdm import tqdm
from matplotlib import pyplot as plt


lst = []


for _ in tqdm(range(100000)):
    lst.append(main(debug=False))


print('Average:', sum(lst) / len(lst))
print('Max:', max(lst))
print('Min:', min(lst))
print('Total:', len(lst))
print('Median:', lst[len(lst) // 2])


plt.hist(lst, bins=50,)
plt.show()