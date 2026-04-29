"""
Initialize the SQLite RAG database with 3 mock historical winning proposals.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "proposals.db")


def create_database():
    """Create the projects table and populate with mock data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS projects")

    cursor.execute("""
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_type TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            tech_stack TEXT NOT NULL,
            timeline TEXT NOT NULL,
            complexity TEXT NOT NULL,
            budget_range TEXT NOT NULL,
            outcome TEXT NOT NULL,
            keywords TEXT NOT NULL
        )
    """)

    mock_proposals = [
        {
            "project_type": "E-commerce Platform",
            "title": "LuxeCart – Premium E-commerce Marketplace",
            "description": (
                "Built a full-featured multi-vendor e-commerce marketplace with real-time "
                "inventory management, AI-powered product recommendations, Stripe payment "
                "integration, and a headless CMS for content management. Included an admin "
                "dashboard with analytics, order tracking, and automated email notifications. "
                "The platform handled 50K+ concurrent users with sub-200ms API response times."
            ),
            "tech_stack": (
                "Next.js 14, React 18, TypeScript, Node.js, PostgreSQL, Redis, "
                "Stripe API, AWS S3, Docker, Kubernetes, Elasticsearch"
            ),
            "timeline": (
                "Phase 1 (Weeks 1-3): Requirements & Architecture Design | "
                "Phase 2 (Weeks 4-8): Core Backend – Auth, Products, Orders, Payments | "
                "Phase 3 (Weeks 9-12): Frontend Storefront & Admin Dashboard | "
                "Phase 4 (Weeks 13-15): Search, Recommendations & Performance Tuning | "
                "Phase 5 (Weeks 16-18): QA, Load Testing & Deployment"
            ),
            "complexity": "High",
            "budget_range": "$120,000 - $180,000",
            "outcome": (
                "Successfully launched with 200+ vendors onboarded in the first month. "
                "Achieved 99.9% uptime and processed $2.3M in transactions within 90 days."
            ),
            "keywords": (
                "ecommerce, e-commerce, shopping, cart, marketplace, payments, stripe, "
                "storefront, products, inventory, orders, checkout, online store, retail, "
                "multi-vendor, catalog, wishlist, reviews"
            ),
        },
        {
            "project_type": "CRM Migration & Modernization",
            "title": "EnterpriseSync – Legacy CRM to Cloud Migration",
            "description": (
                "Migrated a 10-year-old on-premise CRM system (built on .NET/SQL Server) "
                "to a modern cloud-native architecture. Implemented a microservices backend, "
                "real-time data synchronization, role-based access control, and an interactive "
                "reporting dashboard. Preserved all historical data with zero downtime migration "
                "using a blue-green deployment strategy."
            ),
            "tech_stack": (
                "Python, FastAPI, React, TypeScript, PostgreSQL, Apache Kafka, "
                "Docker, AWS (ECS, RDS, S3), Terraform, Grafana, Prometheus"
            ),
            "timeline": (
                "Phase 1 (Weeks 1-4): Legacy System Audit & Data Mapping | "
                "Phase 2 (Weeks 5-10): Microservices Architecture & API Layer | "
                "Phase 3 (Weeks 11-16): Frontend Rebuild & Reporting Dashboard | "
                "Phase 4 (Weeks 17-20): Data Migration & Synchronization Pipeline | "
                "Phase 5 (Weeks 21-24): UAT, Performance Testing & Go-Live"
            ),
            "complexity": "High",
            "budget_range": "$150,000 - $220,000",
            "outcome": (
                "Zero-downtime migration completed on schedule. Reduced query response times "
                "by 85% and cut infrastructure costs by 40% through cloud optimization. "
                "User adoption rate increased by 60% due to improved UX."
            ),
            "keywords": (
                "crm, migration, legacy, modernization, cloud, microservices, database, "
                "enterprise, customer relationship, data migration, api, dashboard, "
                "reporting, analytics, saas, upgrade, refactor"
            ),
        },
        {
            "project_type": "Data Pipeline & Analytics Platform",
            "title": "DataForge – Real-time Analytics Pipeline",
            "description": (
                "Designed and implemented a real-time data pipeline processing 10M+ events "
                "per day from multiple sources (IoT sensors, web analytics, third-party APIs). "
                "Built an ETL framework with automated data quality checks, anomaly detection "
                "using ML models, and an interactive BI dashboard for business stakeholders. "
                "Included automated alerting via Slack/email for KPI threshold breaches."
            ),
            "tech_stack": (
                "Python, Apache Airflow, Apache Spark, Kafka, dbt, Snowflake, "
                "Streamlit, TensorFlow, Docker, GCP (BigQuery, Dataflow, Pub/Sub)"
            ),
            "timeline": (
                "Phase 1 (Weeks 1-3): Data Source Audit & Pipeline Architecture | "
                "Phase 2 (Weeks 4-8): ETL Pipeline Development & Data Lake Setup | "
                "Phase 3 (Weeks 9-12): ML-based Anomaly Detection & Quality Checks | "
                "Phase 4 (Weeks 13-16): BI Dashboard & Alerting System | "
                "Phase 5 (Weeks 17-20): Load Testing, Optimization & Documentation"
            ),
            "complexity": "High",
            "budget_range": "$100,000 - $160,000",
            "outcome": (
                "Processing 10M+ events/day with 99.7% reliability. Reduced manual "
                "reporting effort by 90%. Anomaly detection caught 3 critical data issues "
                "within the first week of deployment that would have gone unnoticed."
            ),
            "keywords": (
                "data pipeline, etl, analytics, big data, data engineering, streaming, "
                "real-time, dashboard, bi, business intelligence, machine learning, "
                "data lake, warehouse, airflow, spark, kafka, iot, automation"
            ),
        },
    ]

    for project in mock_proposals:
        cursor.execute(
            """
            INSERT INTO projects 
                (project_type, title, description, tech_stack, timeline, 
                 complexity, budget_range, outcome, keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project["project_type"],
                project["title"],
                project["description"],
                project["tech_stack"],
                project["timeline"],
                project["complexity"],
                project["budget_range"],
                project["outcome"],
                project["keywords"],
            ),
        )

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH} with {len(mock_proposals)} historical proposals.")


if __name__ == "__main__":
    create_database()
