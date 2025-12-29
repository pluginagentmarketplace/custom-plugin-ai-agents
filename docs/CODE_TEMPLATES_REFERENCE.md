# Code Templates & Reference Guide for Claude Code AI/Data Agents

## Overview
Practical code templates, patterns, and snippets that Claude Code agents can use to provide concrete assistance across all AI/Data specializations.

---

## 1. AI ENGINEER CODE TEMPLATES

### 1.1 Basic API Integration Pattern

```python
# API Integration Template
import os
from typing import Optional
import httpx
import json

class AIEngineerAPIClient:
    """Base class for AI API interactions"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("API_KEY")
        self.base_url = "https://api.openai.com/v1"
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )

    def make_request(
        self,
        endpoint: str,
        method: str = "POST",
        payload: dict = None,
        **kwargs
    ) -> dict:
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = self.client.request(
                method,
                url,
                json=payload,
                timeout=30.0,
                **kwargs
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            print(f"API Error: {e.response.status_code} - {e}")
            raise
        except Exception as e:
            print(f"Request Error: {e}")
            raise

# Usage
# client = AIEngineerAPIClient()
# result = client.make_request("chat/completions", payload={...})
```

### 1.2 Prompt Management Pattern

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class PromptRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class Message:
    role: PromptRole
    content: str

class PromptManager:
    """Manage prompts and conversation history"""

    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.messages: List[Message] = [
            Message(PromptRole.SYSTEM, system_prompt)
        ]

    def add_user_message(self, content: str):
        """Add user message to history"""
        self.messages.append(Message(PromptRole.USER, content))

    def add_assistant_message(self, content: str):
        """Add assistant response to history"""
        self.messages.append(Message(PromptRole.ASSISTANT, content))

    def get_conversation(self) -> List[dict]:
        """Get conversation in API format"""
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in self.messages
        ]

    def clear_history(self):
        """Clear conversation while keeping system prompt"""
        self.messages = [self.messages[0]]

    def get_token_estimate(self) -> int:
        """Rough token count (4 chars ≈ 1 token)"""
        total_chars = sum(len(msg.content) for msg in self.messages)
        return total_chars // 4

# Usage
# prompt_mgr = PromptManager("You are a helpful coding assistant")
# prompt_mgr.add_user_message("How do I sort a list in Python?")
```

### 1.3 RAG (Vector Database) Integration

```python
from typing import List, Tuple
import numpy as np

class SimpleVectorStore:
    """Simplified vector store for RAG"""

    def __init__(self, embedding_model=None):
        self.documents = []
        self.embeddings = []
        self.embedding_model = embedding_model

    def add_document(self, text: str, metadata: dict = None):
        """Add document to vector store"""
        embedding = self.embedding_model.embed(text)
        self.documents.append({
            "text": text,
            "metadata": metadata or {},
            "id": len(self.documents)
        })
        self.embeddings.append(embedding)

    def search(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        """Search similar documents"""
        query_embedding = self.embedding_model.embed(query)

        # Cosine similarity
        similarities = []
        for i, embedding in enumerate(self.embeddings):
            similarity = np.dot(query_embedding, embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
            )
            similarities.append((self.documents[i]["text"], similarity))

        # Return top k
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:k]

# Usage pattern for RAG-based AI
def rag_augmented_response(query: str, vector_store: SimpleVectorStore, api_client):
    """Generate response using retrieved context"""
    # 1. Retrieve relevant documents
    relevant_docs = vector_store.search(query, k=3)
    context = "\n".join([doc[0] for doc in relevant_docs])

    # 2. Augment prompt with context
    augmented_prompt = f"""Use the following context to answer the question:

Context:
{context}

Question: {query}

Answer:"""

    # 3. Generate response
    response = api_client.make_request(
        "chat/completions",
        payload={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": augmented_prompt}]
        }
    )
    return response
```

### 1.4 Error Handling & Retry Logic

```python
import time
from functools import wraps
from typing import Callable, Any

def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """Decorator for retry logic with exponential backoff"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    if attempt == max_retries - 1:
                        raise

                    print(f"Attempt {attempt + 1} failed: {e}")
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= backoff_factor

        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3)
def call_api_with_retry(endpoint: str, payload: dict):
    return api_client.make_request(endpoint, payload)
```

---

## 2. DATA SCIENTIST CODE TEMPLATES

### 2.1 EDA (Exploratory Data Analysis) Pipeline

```python
import pandas as pd
import numpy as np
from typing import Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns

class DataExplorer:
    """Automated EDA toolkit"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.insights = {}

    def profile_data(self) -> Dict[str, Any]:
        """Generate comprehensive data profile"""
        profile = {
            "shape": self.df.shape,
            "dtypes": self.df.dtypes.to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
            "missing_percent": (self.df.isnull().sum() / len(self.df) * 100).to_dict(),
            "duplicates": self.df.duplicated().sum(),
        }
        return profile

    def analyze_distributions(self):
        """Analyze distribution of numerical columns"""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns

        analysis = {}
        for col in numerical_cols:
            analysis[col] = {
                "mean": self.df[col].mean(),
                "median": self.df[col].median(),
                "std": self.df[col].std(),
                "min": self.df[col].min(),
                "max": self.df[col].max(),
                "skewness": self.df[col].skew(),
                "kurtosis": self.df[col].kurtosis(),
            }

        self.insights["distributions"] = analysis
        return analysis

    def analyze_correlations(self):
        """Analyze correlations between features"""
        numerical_df = self.df.select_dtypes(include=[np.number])
        correlation_matrix = numerical_df.corr()

        # Find high correlations
        high_corr = {}
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr = correlation_matrix.iloc[i, j]
                if abs(corr) > 0.7:
                    col1 = correlation_matrix.columns[i]
                    col2 = correlation_matrix.columns[j]
                    high_corr[f"{col1}-{col2}"] = corr

        self.insights["high_correlations"] = high_corr
        return correlation_matrix

    def detect_outliers(self, method: str = "iqr"):
        """Detect outliers using IQR or Z-score"""
        numerical_df = self.df.select_dtypes(include=[np.number])
        outliers = {}

        if method == "iqr":
            for col in numerical_df.columns:
                Q1 = numerical_df[col].quantile(0.25)
                Q3 = numerical_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR

                outlier_count = ((numerical_df[col] < lower) |
                               (numerical_df[col] > upper)).sum()
                outliers[col] = outlier_count

        self.insights["outliers"] = outliers
        return outliers

    def get_summary(self) -> str:
        """Generate EDA summary"""
        profile = self.profile_data()

        summary = f"""
        === DATA EXPLORATION SUMMARY ===

        Shape: {profile['shape']}

        Missing Values:
        {pd.Series(profile['missing_percent']).to_string()}

        Duplicates: {profile['duplicates']}

        Numerical Columns Analysis:
        {pd.DataFrame(self.analyze_distributions()).to_string()}
        """

        return summary

# Usage
# df = pd.read_csv("data.csv")
# explorer = DataExplorer(df)
# print(explorer.get_summary())
```

### 2.2 ML Pipeline Template

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd

class MLPipeline:
    """Standard ML pipeline"""

    def __init__(self, random_state=42):
        self.random_state = random_state
        self.model = None
        self.scaler = StandardScaler()
        self.history = {}

    def prepare_data(self, X, y, test_size=0.2):
        """Train-test split and preprocessing"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.history["data_split"] = {
            "train_size": X_train.shape[0],
            "test_size": X_test.shape[0],
        }

        return X_train_scaled, X_test_scaled, y_train, y_test

    def train(self, X_train, y_train, model=None):
        """Train model"""
        self.model = model or RandomForestClassifier(random_state=self.random_state)
        self.model.fit(X_train, y_train)

        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5)
        self.history["cv_scores"] = {
            "mean": cv_scores.mean(),
            "std": cv_scores.std(),
            "scores": cv_scores.tolist()
        }

        return self.model

    def evaluate(self, X_test, y_test):
        """Evaluate model"""
        y_pred = self.model.predict(X_test)

        metrics = {
            "accuracy": (y_pred == y_test).mean(),
            "classification_report": classification_report(y_test, y_pred, output_dict=True),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
        }

        self.history["evaluation"] = metrics
        return metrics

    def get_feature_importance(self, feature_names):
        """Get feature importance if available"""
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            return pd.DataFrame({
                "feature": feature_names,
                "importance": importances
            }).sort_values("importance", ascending=False)
        return None

# Usage pattern
# pipeline = MLPipeline()
# X_train, X_test, y_train, y_test = pipeline.prepare_data(X, y)
# pipeline.train(X_train, y_train)
# metrics = pipeline.evaluate(X_test, y_test)
```

---

## 3. DATA ENGINEER CODE TEMPLATES

### 3.1 ETL Pipeline Template

```python
import logging
from typing import List, Callable, Any
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

class ETLPipeline:
    """Base ETL pipeline class"""

    def __init__(self, name: str):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.stages = []
        self.data = None

    def extract(self, source_func: Callable) -> Any:
        """Extract data from source"""
        logger.info(f"Extracting data for {self.name}")
        self.start_time = datetime.now()

        try:
            self.data = source_func()
            logger.info(f"Extracted {len(self.data)} rows")
            return self.data
        except Exception as e:
            logger.error(f"Extract failed: {e}")
            raise

    def transform(self, transform_func: Callable) -> Any:
        """Transform data"""
        logger.info("Transforming data")

        try:
            self.data = transform_func(self.data)
            logger.info(f"Transformed to {len(self.data)} rows")
            return self.data
        except Exception as e:
            logger.error(f"Transform failed: {e}")
            raise

    def load(self, load_func: Callable) -> bool:
        """Load data to destination"""
        logger.info("Loading data")

        try:
            load_func(self.data)
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()
            logger.info(f"Load completed in {duration:.2f} seconds")
            return True
        except Exception as e:
            logger.error(f"Load failed: {e}")
            raise

    def validate(self, validation_func: Callable) -> bool:
        """Validate data quality"""
        logger.info("Validating data")

        try:
            is_valid, issues = validation_func(self.data)
            if not is_valid:
                logger.warning(f"Validation issues: {issues}")
            return is_valid
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            raise

    def run(
        self,
        extract_func: Callable,
        transform_func: Callable,
        load_func: Callable,
        validate_func: Callable = None
    ):
        """Run full ETL pipeline"""
        try:
            self.extract(extract_func)
            self.transform(transform_func)

            if validate_func:
                if not self.validate(validate_func):
                    raise ValueError("Data validation failed")

            self.load(load_func)
            logger.info(f"Pipeline {self.name} completed successfully")

        except Exception as e:
            logger.error(f"Pipeline {self.name} failed: {e}")
            raise

# Usage pattern
# pipeline = ETLPipeline("sales_etl")
# pipeline.run(
#     extract_func=lambda: pd.read_csv("raw_sales.csv"),
#     transform_func=clean_and_transform,
#     load_func=lambda data: data.to_sql("sales", conn),
#     validate_func=validate_sales_data
# )
```

### 3.2 Data Quality Validation Framework

```python
from dataclasses import dataclass
from typing import List, Callable, Tuple
import pandas as pd

@dataclass
class ValidationRule:
    name: str
    description: str
    validator: Callable
    severity: str = "error"  # or "warning"

class DataValidator:
    """Data quality validation framework"""

    def __init__(self):
        self.rules: List[ValidationRule] = []
        self.results = {}

    def add_rule(self, rule: ValidationRule):
        """Add validation rule"""
        self.rules.append(rule)

    def add_null_check(self, column: str, allow_nulls: bool = False):
        """Add null check rule"""
        def validator(df):
            null_count = df[column].isnull().sum()
            if allow_nulls:
                return True, {"null_count": null_count}
            return null_count == 0, {"null_count": null_count}

        self.add_rule(ValidationRule(
            name=f"null_check_{column}",
            description=f"Check for null values in {column}",
            validator=validator
        ))

    def add_range_check(self, column: str, min_val, max_val):
        """Add range check rule"""
        def validator(df):
            out_of_range = ((df[column] < min_val) | (df[column] > max_val)).sum()
            return out_of_range == 0, {"out_of_range": out_of_range}

        self.add_rule(ValidationRule(
            name=f"range_check_{column}",
            description=f"Check {column} is between {min_val} and {max_val}",
            validator=validator
        ))

    def add_uniqueness_check(self, column: str):
        """Add uniqueness check rule"""
        def validator(df):
            duplicates = df[column].duplicated().sum()
            return duplicates == 0, {"duplicates": duplicates}

        self.add_rule(ValidationRule(
            name=f"unique_check_{column}",
            description=f"Check {column} has unique values",
            validator=validator
        ))

    def validate(self, df: pd.DataFrame) -> Tuple[bool, dict]:
        """Run all validation rules"""
        all_passed = True
        self.results = {}

        for rule in self.rules:
            try:
                passed, details = rule.validator(df)
                self.results[rule.name] = {
                    "passed": passed,
                    "details": details,
                    "severity": rule.severity
                }

                if not passed and rule.severity == "error":
                    all_passed = False

            except Exception as e:
                self.results[rule.name] = {
                    "passed": False,
                    "error": str(e),
                    "severity": rule.severity
                }
                all_passed = False

        return all_passed, self.results

    def get_report(self) -> str:
        """Generate validation report"""
        report = "=== DATA VALIDATION REPORT ===\n"

        for rule_name, result in self.results.items():
            status = "PASS" if result["passed"] else "FAIL"
            report += f"\n{rule_name}: {status}"
            if "details" in result:
                report += f" {result['details']}"

        return report

# Usage pattern
# validator = DataValidator()
# validator.add_null_check("email")
# validator.add_range_check("age", 0, 120)
# validator.add_uniqueness_check("user_id")
# is_valid, results = validator.validate(df)
```

---

## 4. DATA ANALYST CODE TEMPLATES

### 4.1 SQL Analysis Query Template

```sql
-- Multi-part SQL analysis template
-- ================================

-- Step 1: Data Overview
WITH data_overview AS (
    SELECT
        COUNT(*) as total_records,
        COUNT(DISTINCT user_id) as unique_users,
        MIN(date_column) as earliest_date,
        MAX(date_column) as latest_date
    FROM source_table
)

-- Step 2: Aggregation Analysis
, aggregated_metrics AS (
    SELECT
        DATE_TRUNC('month', date_column) as month,
        user_segment,
        COUNT(*) as transaction_count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount,
        COUNT(DISTINCT user_id) as unique_users
    FROM source_table
    WHERE date_column >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
    GROUP BY 1, 2
)

-- Step 3: Trend Analysis with Window Functions
, trend_analysis AS (
    SELECT
        month,
        user_segment,
        transaction_count,
        LAG(transaction_count) OVER (
            PARTITION BY user_segment
            ORDER BY month
        ) as prev_month_count,
        ((transaction_count - LAG(transaction_count) OVER (
            PARTITION BY user_segment
            ORDER BY month
        )) / LAG(transaction_count) OVER (
            PARTITION BY user_segment
            ORDER BY month
        ) * 100) as pct_change
    FROM aggregated_metrics
)

-- Step 4: Final Results
SELECT
    month,
    user_segment,
    transaction_count,
    total_amount,
    avg_amount,
    unique_users,
    pct_change
FROM trend_analysis
ORDER BY month DESC, user_segment;
```

### 4.2 Python Analysis Template

```python
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalysis:
    """Data analysis workflow"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.insights = {}

    def segment_analysis(self, segment_col: str, value_col: str):
        """Analyze by segments"""
        segments = self.df.groupby(segment_col)[value_col].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).round(2)

        self.insights["segments"] = segments
        return segments

    def time_series_analysis(self, date_col: str, metric_col: str, freq: str = 'D'):
        """Analyze trends over time"""
        ts_data = self.df.set_index(date_col)[metric_col].resample(freq).agg([
            'sum', 'mean', 'count'
        ])

        self.insights["time_series"] = ts_data
        return ts_data

    def correlation_analysis(self, numeric_cols: list = None):
        """Analyze correlations"""
        if numeric_cols is None:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        corr_matrix = self.df[numeric_cols].corr()

        # Find significant correlations
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    high_corr.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_val
                    })

        self.insights["high_correlations"] = high_corr
        return corr_matrix, high_corr

    def hypothesis_test(self, group_col: str, value_col: str):
        """Perform t-test between groups"""
        groups = self.df[group_col].unique()

        if len(groups) == 2:
            group1 = self.df[self.df[group_col] == groups[0]][value_col]
            group2 = self.df[self.df[group_col] == groups[1]][value_col]

            t_stat, p_value = stats.ttest_ind(group1, group2)

            result = {
                'test': 'independent t-test',
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }

            self.insights["hypothesis_test"] = result
            return result

    def visualization_summary(self):
        """Generate summary visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Distribution plot
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols[:2]:
            axes[0, 0].hist(self.df[col], bins=30, alpha=0.7, label=col)
        axes[0, 0].set_title("Distribution")
        axes[0, 0].legend()

        # Correlation heatmap
        corr_cols = min(5, len(numeric_cols))
        sns.heatmap(
            self.df[numeric_cols[:corr_cols]].corr(),
            ax=axes[0, 1],
            cmap='coolwarm'
        )
        axes[0, 1].set_title("Correlations")

        # Box plot
        if len(self.df.select_dtypes(include=['object']).columns) > 0:
            cat_col = self.df.select_dtypes(include=['object']).columns[0]
            self.df.boxplot(column=numeric_cols[0], by=cat_col, ax=axes[1, 0])
            axes[1, 0].set_title(f"{numeric_cols[0]} by {cat_col}")

        # Summary stats table
        axes[1, 1].axis('off')
        summary_text = self.df.describe().to_string()
        axes[1, 1].text(0.1, 0.9, summary_text, transform=axes[1, 1].transAxes,
                       fontsize=8, verticalalignment='top', family='monospace')

        plt.tight_layout()
        return fig

# Usage
# df = pd.read_csv("sales_data.csv")
# analysis = DataAnalysis(df)
# segments = analysis.segment_analysis("region", "revenue")
# analysis.visualization_summary().savefig("analysis.png")
```

---

## 5. PROMPT ENGINEERING CODE TEMPLATES

### 5.1 Prompt Template Engine

```python
from string import Template
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class PromptTemplate:
    """Structured prompt template"""

    system_instruction: str
    task_description: str
    context_template: Optional[str] = None
    examples: List[Dict[str, str]] = None
    constraints: List[str] = None
    output_format: Optional[str] = None

    def render(self, **variables) -> str:
        """Render template with variables"""

        parts = [
            f"SYSTEM: {self.system_instruction}",
            f"\nTASK: {self.task_description}"
        ]

        if self.context_template:
            context = Template(self.context_template).substitute(**variables)
            parts.append(f"\nCONTEXT:\n{context}")

        if self.examples:
            parts.append("\nEXAMPLES:")
            for i, example in enumerate(self.examples, 1):
                parts.append(f"\nExample {i}:")
                for key, value in example.items():
                    parts.append(f"  {key}: {value}")

        if self.constraints:
            parts.append("\nCONSTRAINTS:")
            for constraint in self.constraints:
                parts.append(f"  - {constraint}")

        if self.output_format:
            parts.append(f"\nOUTPUT FORMAT:\n{self.output_format}")

        return "\n".join(parts)

# Examples

# 1. Code Generation Prompt
code_gen_prompt = PromptTemplate(
    system_instruction="You are an expert Python developer",
    task_description="Generate Python code for the given task",
    examples=[
        {
            "input": "Sort a list of dictionaries by age",
            "output": "people.sort(key=lambda x: x['age'])"
        }
    ],
    constraints=[
        "Use clear variable names",
        "Include error handling",
        "Add comments for complex logic"
    ],
    output_format="```python\n[code]\n```"
)

# 2. Analysis Prompt
analysis_prompt = PromptTemplate(
    system_instruction="You are a data analysis expert",
    task_description="Analyze the given data and provide insights",
    context_template="Data shape: $rows rows, $cols columns\nData sample: $sample",
    constraints=[
        "Base insights on the actual data",
        "Highlight anomalies",
        "Suggest next steps"
    ],
    output_format="""
    FINDINGS:
    - [Key finding 1]
    - [Key finding 2]

    ANOMALIES:
    - [Anomaly 1]

    RECOMMENDATIONS:
    - [Next step 1]
    """
)

# Usage
# prompt = code_gen_prompt.render()
# response = api_client.generate(prompt)
```

### 5.2 Few-Shot Example Generator

```python
from typing import List, Dict, Tuple
from itertools import combinations

class FewShotGenerator:
    """Generate effective few-shot examples"""

    def __init__(self, examples: List[Dict[str, str]]):
        self.examples = examples

    def select_diverse_examples(self, k: int = 3) -> List[Dict[str, str]]:
        """Select diverse examples for few-shot"""

        if len(self.examples) <= k:
            return self.examples

        # Simple diversity: select from different parts of list
        indices = []
        step = len(self.examples) // k

        for i in range(k):
            indices.append(min(i * step, len(self.examples) - 1))

        return [self.examples[i] for i in indices]

    def format_examples(self, examples: List[Dict], format_str: str = "Q: {input}\nA: {output}") -> str:
        """Format examples as string"""
        formatted = []
        for example in examples:
            formatted.append(format_str.format(**example))
        return "\n\n".join(formatted)

    def include_edge_cases(self) -> List[Dict[str, str]]:
        """Add edge cases to examples"""
        edge_cases = [
            ex for ex in self.examples
            if any(keyword in ex.get('input', '').lower()
                   for keyword in ['none', 'empty', 'invalid', 'error'])
        ]
        return edge_cases or []

# Usage pattern
examples = [
    {"input": "What is 2+2?", "output": "4"},
    {"input": "What is 10*5?", "output": "50"},
    # ... more examples
]

generator = FewShotGenerator(examples)
selected = generator.select_diverse_examples(k=3)
formatted = generator.format_examples(selected)
final_prompt = f"Here are examples:\n\n{formatted}\n\nNow solve: [NEW PROBLEM]"
```

---

## 6. COMMON PATTERNS & UTILITIES

### 6.1 Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logging(name: str, log_level=logging.INFO) -> logging.Logger:
    """Setup comprehensive logging"""

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # File handler
    log_filename = f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )

    # Console handler
    console_handler = logging.StreamHandler()

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Usage
# logger = setup_logging(__name__)
# logger.info("Process started")
```

### 6.2 Configuration Management

```python
import os
from typing import Any
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration"""

    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    api_key: str = os.getenv("API_KEY", "")
    db_url: str = os.getenv("DB_URL", "")
    batch_size: int = int(os.getenv("BATCH_SIZE", "100"))

    @classmethod
    def from_env(cls) -> "Config":
        """Load config from environment"""
        return cls()

    def validate(self) -> bool:
        """Validate configuration"""
        required = ["api_key", "db_url"]
        for field in required:
            if not getattr(self, field):
                raise ValueError(f"Missing required config: {field}")
        return True

# Usage
# config = Config.from_env()
# config.validate()
```

### 6.3 Performance Timing Decorator

```python
import time
from functools import wraps
from typing import Callable, Any

def time_it(func: Callable) -> Callable:
    """Decorator to time function execution"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start

        print(f"{func.__name__} took {elapsed:.2f} seconds")
        return result

    return wrapper

# Usage
# @time_it
# def expensive_operation():
#     time.sleep(2)
```

---

## 7. INTEGRATION PATTERNS

### 7.1 Combined AI Agent + Data Pipeline

```python
class AIAugmentedETL:
    """ETL pipeline enhanced with AI"""

    def __init__(self, etl_pipeline, ai_client):
        self.etl = etl_pipeline
        self.ai = ai_client

    def transform_with_ai(self, data):
        """Use AI for intelligent transformation"""

        # Get data insights
        insights_prompt = f"""
        Analyze this data and identify transformation opportunities:
        {data.head().to_string()}

        Suggest data cleaning and transformation steps.
        """

        suggestions = self.ai.generate(insights_prompt)

        # Apply suggestions
        # (In real scenario, would parse and apply)

        return data

    def validate_with_ai(self, data):
        """Use AI for quality validation"""

        validation_prompt = f"""
        Review this dataset for data quality issues:
        {data.describe().to_string()}

        Identify any anomalies or data quality concerns.
        """

        issues = self.ai.generate(validation_prompt)
        return issues
```

---

## BEST PRACTICES CHECKLIST

### For Each Code Template:
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Type hints included
- [ ] Docstrings provided
- [ ] Example usage shown
- [ ] Configuration externalized
- [ ] Performance considerations noted
- [ ] Security best practices followed
- [ ] Testing approach outlined
- [ ] Documentation complete

### For Agent Usage:
- [ ] Template customized for specific use case
- [ ] Input validation added
- [ ] Output formatting ensured
- [ ] Error messages user-friendly
- [ ] Performance optimized
- [ ] Monitoring/logging implemented
- [ ] Documentation provided
- [ ] Examples shown
- [ ] Edge cases handled
- [ ] Feedback mechanism included

---

## CONCLUSION

These code templates and patterns provide concrete implementations that Claude Code agents can:

1. **Reference** - When explaining concepts
2. **Adapt** - For specific user scenarios
3. **Extend** - By adding custom functionality
4. **Teach** - Through annotated examples
5. **Review** - For best practices and quality

Each template follows industry best practices and includes:
- Clear structure and organization
- Comprehensive error handling
- Logging and monitoring
- Type hints for clarity
- Docstrings for documentation
- Practical usage patterns
