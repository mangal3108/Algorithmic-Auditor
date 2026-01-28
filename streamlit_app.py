import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from io import StringIO

st.set_page_config(page_title="Algorithmic Auditor", layout="wide")

# ============================================================================
# CONFIGURATION & STATE
# ============================================================================

# Backend URL - set to localhost for local development
BACKEND_URL = "http://localhost:8000"

# Initialize session state
if "biased_metrics" not in st.session_state:
    st.session_state.biased_metrics = None
if "mitigated_metrics" not in st.session_state:
    st.session_state.mitigated_metrics = None
if "upload_status" not in st.session_state:
    st.session_state.upload_status = None

# ============================================================================
# TITLE & DESCRIPTION
# ============================================================================

st.title("🔍 Algorithmic Auditor")
st.markdown("Detect and mitigate bias in machine learning models")

# ============================================================================
# SIDEBAR - CONFIGURATION
# ============================================================================

with st.sidebar:
    st.header("⚙️ Configuration")
    backend_url_input = st.text_input("Backend URL", value=BACKEND_URL)
    if backend_url_input:
        BACKEND_URL = backend_url_input
    
    n_samples = st.slider("Number of Samples", min_value=100, max_value=10000, value=3000, step=100)

# ============================================================================
# MAIN LAYOUT - TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["📊 Data Upload", "🤖 Model Training", "📈 Results"])

# ============================================================================
# TAB 1: DATA UPLOAD
# ============================================================================

with tab1:
    st.header("Upload Your Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Option 1: Upload CSV File")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            # Read and display the file
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ File loaded! Shape: {df.shape}")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Upload to backend
            if st.button("Upload to Backend", key="upload_btn"):
                with st.spinner("Uploading..."):
                    try:
                        files = {"file": uploaded_file.getvalue()}
                        response = requests.post(
                            f"{BACKEND_URL}/upload",
                            files={"file": ("data.csv", uploaded_file.getvalue())}
                        )
                        if response.status_code == 200:
                            st.session_state.upload_status = f"✅ Uploaded! ({response.json().get('rows', '?')} rows)"
                            st.success(st.session_state.upload_status)
                        else:
                            st.error(f"Upload failed: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.subheader("Option 2: Paste CSV Data")
        csv_text = st.text_area("Paste CSV data here", height=150)
        if csv_text:
            try:
                df_pasted = pd.read_csv(StringIO(csv_text))
                st.success(f"✅ Parsed! Shape: {df_pasted.shape}")
                st.dataframe(df_pasted.head(), use_container_width=True)
                
                if st.button("Upload Pasted Data", key="upload_paste_btn"):
                    with st.spinner("Uploading..."):
                        try:
                            response = requests.post(
                                f"{BACKEND_URL}/upload",
                                files={"file": ("data.csv", csv_text)}
                            )
                            if response.status_code == 200:
                                st.session_state.upload_status = f"✅ Uploaded! ({response.json().get('rows', '?')} rows)"
                                st.success(st.session_state.upload_status)
                            else:
                                st.error(f"Upload failed: {response.text}")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            except Exception as e:
                st.error(f"Invalid CSV format: {str(e)}")
    
    # Display current upload status
    if st.session_state.upload_status:
        st.info(st.session_state.upload_status)
    
    # Example data generator
    st.markdown("---")
    st.subheader("💡 Generate Sample Data")
    if st.button("Generate Synthetic Dataset"):
        # Create a simple synthetic dataset
        np.random.seed(42)
        n = 500
        df_synthetic = pd.DataFrame({
            'age': np.random.randint(20, 70, n),
            'income': np.random.choice(['low', 'high'], n, p=[0.6, 0.4]),
            'gender': np.random.choice(['Male', 'Female'], n),
            'education': np.random.choice(['HS', 'Bachelor', 'Master'], n),
            'approved': np.random.choice([0, 1], n)
        })
        
        csv_content = df_synthetic.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample CSV",
            data=csv_content,
            file_name="synthetic_data.csv",
            mime="text/csv"
        )
        
        st.dataframe(df_synthetic.head(10), use_container_width=True)
        st.write(f"Dataset shape: {df_synthetic.shape}")

# ============================================================================
# TAB 2: MODEL TRAINING
# ============================================================================

with tab2:
    st.header("Train Models")
    
    col1, col2 = st.columns(2)
    
    # Train Biased Model
    with col1:
        st.subheader("1️⃣ Train Biased Model")
        st.markdown("Trains a standard Decision Tree Classifier without fairness constraints")
        
        if st.button("🚀 Train Biased Model", key="train_biased_btn"):
            with st.spinner("Training biased model..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/train/biased",
                        json={"n_samples": n_samples}
                    )
                    if response.status_code == 200:
                        st.session_state.biased_metrics = response.json()
                        st.success("✅ Biased model trained!")
                    else:
                        st.error(f"Training failed: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Train Mitigated Model
    with col2:
        st.subheader("2️⃣ Train Mitigated Model")
        st.markdown("Trains a Decision Tree with fairness constraints (Demographic Parity)")
        
        if st.button("🚀 Train Mitigated Model", key="train_mitigated_btn"):
            with st.spinner("Training mitigated model..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/train/mitigated",
                        json={"n_samples": n_samples}
                    )
                    if response.status_code == 200:
                        st.session_state.mitigated_metrics = response.json()
                        st.success("✅ Mitigated model trained!")
                    else:
                        st.error(f"Training failed: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Training info
    st.markdown("---")
    st.info(f"**Current Configuration:** {n_samples} samples | Backend: {BACKEND_URL}")

# ============================================================================
# TAB 3: RESULTS COMPARISON
# ============================================================================

with tab3:
    st.header("📊 Model Comparison")
    
    # Check if we have metrics
    if st.session_state.biased_metrics is None and st.session_state.mitigated_metrics is None:
        st.warning("⚠️ Train models first to see results!")
    else:
        # Create comparison data
        metrics_data = []
        
        if st.session_state.biased_metrics:
            metrics_data.append({
                "Model": "Biased (Baseline)",
                "Accuracy": st.session_state.biased_metrics.get("accuracy", 0),
                "Bias Gap": st.session_state.biased_metrics.get("bias_gap", 0),
                "Male Selection Rate": st.session_state.biased_metrics.get("male_rate", 0),
                "Female Selection Rate": st.session_state.biased_metrics.get("female_rate", 0)
            })
        
        if st.session_state.mitigated_metrics:
            metrics_data.append({
                "Model": "Mitigated (Fair)",
                "Accuracy": st.session_state.mitigated_metrics.get("accuracy", 0),
                "Bias Gap": st.session_state.mitigated_metrics.get("bias_gap", 0),
                "Male Selection Rate": st.session_state.mitigated_metrics.get("male_rate", 0),
                "Female Selection Rate": st.session_state.mitigated_metrics.get("female_rate", 0)
            })
        
        df_comparison = pd.DataFrame(metrics_data)
        
        # Display metrics table
        st.subheader("Detailed Metrics")
        st.dataframe(df_comparison, use_container_width=True)
        
        # Create visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Accuracy comparison
            fig_accuracy = go.Figure()
            for idx, row in df_comparison.iterrows():
                fig_accuracy.add_trace(go.Bar(
                    x=[row["Model"]],
                    y=[row["Accuracy"]],
                    name="Accuracy",
                    text=f'{row["Accuracy"]:.3f}',
                    textposition='auto',
                ))
            fig_accuracy.update_layout(
                title="Model Accuracy Comparison",
                yaxis_title="Accuracy",
                xaxis_title="Model",
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig_accuracy, use_container_width=True)
        
        with col2:
            # Bias gap comparison
            fig_bias = go.Figure()
            for idx, row in df_comparison.iterrows():
                fig_bias.add_trace(go.Bar(
                    x=[row["Model"]],
                    y=[abs(row["Bias Gap"])],
                    name="Bias Gap (|DPD|)",
                    text=f'{abs(row["Bias Gap"]):.3f}',
                    textposition='auto',
                ))
            fig_bias.update_layout(
                title="Fairness: Demographic Parity Difference (Lower is Better)",
                yaxis_title="|Demographic Parity Difference|",
                xaxis_title="Model",
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig_bias, use_container_width=True)
        
        # Selection rates by gender
        st.subheader("Selection Rates by Gender")
        col3, col4 = st.columns(2)
        
        with col3:
            fig_male = go.Figure()
            for idx, row in df_comparison.iterrows():
                fig_male.add_trace(go.Bar(
                    x=[row["Model"]],
                    y=[row["Male Selection Rate"]],
                    text=f'{row["Male Selection Rate"]:.3f}',
                    textposition='auto',
                ))
            fig_male.update_layout(
                title="Male Selection Rate",
                yaxis_title="Selection Rate",
                yaxis=dict(range=[0, 1]),
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig_male, use_container_width=True)
        
        with col4:
            fig_female = go.Figure()
            for idx, row in df_comparison.iterrows():
                fig_female.add_trace(go.Bar(
                    x=[row["Model"]],
                    y=[row["Female Selection Rate"]],
                    text=f'{row["Female Selection Rate"]:.3f}',
                    textposition='auto',
                ))
            fig_female.update_layout(
                title="Female Selection Rate",
                yaxis_title="Selection Rate",
                yaxis=dict(range=[0, 1]),
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig_female, use_container_width=True)
        
        # Summary insights
        st.markdown("---")
        st.subheader("📝 Key Insights")
        
        if st.session_state.biased_metrics and st.session_state.mitigated_metrics:
            acc_diff = st.session_state.mitigated_metrics["accuracy"] - st.session_state.biased_metrics["accuracy"]
            bias_reduction = abs(st.session_state.biased_metrics["bias_gap"]) - abs(st.session_state.mitigated_metrics["bias_gap"])
            
            col_i1, col_i2, col_i3 = st.columns(3)
            
            with col_i1:
                st.metric("Accuracy Change", f"{acc_diff:+.3f}", delta=f"{acc_diff*100:+.1f}%")
            
            with col_i2:
                st.metric("Bias Gap Reduction", f"{bias_reduction:.3f}", delta=f"{bias_reduction*100:+.1f}%")
            
            with col_i3:
                fairness_improved = bias_reduction > 0
                status = "✅ Improved" if fairness_improved else "⚠️ Degraded"
                st.metric("Fairness Status", status)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
### About Algorithmic Auditor
This tool helps detect and mitigate bias in machine learning models by comparing:
- **Biased Model**: Standard Decision Tree Classifier (baseline)
- **Mitigated Model**: Decision Tree with fairness constraints (Demographic Parity)

**Key Metrics:**
- **Accuracy**: Predictive performance
- **Demographic Parity Difference (DPD)**: Measures fairness gap between groups
- **Selection Rate**: Proportion of positive predictions per demographic group
""")
