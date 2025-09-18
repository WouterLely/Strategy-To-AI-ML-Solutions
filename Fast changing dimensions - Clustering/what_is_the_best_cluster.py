# Quick and Dirty Simple Example 
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
import networkx as nx
import warnings

# ----------------- Dummy Data Generator -----------------
class DummyDataGenerator:
    def __init__(self, applications, services, days=30, seed=42):
        self.applications = applications
        self.services = services
        self.days = days
        np.random.seed(seed)

    def generate(self):
        data = []
        for app in self.applications:
            base = np.random.uniform(500, 2000)
            for svc in self.services:
                svc_base = np.random.uniform(50, 500)
                values = base + svc_base + np.random.normal(0, 50, self.days)
                for v in values:
                    data.append([app, svc, v])
        return pd.DataFrame(data, columns=["application_name", "product_name", "eur_total_costs"])

# ----------------- Data Transformation -----------------
class DataTransformer:
    def __init__(self, df):
        self.df = df
        self.pivot = None
        self.X = None

    def pivot_data(self):
        self.pivot = self.df.pivot_table(
            index="application_name",
            columns="product_name",
            values="eur_total_costs",
            aggfunc="sum",
            fill_value=0
        )
        return self.pivot

    def scale_features(self):
        self.X = StandardScaler().fit_transform(self.pivot.values)
        return self.X

# ----------------- Cluster Analyzer -----------------
class ClusterAnalyzer:
    def __init__(self, X, names):
        self.X = X
        self.names = names
        self.results = []

    def try_kmeans(self, k_range=(2,6)):
        best, best_k, best_score = None, None, -1
        for k in range(k_range[0], min(k_range[1], self.X.shape[0]-1)+1):
            km = KMeans(n_clusters=k, random_state=0, n_init=10)
            labels = km.fit_predict(self.X)
            score = silhouette_score(self.X, labels)
            if score > best_score:
                best, best_k, best_score = labels, k, score
        self.results.append(("KMeans", best_k, best_score, best))

    def try_agglomerative(self):
        k = next((r[1] for r in self.results if r[0]=="KMeans"), None)
        if k is None: return
        ag = AgglomerativeClustering(n_clusters=k)
        labels = ag.fit_predict(self.X)
        score = silhouette_score(self.X, labels)
        self.results.append(("Agglomerative", k, score, labels))

    def try_gmm(self, max_components=6):
        best_bic, best_labels, best_n = np.inf, None, None
        for n in range(2, min(max_components, self.X.shape[0]-1)+1):
            gm = GaussianMixture(n_components=n, random_state=0)
            labels = gm.fit_predict(self.X)
            bic = gm.bic(self.X)
            if bic < best_bic:
                best_bic, best_labels, best_n = bic, labels, n
        score = silhouette_score(self.X, best_labels) if best_labels is not None else -1
        self.results.append(("GMM", best_n, score, best_labels))

    def try_dbscan(self):
        from sklearn.neighbors import NearestNeighbors
        k = min(5, self.X.shape[0]-1)
        nbrs = NearestNeighbors(n_neighbors=k).fit(self.X)
        dists, _ = nbrs.kneighbors(self.X)
        eps = np.percentile(dists[:, -1], 80)
        labels = DBSCAN(eps=eps, min_samples=3).fit_predict(self.X)
        score = silhouette_score(self.X, labels) if len(set(labels))>1 and -1 not in labels else -1
        self.results.append(("DBSCAN", None, score, labels))

    def try_hdbscan(self):
        if not HAVE_HDBSCAN:
            self.results.append(("HDBSCAN", None, -1, None))
            return
        labels = hdbscan.HDBSCAN(min_cluster_size=3).fit_predict(self.X)
        lab_valid = labels[labels!=-1]
        score = silhouette_score(self.X[labels!=-1], lab_valid) if len(set(lab_valid))>1 else -1
        self.results.append(("HDBSCAN", None, score, labels))

    def try_louvain(self):
        if not HAVE_LOUVAIN:
            self.results.append(("Louvain", None, -1, None))
            return
        from sklearn.metrics.pairwise import cosine_similarity
        sim = cosine_similarity(self.X)
        G = nx.Graph()
        for i, a in enumerate(self.names):
            for j, b in enumerate(self.names):
                if i>=j: continue
                if sim[i,j] > 0.5:
                    G.add_edge(a, b, weight=sim[i,j])
        if G.number_of_nodes() == 0:
            self.results.append(("Louvain", None, -1, None))
            return
        part = community_louvain.best_partition(G, weight='weight')
        labels = np.array([part.get(n,-1) for n in self.names])
        score = silhouette_score(self.X, labels) if len(set(labels))>1 and -1 not in labels else -1
        self.results.append(("Louvain", None, score, labels))

    def run_all(self):
        self.try_kmeans()
        self.try_agglomerative()
        self.try_gmm()
        self.try_dbscan()
        self.try_hdbscan()
        self.try_louvain()
        return self.results

    def print_summary(self, pivot):
        best, best_score = None, -999
        print("\nCluster Results:")
        for method, param, score, labels in self.results:
            if labels is None: continue
            print(f"Method: {method}, Param: {param}, Silhouette: {score:.3f}")
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            print(f"  Number of clusters: {n_clusters}")
            top_products = []
            df = pivot.copy()
            df['cluster'] = labels
            for cl, grp in df.groupby('cluster'):
                top = grp.drop(columns='cluster').sum().sort_values(ascending=False).head(3)
                top_products.append(f"Cluster {cl}: " + ", ".join(top.index))
            if score > best_score:
                best, best_score = (method, labels), score
        if best:
            method, labels = best
            print(f"\nBest method: {method}, Silhouette score: {best_score:.3f}")

# ----------------- Main -----------------
def main():
    applications = ["SalesPortal", "HRSystem", "PayrollApp", "InventoryMgmt", "CustomerPortal",
                    "AnalyticsDashboard", "EmailService", "DevOpsTooling", "KnowledgeBase", "ChatOps"]
    services = ["AWS Lambda", "Amazon API Gateway", "Amazon DynamoDB", "Amazon RDS",
                "Amazon SNS", "Amazon SQS", "Amazon S3", "Amazon VPC",
                "Amazon CloudWatch", "Amazon EC2", "Amazon ECS", "Amazon Redshift"]

    df = DummyDataGenerator(applications, services).generate()
    transformer = DataTransformer(df)
    pivot = transformer.pivot_data()
    X = transformer.scale_features()

    analyzer = ClusterAnalyzer(X, pivot.index)
    analyzer.run_all()
    analyzer.print_summary(pivot)

if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
