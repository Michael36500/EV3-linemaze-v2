from  main import main
from tqdm import tqdm


lst = []


for _ in tqdm(range(10000)):
    lst.append(main(debug=False))

print('Average:', sum(lst) / len(lst))
print('Max:', max(lst))
print('Min:', min(lst))
print('Total:', len(lst))
print('Median:', lst[len(lst) // 2])