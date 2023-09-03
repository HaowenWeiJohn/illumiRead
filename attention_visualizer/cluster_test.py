import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

X = np.array([[1,1], [1,2], [0,0], [5,5], [5,6], [6,5], [10,10], [10,11], [11,10], [12,11]])

# Calculate WCSS for different values of n_clusters
wcss = []
for i in range(1, 11):  # Try a range of cluster values from 1 to 10
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# Plot the WCSS values
plt.plot(range(1, 11), wcss)
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.title('Elbow Method')
plt.show()