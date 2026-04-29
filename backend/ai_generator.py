"""
AI Proposal Generator — uses LangChain + Gemini to generate structured proposal JSON.
Includes a mock fallback if no API key is configured.
"""

import json
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Check if we have a real API key
HAS_API_KEY = bool(GOOGLE_API_KEY) and GOOGLE_API_KEY != "your_gemini_api_key_here"

SYSTEM_PROMPT = """You are a senior technical consultant generating a project proposal.

Analyze the client requirements document and the context from similar past projects.
Generate a structured JSON response with EXACTLY this schema:

{
  "project_summary": "A 2-3 paragraph executive summary of the proposed project.",
  "project_type": "The category of this project (e.g., E-commerce Platform, Data Pipeline, etc.)",
  "tech_stack": [
    {
      "technology": "Technology name",
      "justification": "Why this technology was chosen for this project"
    }
  ],
  "milestones": [
    {
      "name": "Milestone name",
      "description": "What this milestone delivers",
      "duration_weeks": 3,
      "features": [
        {
          "name": "Feature display name",
          "feature_type": "One of: authentication, database_design, api_development, frontend_ui, payment_integration, data_pipeline, cloud_infrastructure, testing_qa, reporting_dashboard, search_functionality, notifications, third_party_integration, migration, security_compliance, general",
          "complexity": "One of: Low, Medium, High"
        }
      ]
    }
  ],
  "risks": [
    {
      "risk": "Risk description",
      "mitigation": "How to mitigate it"
    }
  ],
  "estimated_timeline_weeks": 18
}

RULES:
- Output ONLY valid JSON, no markdown fences, no extra text  
- Every milestone must have at least 2 features
- feature_type MUST be one of the listed types
- complexity MUST be exactly "Low", "Medium", or "High"
- Be thorough and realistic in your analysis
"""


def generate_proposal(client_text: str, rag_context: list[dict]) -> dict:
    """
    Generate a structured proposal using the LLM or fallback to mock.
    """
    if HAS_API_KEY:
        return _generate_with_llm(client_text, rag_context)
    else:
        return _generate_mock(client_text, rag_context)


def _generate_with_llm(client_text: str, rag_context: list[dict]) -> dict:
    """Use LangChain + Gemini to generate the proposal."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.prompts import ChatPromptTemplate

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3,
    )

    context_str = "\n\n---\n\n".join([
        f"Past Project: {p['title']}\n"
        f"Type: {p['project_type']}\n"
        f"Description: {p['description']}\n"
        f"Tech Stack: {p['tech_stack']}\n"
        f"Timeline: {p['timeline']}\n"
        f"Budget: {p['budget_range']}\n"
        f"Outcome: {p['outcome']}"
        for p in rag_context
    ]) if rag_context else "No similar past projects found."

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", (
            "## Client Requirements Document:\n{client_text}\n\n"
            "## Context from Similar Past Projects:\n{context}"
        )),
    ])

    chain = prompt | llm
    response = chain.invoke({
        "client_text": client_text,
        "context": context_str,
    })

    # Parse the JSON from the response
    raw = response.content.strip()
    # Remove markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        raw = raw.rsplit("```", 1)[0]
    
    return json.loads(raw)


def _generate_mock(client_text: str, rag_context: list[dict]) -> dict:
    """Fallback mock response for demo purposes when no API key is set."""
    
    # Detect project type from text
    text_lower = client_text.lower()
    if any(w in text_lower for w in ["ecommerce", "e-commerce", "shop", "store", "cart"]):
        project_type = "E-commerce Platform"
    elif any(w in text_lower for w in ["crm", "migration", "legacy", "modernize"]):
        project_type = "CRM Migration & Modernization"
    elif any(w in text_lower for w in ["data", "pipeline", "analytics", "etl"]):
        project_type = "Data Pipeline & Analytics Platform"
    elif any(w in text_lower for w in ["mobile", "app", "ios", "android"]):
        project_type = "Mobile Application Development"
    else:
        project_type = "Custom Software Development"

    return {
        "project_summary": (
            f"Based on the provided requirements document, we propose building a comprehensive "
            f"{project_type} solution. The project involves designing and implementing a scalable, "
            f"production-ready system that addresses the client's core business needs.\n\n"
            f"Our approach leverages modern development practices and industry-proven technologies, "
            f"informed by our experience delivering similar projects. We will follow an agile "
            f"methodology with bi-weekly sprint cycles and continuous stakeholder communication."
        ),
        "project_type": project_type,
        "tech_stack": [
            {"technology": "Next.js 14 / React 18", "justification": "Modern full-stack framework enabling SSR, API routes, and optimal developer experience"},
            {"technology": "TypeScript", "justification": "Type safety reduces runtime errors and improves team collaboration at scale"},
            {"technology": "PostgreSQL", "justification": "Battle-tested relational database with strong ACID compliance for transactional workloads"},
            {"technology": "Redis", "justification": "In-memory caching layer for session management and performance optimization"},
            {"technology": "Docker + Kubernetes", "justification": "Container orchestration for reliable deployment, scaling, and environment parity"},
            {"technology": "AWS (ECS, RDS, S3)", "justification": "Enterprise-grade cloud infrastructure with managed services reducing operational overhead"},
        ],
        "milestones": [
            {
                "name": "Discovery & Architecture",
                "description": "Requirements deep-dive, system architecture design, and development environment setup",
                "duration_weeks": 3,
                "features": [
                    {"name": "System Architecture Design", "feature_type": "database_design", "complexity": "Medium"},
                    {"name": "Cloud Infrastructure Setup", "feature_type": "cloud_infrastructure", "complexity": "Medium"},
                    {"name": "CI/CD Pipeline Configuration", "feature_type": "cloud_infrastructure", "complexity": "Low"},
                ],
            },
            {
                "name": "Core Backend Development",
                "description": "API layer, authentication system, and database schema implementation",
                "duration_weeks": 4,
                "features": [
                    {"name": "User Authentication & RBAC", "feature_type": "authentication", "complexity": "High"},
                    {"name": "RESTful API Layer", "feature_type": "api_development", "complexity": "High"},
                    {"name": "Database Schema & Migrations", "feature_type": "database_design", "complexity": "Medium"},
                    {"name": "Third-party Service Integration", "feature_type": "third_party_integration", "complexity": "Medium"},
                ],
            },
            {
                "name": "Frontend & User Experience",
                "description": "Responsive UI, interactive dashboards, and user-facing features",
                "duration_weeks": 4,
                "features": [
                    {"name": "Responsive UI Components", "feature_type": "frontend_ui", "complexity": "High"},
                    {"name": "Analytics Dashboard", "feature_type": "reporting_dashboard", "complexity": "Medium"},
                    {"name": "Search & Filtering System", "feature_type": "search_functionality", "complexity": "Medium"},
                    {"name": "Notification System", "feature_type": "notifications", "complexity": "Medium"},
                ],
            },
            {
                "name": "Integration & Testing",
                "description": "End-to-end testing, security audit, and performance optimization",
                "duration_weeks": 3,
                "features": [
                    {"name": "Comprehensive Test Suite", "feature_type": "testing_qa", "complexity": "High"},
                    {"name": "Security Audit & Compliance", "feature_type": "security_compliance", "complexity": "Medium"},
                    {"name": "Performance Optimization", "feature_type": "api_development", "complexity": "Medium"},
                ],
            },
            {
                "name": "Deployment & Launch",
                "description": "Production deployment, monitoring setup, and documentation",
                "duration_weeks": 2,
                "features": [
                    {"name": "Production Deployment", "feature_type": "cloud_infrastructure", "complexity": "Medium"},
                    {"name": "Monitoring & Alerting", "feature_type": "cloud_infrastructure", "complexity": "Low"},
                    {"name": "Documentation & Handoff", "feature_type": "general", "complexity": "Low"},
                ],
            },
        ],
        "risks": [
            {"risk": "Scope creep due to evolving client requirements", "mitigation": "Strict change control process with impact analysis for any scope additions"},
            {"risk": "Third-party API instability or rate limits", "mitigation": "Implement circuit breaker patterns and fallback mechanisms"},
            {"risk": "Data migration complexity exceeding estimates", "mitigation": "Conduct thorough data audit in Phase 1 and allocate 20% buffer time"},
        ],
        "estimated_timeline_weeks": 16,
    }
