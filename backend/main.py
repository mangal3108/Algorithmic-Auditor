from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import io
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from fairlearn.metrics import MetricFrame, selection_rate, demographic_parity_difference
from fairlearn.reductions import ExponentiatedGradient, DemographicParity

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- GLOBAL STORAGE ---
# In a real app, use a database. For this demo, global variables are fine.
data_store = {
    "X": None,
    "y": None,
    "sensitive": None,
    "is_uploaded": False
}

# --- HELPER: SYNTHETIC DATA (Backup) ---
def generate_synthetic_data(n=2000):
    X = pd.DataFrame(np.random.rand(n, 5), columns=['A','B','C','D','E'])
    bias = np.random.rand(n)
    sex = np.random.choice([0, 1], n) # 0=Male, 1=Female
    score = X['A'] + X['B'] + (1 - sex) * 0.3 
    y = (score > 1.0).astype(int)
    return X, y, pd.Series(sex).map({0: 'Male', 1: 'Female'})

# --- HELPER: PROCESS UPLOADED DATA ---
def process_dataframe(df):
    # 1. Clean Data
    df = df.dropna()
    
    # 2. Identify Sensitive Column (Simple Auto-detection)
    possible_sensitive = ['sex', 'gender', 'race', 'ethnicity', 'age']
    sensitive_col = next((col for col in df.columns if col.lower() in possible_sensitive), None)
    
    if not sensitive_col:
        # Fallback: Pick first text-based column
        sensitive_col = df.select_dtypes(include=['object', 'category']).columns[0]

    # 3. Identify Target Column (Assume it's the last one)
    target_col = df.columns[-1]

    # 4. Split and Encode
    y = df[target_col]
    X = df.drop(columns=[target_col, sensitive_col])
    sensitive = df[sensitive_col]

    # Encode Categorical Data to Numbers
    le = LabelEncoder()
    # Encode y if it's text (e.g., "Yes"/"No")
    if y.dtype == 'object':
        y = le.fit_transform(y)
    
    # One-hot encode X (features)
    X = pd.get_dummies(X)

    return X, y, sensitive

class TrainRequest(BaseModel):
    n_samples: int = 2000

@app.get("/")
def home():
    return {"message": "Backend Ready"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Process it
        X, y, sensitive = process_dataframe(df)
        
        # Save to Global Store
        data_store["X"] = X
        data_store["y"] = y
        data_store["sensitive"] = sensitive
        data_store["is_uploaded"] = True
        
        return {"message": "File processed", "rows": len(df), "sensitive_col": sensitive.name}
    except Exception as e:
        return {"error": str(e)}

@app.post("/train/biased")
def train_biased(req: TrainRequest):
    # USE UPLOADED DATA IF AVAILABLE, ELSE SYNTHETIC
    if data_store["is_uploaded"]:
        X, y, sex = data_store["X"], data_store["y"], data_store["sensitive"]
        # Resample to requested size if needed
        if len(X) > req.n_samples:
             X = X.sample(n=req.n_samples, random_state=42)
             y = y.loc[X.index]
             sex = sex.loc[X.index]
    else:
        X, y, sex = generate_synthetic_data(req.n_samples)

    X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(X, y, sex, test_size=0.3)
    
    model = DecisionTreeClassifier(max_depth=5)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    try:
        gap = demographic_parity_difference(y_test, y_pred, sensitive_features=s_test)
        frame = MetricFrame(metrics=selection_rate, y_true=y_test, y_pred=y_pred, sensitive_features=s_test)
        rates = frame.by_group.to_dict()
        # Handle cases where keys might be 0/1 instead of strings
        female_rate = rates.get('Female', rates.get(1, 0.0))
        male_rate = rates.get('Male', rates.get(0, 0.0))
    except:
        gap = 0.0
        female_rate = 0.0
        male_rate = 0.0

    return {
        "accuracy": float(acc),
        "bias_gap": float(gap),
        "female_rate": float(female_rate),
        "male_rate": float(male_rate)
    }

@app.post("/train/mitigated")
def train_mitigated(req: TrainRequest):
    if data_store["is_uploaded"]:
        X, y, sex = data_store["X"], data_store["y"], data_store["sensitive"]
        if len(X) > req.n_samples:
             X = X.sample(n=req.n_samples, random_state=42)
             y = y.loc[X.index]
             sex = sex.loc[X.index]
    else:
        X, y, sex = generate_synthetic_data(req.n_samples)

    X_train, X_test, y_train, y_test, s_train, s_test = train_test_split(X, y, sex, test_size=0.3)
    
    mitigator = ExponentiatedGradient(
        estimator=DecisionTreeClassifier(max_depth=5),
        constraints=DemographicParity()
    )
    mitigator.fit(X_train, y_train, sensitive_features=s_train)
    y_pred = mitigator.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    try:
        gap = demographic_parity_difference(y_test, y_pred, sensitive_features=s_test)
        frame = MetricFrame(metrics=selection_rate, y_true=y_test, y_pred=y_pred, sensitive_features=s_test)
        rates = frame.by_group.to_dict()
        female_rate = rates.get('Female', rates.get(1, 0.0))
        male_rate = rates.get('Male', rates.get(0, 0.0))
    except:
        gap = 0.0
        female_rate = 0.0
        male_rate = 0.0

    return {
        "accuracy": float(acc),
        "bias_gap": float(gap),
        "female_rate": float(female_rate),
        "male_rate": float(male_rate)
    }