import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']}
df = pd.DataFrame(data)

# Define the row to highlight
highlight_row = 2

# Plotting
plt.figure(figsize=(10, 4))
ax = plt.subplot(111, frame_on=False)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
sns.set(font_scale=1.2)
sns.heatmap(df.T, annot=True, cmap='Blues', cbar=False, linewidths=0.5)

# Highlight the specified row
highlight_color = 'gold'
highlight_indices = [df.columns.get_loc(df.index[highlight_row])]
for idx in highlight_indices:
    ax.add_patch(plt.Rectangle((idx + 0.1, -0.2), 1, 1, fill=True, edgecolor=highlight_color, facecolor=highlight_color))

plt.title('DataFrame with Highlighted Row')
plt.show()