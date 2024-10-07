import pandas as pd

data = {
    'Feature': [
        'Purpose',
        'Primary Use Cases',
        'Data Processing Engine',
        'Data Transformation Capabilities',
        'Support for Python and Advanced Libraries',
        'Machine Learning Support',
        'Collaboration Features',
        'Integration with Other Azure Services',
        'Scalability',
        'Complex Data Processing (e.g., NLP, Simulations)',
        'User Interface',
        'Cost Structure',
        'Maturity and Industry Adoption'
    ],
    'Azure Data Factory (ADF)': [
        'Data integration and orchestration service',
        'ETL/ELT pipelines, data movement, and basic data transformation',
        'Orchestrates external compute (e.g., Azure HDInsight, Azure Databricks)',
        'Mapping Data Flows for visual data transformation; limited complex transformations',
        'Limited; custom activities can run Python scripts via Azure Batch or Azure Functions',
        'Not designed for machine learning workloads',
        'Limited collaboration; focuses on pipeline management',
        'Integrates with various Azure data stores and compute services',
        'Scales for data movement and orchestration needs',
        'Not suitable for complex data processing or simulations',
        'Visual interface for designing and managing pipelines',
        'Pay-as-you-go based on pipeline activities and data movement',
        'Mature service widely used for ETL and data integration tasks'
    ],
    'Azure Synapse Analytics': [
        'Integrated analytics platform combining data warehousing and big data analytics',
        'Data warehousing, big data analytics, integrated SQL and Spark processing',
        'Built-in SQL pools (dedicated and serverless), Spark pools',
        'Advanced transformations using T-SQL, Spark SQL, and notebooks',
        'Supports Python in Spark pools; may have limitations with library support',
        'Basic ML support via Spark MLlib; integration with Azure Machine Learning',
        'Basic collaboration through shared workspaces and notebooks',
        'Deep integration with Azure Data Lake Storage, Azure SQL Database, Power BI, and others',
        'Scales for large-scale analytics and data warehousing workloads',
        'Can perform complex processing but may have limitations in library support',
        'Integrated workspace with SQL editor, Spark notebooks, and pipelines',
        'Costs associated with compute resources (SQL pools, Spark pools) and storage',
        'Emerging platform with growing adoption; combines mature services (SQL DW) with new features'
    ],
    'Azure Databricks': [
        'Collaborative platform for big data analytics, data science, and machine learning',
        'Advanced analytics, data engineering, data science, machine learning, complex data processing',
        'Optimized Apache Spark engine',
        'Complex transformations using Python, Scala, R, SQL within notebooks',
        'Full support for Python and extensive libraries (Pandas, NumPy, SimPy, NLP libraries)',
        'Extensive ML support; integrates with MLflow, supports deep learning frameworks',
        'Advanced collaboration with interactive notebooks, real-time co-authoring, version control integration',
        'Integrates seamlessly with Azure Data Lake Storage, Azure SQL Database, Power BI, and more',
        'Highly scalable for big data processing and machine learning workloads',
        'Ideal for complex data processing, simulations, NLP tasks with full library support',
        'Collaborative notebooks supporting Python, Scala, SQL, R with rich visualization',
        'Costs based on compute usage (Databricks Units) and cluster uptime; can optimize with auto-scaling',
        'Mature platform with widespread industry use for data science, analytics, and machine learning'
    ]
}

df = pd.DataFrame(data)

# Display the DataFrame
print(df)
