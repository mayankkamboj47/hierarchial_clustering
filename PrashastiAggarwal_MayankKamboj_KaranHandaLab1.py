"""
Group Members - 
1.  Prashasti Aggarwal
2.  Mayank Kamboj
3.  Karan Handa
"""

"""
Requirements - 
1.  Read a dataset from a file and run your 
    clustering model on it for different values 
    of K.
2.  Need to show demo of program with 5000 points
    in 2D. This means that time complexity can be
    atmost O(n^3)
3.  Visualization needs to be there.
"""
import math
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage

class AHC:
    def euclidean_dist(self, node1, node2):
        return math.sqrt((node1[0] - node2[0])**2 + (node1[1] - node2[1])**2)
    def initialize_dist_matrix(self):
        for i in range(self.n):
            min_cluster_id = -1
            min_cluster_dist = math.inf
            for j in range(self.n):
                self.dist_matrix[i][j] = self.euclidean_dist(self.clusters[i][0], self.clusters[j][0])
                if (i != j and self.dist_matrix[i][j] < min_cluster_dist):
                    min_cluster_dist = self.dist_matrix[i][j]
                    min_cluster_id = j
            self.min_arr[i] = [min_cluster_dist, min_cluster_id]
    def __init__(self, data, k):
        self.data = data
        self.n = len(data)
        self.k = k
        self.clusters = {data_id : [data_point] for data_id, data_point in enumerate(self.data)}
        self.dist_matrix = {item_id: {item_id : -1 for item_id in range(self.n)} for item_id in range(self.n)}
        # min_array[i] = [min dist from cluster(i) to any other cluster, id of min dist cluster]
        self.min_arr = {item_id: [-1, -1] for item_id in range(self.n)}
        self.initialize_dist_matrix()
        # Don't need the valid_cluster<bool> thingy
    
    def distance(self, cluster1_id, cluster2_id):
        return self.dist_matrix[cluster1_id][cluster2_id]

    def run_algorithm(self):
        while (len(self.clusters) > self.k):
            # Find two clusters with the smallest dist
            # print("top")
            # print(self.clusters)
            min_dist = math.inf
            cluster_x_id = -1
            cluster_y_id = -1
            # print(f"min_arr = {self.min_arr}")
            for x in self.min_arr:
                if (self.min_arr[x][0] < min_dist):
                    cluster_x_id = x
                    cluster_y_id = self.min_arr[x][1]
            
            # print(f"cluster_x_id = {cluster_x_id} and cluster_y_id = {cluster_y_id}")
            # Now we have cluster_x and cluster_y and we wish to merge these clusters
            # First update clusters. We're retaining the x cluster and removing the y cluster
            self.clusters[cluster_x_id].extend(self.clusters[cluster_y_id])
            del self.clusters[cluster_y_id]

            # Update array of distances.
            for i in self.dist_matrix:
                self.dist_matrix[cluster_x_id][i] = min(self.dist_matrix[cluster_x_id][i], self.dist_matrix[cluster_y_id][i])
                self.dist_matrix[i][cluster_x_id] = min(self.dist_matrix[i][cluster_x_id], self.dist_matrix[i][cluster_y_id])
            
            del self.dist_matrix[cluster_y_id]
            for i in self.dist_matrix:
                del self.dist_matrix[i][cluster_y_id]

            # print("BONK")
            # print(self.dist_matrix)

            # Update min_arr
            del self.min_arr[cluster_y_id]
            min_dist = math.inf
            min_dist_id = -1
            for i in self.dist_matrix:
                if (i != cluster_x_id and self.dist_matrix[i][cluster_x_id] < min_dist):
                    min_dist = self.dist_matrix[i][cluster_x_id]
                    min_dist_id = i
            self.min_arr[cluster_x_id][0] = min_dist
            self.min_arr[cluster_x_id][1] = min_dist_id

            # print(self.clusters)


    #-------------------

def data_input(file_name):
    data = []
    with open(file_name) as f:
        linecount = 0
        for row in f.readlines():
            if linecount == 0: 
                linecount+=1 
                continue 
            data.append([float(item) for item in row.split(',')])
            linecount+=1
    return data

    
    #-------------------

def main():
    # Read Input
    data = data_input("test_data.csv")
    # print(data)

    # Initialize clusters
    # this is a dictionary of clusters
    # {0: [[point]], 1: [[point]], ...}
    clustering_algo = AHC(data, 5)

    # While the number of clusters is greater than k
        # Find the closest clusters.
        # Merge the clusters
    clustering_algo.run_algorithm()
    print(clustering_algo.clusters) #save it in the variable

    #-------------------

    # Dendrogram Visualization
    linkage_data = linkage(data, method='ward', metric='euclidean')
    dendrogram(linkage_data)
    # Plotting a horizontal line based on the first biggest distance between clusters 
    plt.axhline(y = 0.9, color='red', linestyle='--'); 
    # Plotting a horizontal line based on the second biggest distance between clusters 
    plt.axhline(y = 0.8, color='crimson');
    plt.title("Agglomerative Hierarchical Clustering Dendrogram")
    plt.show()

    # Scatter Plot Visualization
    # plt.figure(figsize=(0,15))
    # plt.scatter(data[0], data[1], c = clustering_algo.clusters)
    # ----------
    # plt.figure(figsize=(20,10))
    # sns.scatterplot(X[:,0], X[:, 1], hue=cluster)
    # sns.scatterplot(c_points[:,0], c_points[:, 1], s=200, color='blue')

main()
