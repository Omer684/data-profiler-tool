import pandas as pd
import numpy as np

class DataProfiler:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_summary_stats(self):
        """Returns basic dataset shape and missing value counts."""
        summary = {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "missing_values": self.df.isnull().sum().to_dict(),
            "data_types": self.df.dtypes.astype(str).to_dict()
        }
        return summary

    def detect_outliers(self):
        """Detects numerical outliers using the IQR method."""
        outlier_counts = {}
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns

        for col in numerical_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            outlier_counts[col] = len(outliers)
            
        return outlier_counts

    def generate_sql_ddl(self, table_name="imported_data"):
        """Infers a basic SQL CREATE TABLE statement from Pandas data types."""
        type_mapping = {
            'int64': 'INTEGER',
            'float64': 'REAL',
            'object': 'TEXT',
            'bool': 'BOOLEAN',
            'datetime64[ns]': 'TIMESTAMP'
        }

        sql_columns = []
        for col, dtype in self.df.dtypes.items():
            # Clean column names for SQL safety
            safe_col = col.strip().lower().replace(" ", "_")
            sql_type = type_mapping.get(str(dtype), 'TEXT')
            sql_columns.append(f"    {safe_col} {sql_type}")

        columns_str = ",\n".join(sql_columns)
        ddl = f"CREATE TABLE {table_name} (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n{columns_str}\n);"
        return ddl