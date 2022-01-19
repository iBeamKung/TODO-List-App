import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = ['School', 'Hospital', 'Condo', 'Office', 'Home']
all_means = [10, 5, 3, 2, 15]
men_means = [5, 3, 1, 1, 10]
women_means = [5, 2, 2, 1, 5]

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars
print(x)
fig, ax = plt.subplots()
rects2 = ax.bar(x - width, all_means, width, label='Task')
rects1 = ax.bar(x, men_means, width, label='Complete')
rects3 = ax.bar(x + width, women_means, width, label='Incomplete')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.show()