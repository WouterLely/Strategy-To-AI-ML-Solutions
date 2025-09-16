import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# ---------- Settings ----------
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# ---------- Applications and Products ----------
APPLICATIONS = [
    "SalesPortal", "HRSystem", "PayrollApp", "InventoryMgmt", "CustomerPortal",
    "AnalyticsDashboard", "EmailService", "DevOpsTooling", "KnowledgeBase", "ChatOps",
    "InternalWiki", "RecruitmentPlatform", "SupportDesk", "FinanceTool", "ProcurementApp",
    "MonitoringDashboard", "BackupService", "NotificationHub", "OnboardingTool", "TimeTracking"
]
AWS_PRODUCTS = ["EC2", "S3", "RDS", "Lambda", "DynamoDB", "CloudFront", "SNS", "SQS", "EKS"]

# ---------- Dummy Data Generator ----------
class DummyDataGenerator:
    def __init__(self, apps, products, days=120, seed=42):
        self.apps = apps
        self.products = products
        self.days = days
        np.random.seed(seed)

    def generate(self):
        dates = pd.date_range(start="2023-01-01", periods=self.days, freq="D")
        data = []
        for app in self.apps:
            for prod in self.products:
                base = np.random.uniform(80, 120)
                seasonal = 10 * np.sin(np.linspace(0, 3 * np.pi, self.days))
                noise = np.random.normal(0, 3, self.days)
                values = base + seasonal + noise

                # Inject **more anomalies** (spikes and drops)
                n_anoms = np.random.randint(25, 40)  # increase number of anomalies
                idx = np.random.choice(self.days, n_anoms, replace=False)
                for i in idx:
                    if np.random.rand() > 0.5:
                        values[i] += np.random.uniform(50, 150)  # bigger spikes
                    else:
                        values[i] -= np.random.uniform(50, 150)  # bigger drops

                for d, v in zip(dates, values):
                    data.append([app, prod, d, v])
        return pd.DataFrame(data, columns=["application_name", "product_name", "date", "eur_total_costs"])

# ---------- Holt-Winters Anomaly Detector ----------
def detect_anomalies_holtwinters(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    anomalies = []

    for (app, product), group in df.groupby(['application_name', 'product_name']):
        series = group.set_index('date')['eur_total_costs'].asfreq('D').fillna(0.0)
        if len(series) < 42:
            continue

        try:
            model = ExponentialSmoothing(
                series,
                seasonal='add',
                seasonal_periods=7,
                trend='add',
                initialization_method="estimated"
            ).fit()

            fitted = model.fittedvalues
            resid = series - fitted

            threshold = 2 * resid.std()
            anomaly_score = resid / threshold
            anomaly_score = anomaly_score.where(anomaly_score.abs() > 0.8, 0.0)

            result = pd.DataFrame({
                'application_name': app,
                'product_name': product,
                'date': series.index,
                'anomaly_score': anomaly_score.values
            })
            anomalies.append(result)

        except Exception as e:
            print(f"Holt-Winters failed for {app} × {product}: {e}")
            continue

    return pd.concat(anomalies).reset_index(drop=True) if anomalies else pd.DataFrame()

# ---------- Heatmap Visualizer ----------
def plot_heatmap_last_week(anomalies_df: pd.DataFrame):
    if anomalies_df.empty:
        print("No anomalies to display.")
        return

    last_date = anomalies_df['date'].max()
    start_date = last_date - pd.Timedelta(days=6)
    last_week = anomalies_df[anomalies_df['date'].between(start_date, last_date)]

    # Max anomaly score per app × product over last week
    pivot = last_week.groupby(['application_name', 'product_name'])['anomaly_score'].max().unstack(fill_value=0)
    pivot = pivot.reindex(index=APPLICATIONS, columns=AWS_PRODUCTS, fill_value=0)

    plt.figure(figsize=(16, 10))
    sns.heatmap(
        pivot,
        annot=True,
        cmap="Spectral",  # richer distribution of colors
        center=0,
        fmt=".2f",
        linewidths=0.5,
        linecolor="gray",
        cbar_kws={'label': 'Anomaly Strength'}
    )
    plt.title(f"AWS Products Anomaly Strength (Last 7 Days) — up to {last_date.date()}", fontsize=16)
    plt.ylabel("Application", fontsize=12)
    plt.xlabel("AWS Product", fontsize=12)
    plt.yticks(rotation=0)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ---------- Main ----------
if __name__ == "__main__":
    generator = DummyDataGenerator(APPLICATIONS, AWS_PRODUCTS, days=120)
    df = generator.generate()

    anomalies_df = detect_anomalies_holtwinters(df)
    plot_heatmap_last_week(anomalies_df)
