import seaborn as sns
import matplotlib.pyplot as plt

# Sample data (you can replace this with your own dataset)
data = [
    [0.8, 0.2, 0.5, 0.6],
    [0.3, 0.7, 0.1, 0.9],
    [0.4, 0.4, 0.8, 0.3],
    [0.1, 0.5, 0.6, 0.7]
]

# Create a heatmap using Seaborn
sns.set()  # Set Seaborn style (optional)
sns.heatmap(data, annot=True, cmap="YlGnBu", fmt=".2f")

# Add labels and title
plt.xlabel("X-axis Labels")
plt.ylabel("Y-axis Labels")
plt.title("Example Heatmap")

# Show the plot
plt.show()