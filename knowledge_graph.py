import pandas as pd
import networkx as nx
from tqdm import tqdm

df = pd.read_csv("IMDb movies.csv")

sample = df.sample(100, random_state=42)

sample["genre"] = sample["genre"].fillna("").apply(lambda x: x.split(", "))
sample["actors"] = sample["actors"].fillna("").apply(lambda x: x.split(", "))
sample["language"] = sample["language"].fillna("").apply(lambda x: x.split(", "))

for j in ["actors", "genre", "language"]:
    colname = j + "_edited"
    sample[colname] = sample[["title", j]].apply(lambda a: [(a["title"], actor) for actor in a[j]], axis=1)


G = nx.Graph()

for i in tqdm(sample.index):
    for j in sample[["title", "genre", "country", "language", "director", "production_company", "actors", "writer"]]:
            if j in ["actors", "genre", "language"]:
                G.add_nodes_from(sample.loc[i, j])
                colname = j + "_edited"
                G.add_edges_from(sample.loc[i, colname], attr=j)
            else:
                G.add_node(sample.loc[i, j])
                G.add_edge(sample.loc[i, "title"], sample.loc[i, j], attr=j)


print("Number of nodes: {}".format(len(G.nodes)))

print("Details about the movie {}: {}".format("Insonnia d'amore", G["Insonnia d'amore"]))

print("Genres of the the movie {}: {}".format("Insonnia d'amore", [y for x, y, attr in G.edges("Insonnia d'amore", data=True) if attr["attr"] == "genre"]))

d = {}
for e in list(nx.dfs_edges(G, source="Insonnia d'amore", depth_limit=2)):
    if d.get(e[1]):
        d[e[1]] +=1
    else:
        d[e[1]] = 1

similar_movies = {}
for node in tqdm(d.keys()):
    similar_movies[node] = len(list(nx.all_shortest_paths(G, source=node, target="Insonnia d'amore")))

print("Similar movies: ", {k: v for k, v in sorted(similar_movies.items(), key=lambda item: item[1], reverse=True)})

