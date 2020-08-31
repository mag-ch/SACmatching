import geopy
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint


# Significant parts of this code are taken from this blog post https://github.com/gboeing/2014-summer-travels/blob/master/clustering-scikitlearn.ipynb
users = pd.read_csv("responses_clean_locations.csv")
# users_who_want_loc = user_data[user_data["Do you have a preference on location of the person you are matched with? "] != "No"]
users = users.drop_duplicates("Email address")

clusters = {}
pd.options.mode.chained_assignment = None

with open('locationData.json') as json_file:
    location_data = json.load(json_file)
    lat = []
    lon = []
    for index, row in users.iterrows():
        location = location_data[row.iloc[3]]
        lat.append(float(location["lat"]))
        lon.append(float(location["lon"]))
    users["lat"] = lat
    users["lon"] = lon
    coords = users[['lat', 'lon']].to_numpy()
    kms_per_radian = 6371.0088
    epsilon = 50 / kms_per_radian
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree',
                metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels)) - \
        (1 if -1 in cluster_labels else 0)
    clusters = pd.Series([coords[cluster_labels == n]
                          for n in range(num_clusters)])

    def f(row): return users[(users['lat'] == row['lat']) &
                             (users['lon'] == row['lon'])].iloc[0]

    def show_on_graph():
        print('Number of clusters: {}'.format(num_clusters))
        _, ax = plt.subplots(figsize=[10, 6])

        def get_centermost_point(cluster):
            centroid = (MultiPoint(cluster).centroid.x,
                        MultiPoint(cluster).centroid.y)
            centermost_point = min(
                cluster, key=lambda point: great_circle(point, centroid).m)
            return tuple(centermost_point)
        centermost_points = clusters.map(get_centermost_point)
        lats, lons = zip(*centermost_points)
        rep_points = pd.DataFrame({'lon': lons, 'lat': lats})
        print(len(rep_points))
        rs = rep_points.apply(f, axis=1)
        rs_scatter = ax.scatter(
            rs['lon'], rs['lat'], c='#99cc99', edgecolor='None', alpha=0.7, s=120)
        df_scatter = ax.scatter(
            users['lon'], users['lat'], c='k', alpha=0.9, s=3)
        ax.set_title('Full data set vs DBSCAN reduced set')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.legend([rs_scatter, df_scatter], [
            'Full set', 'Reduced set'], loc='upper right')
        plt.show()
    show_on_graph()

    def get_users_with_coords(user_coords):
        return users[(users['lat'] == user_coords[0]) &
                     (users['lon'] == user_coords[1])]

    def cluster_to_users(cluster, n):
        unique_coords = np.unique(cluster, axis=0)
        users_by_coords = list(map(get_users_with_coords, unique_coords))
        group_id = n if len(cluster) > 1 else -1
        print(len(cluster))
        return [
            list(item) + [group_id] for sublist in users_by_coords for item in sublist.values]

    users_with_group_ids = list(
        map(cluster_to_users, clusters, range(0, len(clusters))))
    flat_list = [item for sublist in users_with_group_ids for item in sublist]
    df = pd.DataFrame(flat_list,
                      columns=list(users.columns.values) + ["group_id"])
