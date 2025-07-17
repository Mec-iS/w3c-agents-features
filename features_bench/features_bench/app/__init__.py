"""
An app to visualise outputs from the translation process
"""

import re
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st


def parse_log_file(log_content):
    """Parse the log file to extract question-response pairs with metadata."""
    # Adjusted regex pattern to correctly capture question and response pairs
    pattern = re.compile(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+) \[info[ ]*\] One shot Question:[ ]+component=bspl_to_nl/translate_one_shot.py model=([\w\.]+) question='([^']+)' question_n=(\d+)"  # Question line
        r".*?"
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+) \[info[ ]*\] One shot Response:[ ]+component=bspl_to_nl/translate_one_shot.py model=([\w\.]+) question_n=(\d+) response='([^']+)'",  # Response line
        re.DOTALL,
    )

    matches = pattern.findall(log_content)

    data = []
    for match in matches:
        (
            question_time,
            question_model,
            question_text,
            question_n,
            response_time,
            response_model,
            response_n,
            response_text,
        ) = match

        # Only accept matched pairs where question_n == response_n and question_model == response_model
        if question_n != response_n or question_model != response_model:
            continue

        try:
            q_time = datetime.strptime(question_time, "%Y-%m-%d %H:%M:%S.%f")
            r_time = datetime.strptime(response_time, "%Y-%m-%d %H:%M:%S.%f")
        except Exception:
            continue

        response_duration = (r_time - q_time).total_seconds()

        data.append(
            {
                "question_n": int(question_n),
                "model": question_model,
                "question": question_text,
                "response": response_text,
                "question_time": q_time,
                "response_time": r_time,
                "response_duration": response_duration,
            }
        )

    return pd.DataFrame(data)


def extract_bspl_info(question_text):
    """Extract BSPL protocol information from question text."""

    # Extract protocol name
    protocol_match = re.search(r"^(\w+)\s*\{", question_text)
    protocol_name = protocol_match.group(1) if protocol_match else "Unknown"

    # Extract roles
    roles_match = re.search(r"roles\s+([^}]+?)(?=\s+parameters)", question_text)
    roles = roles_match.group(1).strip() if roles_match else ""

    # Extract parameters
    params_match = re.search(r"parameters\s+([^}]+?)(?=\s+\w+\s*→)", question_text)
    parameters = params_match.group(1).strip() if params_match else ""

    return {"protocol_name": protocol_name, "roles": roles, "parameters": parameters}


def main():
    st.set_page_config(page_title="BSPL Translation Log Visualizer", page_icon="📊", layout="wide")

    st.title("🔍 BSPL Translation Log Visualizer")
    st.markdown(
        "### Analyze question-response pairs from BSPL to Natural Language translation logs"
    )

    # Sidebar for file upload
    st.sidebar.header("📁 Upload Log File")
    uploaded_file = st.sidebar.file_uploader("Choose a log file", type=["log", "txt"])

    if uploaded_file is not None:
        # Read the uploaded file
        log_content = str(uploaded_file.read(), "utf-8")

        # Parse the log file
        with st.spinner("Parsing log file..."):
            df = parse_log_file(log_content)

        if df.empty:
            st.error(
                "No question-response pairs found in the log file. Please check the file format."
            )
            return

        # Extract BSPL information
        bspl_info = df["question"].apply(extract_bspl_info)
        df["protocol_name"] = [info["protocol_name"] for info in bspl_info]
        df["roles"] = [info["roles"] for info in bspl_info]
        df["parameters"] = [info["parameters"] for info in bspl_info]

        # Display summary statistics
        st.header("📈 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Questions", len(df))

        with col2:
            st.metric("Unique Models", df["model"].nunique())

        with col3:
            st.metric("Avg Response Time", f"{df['response_duration'].mean():.2f}s")

        with col4:
            st.metric("Unique Protocols", df["protocol_name"].nunique())

        # Model performance visualization
        st.header("⚡ Model Performance")

        col1, col2 = st.columns(2)

        with col1:
            # Response time by model
            fig_time = px.box(
                df,
                x="model",
                y="response_duration",
                title="Response Time by Model",
                labels={"response_duration": "Response Time (seconds)", "model": "Model"},
            )
            st.plotly_chart(fig_time, use_container_width=True)

        with col2:
            # Questions per model
            model_counts = df["model"].value_counts()
            fig_count = px.bar(
                x=model_counts.index,
                y=model_counts.values,
                title="Questions per Model",
                labels={"x": "Model", "y": "Number of Questions"},
            )
            st.plotly_chart(fig_count, use_container_width=True)

        # Interactive question-response viewer
        st.header("💬 Question-Response Pairs")

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            selected_model = st.selectbox("Filter by Model", ["All"] + list(df["model"].unique()))
        with col2:
            selected_protocol = st.selectbox(
                "Filter by Protocol", ["All"] + list(df["protocol_name"].unique())
            )

        # Apply filters
        filtered_df = df.copy()
        if selected_model != "All":
            filtered_df = filtered_df[filtered_df["model"] == selected_model]
        if selected_protocol != "All":
            filtered_df = filtered_df[filtered_df["protocol_name"] == selected_protocol]

        # Display filtered results
        for idx, row in filtered_df.iterrows():
            with st.expander(
                f"Question {row['question_n']} - {row['protocol_name']} ({row['model']})"
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📝 BSPL Question")
                    st.code(row["question"], language="text")

                    st.subheader("ℹ️ Metadata")
                    st.write(f"**Model:** {row['model']}")
                    st.write(f"**Protocol:** {row['protocol_name']}")
                    st.write(f"**Roles:** {row['roles']}")
                    st.write(f"**Parameters:** {row['parameters']}")
                    st.write(f"**Response Time:** {row['response_duration']:.2f}s")

                with col2:
                    st.subheader("🤖 Natural Language Response")
                    st.write(row["response"])

        # Raw data view
        st.header("📊 Raw Data")
        if st.checkbox("Show raw data"):
            st.dataframe(df)

        # Download processed data
        st.header("💾 Export Data")
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="bspl_translation_analysis.csv",
            mime="text/csv",
        )

    else:
        st.info("👆 Please upload a log file to begin analysis")

        # Show example of expected log format
        st.header("📋 Expected Log Format")
        st.markdown("""
        The log file should contain lines with the following pattern:
        ```
        2025-07-17 10:52:34.422745 [info ] One shot Question: component=bspl_to_nl/translate_one_shot.py model=llama3.2 question='Pay { roles Payer , Payee parameters in ID key , in amount Payer → Payee : payM [ in ID , in amount ]}' question_n=0
        ...
        2025-07-17 10:52:34.938353 [info ] One shot Response: component=bspl_to_nl/translate_one_shot.py model=llama3.2 question_n=0 response='The buyer sends a payment request to the seller with item ID and amount.'
        ```
        """)


if __name__ == "__main__":
    main()
