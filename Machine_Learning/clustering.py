import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
from generic import read_cluster_data_set


def indicator(train_x):
    pca = PCA(n_components=2)
    scaled_x = scale(train_x)
    return pca.fit_transform(scaled_x)


def k_means(train_x, train_y=None, num_classes=3):
    # num_classes = len(np.unique(train_x, axis=0))
    kmeans = KMeans(n_clusters=num_classes)
    kmeans.fit(train_x)

    # Project High dimensional data to 2-D
    # https://stackoverflow.com/questions/27930413/how-to-plot-a-multi-dimensional-data-point-in-python
    if np.shape(train_x)[1] == 2:
        print("DO NOT PCA IT!")
        plot(train_x, train_y, kmeans)
    else:
        pr_comp = indicator(train_x)
        x = pr_comp[:, 0]
        y = pr_comp[:, 1]
        plot(x, y, kmeans)


# Assume incoming data is already 2-D
def plot(x, y, kmeans):
    print(np.shape(x))
    plt.title("Clusters")
    labels = kmeans.labels_
    colors = cm.rainbow(np.linspace(0, 1, kmeans.n_clusters))
    # colors = ["g.", "r.", "c."]
    # Print Label and feature
    for i in range(len(x)):
        # print(str(labels[i]) + " -> " + str(y[i]))
        # plt.plot(x[i], y[i], color=colors[labels[i]], marker='o', linestyle='-', markersize=10)
        plt.plot(x[i][0], x[i][1], 'o', color=colors[labels[i]], markersize=10)
        print(str(x[i][0]) + "," + str(x[i][1]))

    centroids = kmeans.cluster_centers_
    print(centroids)
    plt.scatter(centroids[:, 0], centroids[:, 1], marker="X", s=150, linewidths=5, zorder=10)

    # Create legend dictionary...
    # legend_dict = {}
    # for i in range(len(labels)):
    #    legend_dict[labels[i]] = colors[labels[i]]

    # patch_list = []
    # for key in legend_dict:
    #    data_key = mpatches.Patch(color=legend_dict[key], label=key)
    #    patch_list.append(data_key)
    # plt.legend(loc='best', handles=patch_list)
    plt.show()
    # plt.savefig('foo.png')

def main():
    # Read Wifi and Blue Tooth Data Set
    pts = read_cluster_data_set("./../../HOME_g8.csv")
    # Cluster it...see what happens...
    k_means(pts, None)


if __name__ == "__main__":
    main()