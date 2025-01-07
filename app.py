import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from astrapy import DataAPIClient
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

client = DataAPIClient(os.getenv("ASTRA_TOKEN"))
db = client.get_database_by_api_endpoint(
    "https://af83915c-c251-4610-bef2-28af68c893bc-us-east1.apps.astra.datastax.com",
    keyspace="social_media_analytics",
)

def get_engagement_metrics():
    collection = db["social_media_posts"]
    posts = collection.find({})
    
    df = pd.DataFrame(posts)
    
    metrics = df.groupby('post_type').agg({
        'likes': 'mean',
        'shares': 'mean',
        'comments': 'mean',
        'engagement_rate': 'mean'
    }).round(2)
    
    return metrics

def generate_insights(metrics_df):

    metrics_text = metrics_df.to_string()

    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="mixtral-8x7b-32768"
    )
    
    prompt = ChatPromptTemplate.from_template("""
    Analyze the following social media engagement metrics and provide 3-4 key insights:
    
    {metrics}
    
    Focus on:
    1. Comparing performance across post types
    2. Identifying the most effective content format
    3. Suggesting ways to improve engagement
    
    Please provide specific numbers and percentages in your analysis.
    """)
    
    chain = prompt | llm
    
    response = chain.invoke({"metrics": metrics_text})
    return response.content

def main():
    st.title("Social Media Analytics Dashboard")
    
    metrics_df = get_engagement_metrics()
    st.subheader("Average Engagement Metrics by Post Type")
    st.dataframe(metrics_df)

    st.subheader("AI-Generated Insights")
    if st.button("Generate Insights"):
        with st.spinner("Generating insights using Groq LLM..."):
            insights = generate_insights(metrics_df)
            st.write(insights)

    st.subheader("Engagement Visualization")
    chart_data = metrics_df.reset_index()
    st.bar_chart(chart_data.set_index('post_type')['engagement_rate'])

if __name__ == "__main__":
    main()