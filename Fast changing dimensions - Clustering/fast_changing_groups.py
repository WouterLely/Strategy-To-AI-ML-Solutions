import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 400)
pd.set_option('display.float_format', '{:,.2f}'.format)

# ---------- Settings ----------
RANDOM_SEED = 42
AWS_SERVICES = [
    "AWS Lambda", "Amazon API Gateway", "Amazon DynamoDB",
    "Amazon Relational Database Service", "Amazon Simple Notification Service",
    "Amazon Simple Queue Service", "Amazon Simple Storage Service",
    "Amazon Virtual Private Cloud", "AmazonCloudWatch",
    "Amazon Elastic Compute Cloud", "Amazon Elastic Container Service",
    "Amazon Redshift"
]

APPLICATIONS = [
    "SalesPortal", "HRSystem", "PayrollApp", "InventoryMgmt", "CustomerPortal",
    "AnalyticsDashboard", "EmailService", "DevOpsTooling", "KnowledgeBase", "ChatOps",
    "InternalWiki", "RecruitmentPlatform", "SupportDesk", "FinanceTool", "ProcurementApp",
    "MonitoringDashboard", "BackupService", "NotificationHub", "OnboardingTool", "TimeTracking"
]

# ---------- Manual cluster name mapping ----------
CLUSTER_NAME_MAPPING = {
    0: "A",
    1: "Server full applications",
    2: "Server less applications",
    3: "Database applications",
    4: "E",
    5: "F"
}

# ---------- Dummy Data Generator ----------
class DummyDataGenerator:
    def __init__(self, apps, services, days=42, seed=RANDOM_SEED):
        self.apps = apps
        self.services = services
        self.days = days
        np.random.seed(seed)

    def generate(self):
        data = []
        for app in self.apps:
            app_base = np.random.uniform(500, 2000)
            for service in self.services:
                service_base = np.random.uniform(50, 500)
                values = app_base + service_base + np.random.normal(0, 50, self.days)
                for v in values:
                    data.append([app, service, v])
        df = pd.DataFrame(data, columns=["application_name", "product_name", "eur_total_costs"])
        return df

# ---------- Data Transformation ----------
class DataTransformer:
    @staticmethod
    def pivot_costs(df: pd.DataFrame) -> pd.DataFrame:
        pivot = df.pivot_table(
            index="application_name",
            columns="product_name",
            values="eur_total_costs",
            aggfunc="sum",
            fill_value=0
        )
        pivot["total_cost"] = pivot.sum(axis=1)
        return pivot

    @staticmethod
    def normalize_to_percentage(pivot: pd.DataFrame) -> pd.DataFrame:
        pivot_pct = pivot.div(pivot["total_cost"], axis=0).fillna(0) * 100
        pivot_pct["total_cost"] = 100.0
        return pivot_pct

# ---------- Clustering ----------
class ClusterAnalyzer:
    def __init__(self, random_state=RANDOM_SEED):
        self.random_state = random_state

    def cluster_by_total_cost(self, pivot: pd.DataFrame, n_clusters=6):
        X = np.log1p(pivot[["total_cost"]].values)
        X_scaled = StandardScaler().fit_transform(X)
        kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state, n_init=10)
        pivot["cluster_total_cost"] = kmeans.fit_predict(X_scaled)
        return pivot, X_scaled

    def cluster_by_usage_pattern(self, pivot: pd.DataFrame, pivot_pct: pd.DataFrame, n_clusters=6):
        X_scaled = StandardScaler().fit_transform(pivot_pct[AWS_SERVICES].values)
        kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state, n_init=10)
        pivot["cluster_usage_pattern"] = kmeans.fit_predict(X_scaled)
        return pivot, X_scaled

    def silhouette_analysis(self, X, k_range, title):
        scores = []
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10).fit(X)
            scores.append(silhouette_score(X, kmeans.labels_))
        plt.figure(figsize=(8,5))
        plt.plot(k_range, scores, marker="o")
        plt.xlabel("Number of clusters (k)")
        plt.ylabel("Silhouette Score")
        plt.title(title)
        plt.show()

# ---------- Main ----------
def main():
    out_dir = "./output"
    os.makedirs(out_dir, exist_ok=True)

    # --- Generate dummy data ---
    generator = DummyDataGenerator(APPLICATIONS, AWS_SERVICES)
    df = generator.generate()

    # --- Transform data ---
    transformer = DataTransformer()
    pivot = transformer.pivot_costs(df)
    pivot_pct = transformer.normalize_to_percentage(pivot)

    # --- Clustering ---
    analyzer = ClusterAnalyzer()
    pivot, X_cost = analyzer.cluster_by_total_cost(pivot)
    pivot, X_usage = analyzer.cluster_by_usage_pattern(pivot, pivot_pct)

    # --- Summary Table ---
    summary_table = pivot.reset_index()[[
        "application_name", "cluster_total_cost", "cluster_usage_pattern"
    ]]

    # Add manual field for given cluster names
    summary_table["given_cluster_name"] = summary_table["cluster_usage_pattern"].map(CLUSTER_NAME_MAPPING)

    summary_csv = os.path.join(out_dir, "cluster_summary_full.csv")
    summary_table.to_csv(summary_csv, index=False, float_format="%.2f")  # ✅ no row numbers in CSV
    print("\nSaved cluster summary CSV to:", summary_csv)
    print(summary_table.to_string(index=False))  # ✅ no row numbers when printing

    # --- Top 3 products per cluster normalized ---
    top_products_summary = []
    clusters = pivot['cluster_usage_pattern'].unique()
    for cluster in sorted(clusters):
        cluster_data = pivot[pivot['cluster_usage_pattern'] == cluster]
        cluster_pct = cluster_data[AWS_SERVICES].div(cluster_data[AWS_SERVICES].sum(axis=1), axis=0).fillna(0) * 100
        top_products = cluster_pct.mean().sort_values(ascending=False).head(3)
        for product in top_products.index:
            top_products_summary.append({
                "cluster_usage_pattern": cluster,
                "given_cluster_name": CLUSTER_NAME_MAPPING.get(cluster, ""),
                "subscription": product,
                "mean_percentage": top_products[product]
            })

    top_products_df = pd.DataFrame(top_products_summary)
    top_products_csv = os.path.join(out_dir, "top3_products_per_cluster.csv")
    top_products_df.to_csv(top_products_csv, index=False, float_format="%.2f")  # ✅ no row numbers in CSV
    print("\nSaved Top 3 products per cluster (normalized) CSV to:", top_products_csv)
    print(top_products_df.to_string(index=False))  # ✅ no row numbers when printing

    # --- Silhouette plots ---
    analyzer.silhouette_analysis(X_cost, range(2, 10), "Silhouette Analysis - Total Cost")
    analyzer.silhouette_analysis(X_usage, range(2, 10), "Silhouette Analysis - Usage Pattern")

if __name__ == "__main__":
    main()
