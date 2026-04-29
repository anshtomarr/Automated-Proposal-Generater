"""
Deterministic pricing engine — maps feature types and complexity to costs.
"""

# Hourly rate by role
HOURLY_RATES = {
    "senior_developer": 150,
    "mid_developer": 110,
    "junior_developer": 75,
    "designer": 120,
    "qa_engineer": 95,
    "devops_engineer": 130,
    "project_manager": 140,
    "data_engineer": 145,
}

# Feature-to-effort mapping: { feature_type: { complexity: (hours, roles_involved) } }
FEATURE_EFFORT_MAP = {
    "authentication": {
        "Low": (20, ["mid_developer"]),
        "Medium": (45, ["senior_developer", "mid_developer"]),
        "High": (80, ["senior_developer", "mid_developer", "qa_engineer"]),
    },
    "database_design": {
        "Low": (15, ["mid_developer"]),
        "Medium": (40, ["senior_developer", "data_engineer"]),
        "High": (70, ["senior_developer", "data_engineer", "devops_engineer"]),
    },
    "api_development": {
        "Low": (25, ["mid_developer"]),
        "Medium": (60, ["senior_developer", "mid_developer"]),
        "High": (120, ["senior_developer", "mid_developer", "qa_engineer"]),
    },
    "frontend_ui": {
        "Low": (30, ["mid_developer", "designer"]),
        "Medium": (80, ["senior_developer", "mid_developer", "designer"]),
        "High": (150, ["senior_developer", "mid_developer", "designer", "qa_engineer"]),
    },
    "payment_integration": {
        "Low": (20, ["mid_developer"]),
        "Medium": (50, ["senior_developer", "mid_developer"]),
        "High": (90, ["senior_developer", "mid_developer", "qa_engineer"]),
    },
    "data_pipeline": {
        "Low": (30, ["data_engineer"]),
        "Medium": (70, ["senior_developer", "data_engineer"]),
        "High": (130, ["senior_developer", "data_engineer", "devops_engineer"]),
    },
    "cloud_infrastructure": {
        "Low": (15, ["devops_engineer"]),
        "Medium": (40, ["devops_engineer", "senior_developer"]),
        "High": (80, ["devops_engineer", "senior_developer", "qa_engineer"]),
    },
    "testing_qa": {
        "Low": (20, ["qa_engineer"]),
        "Medium": (50, ["qa_engineer", "mid_developer"]),
        "High": (100, ["qa_engineer", "senior_developer", "mid_developer"]),
    },
    "reporting_dashboard": {
        "Low": (25, ["mid_developer", "designer"]),
        "Medium": (55, ["senior_developer", "mid_developer", "designer"]),
        "High": (100, ["senior_developer", "mid_developer", "designer", "data_engineer"]),
    },
    "search_functionality": {
        "Low": (15, ["mid_developer"]),
        "Medium": (40, ["senior_developer", "mid_developer"]),
        "High": (75, ["senior_developer", "mid_developer", "data_engineer"]),
    },
    "notifications": {
        "Low": (10, ["mid_developer"]),
        "Medium": (30, ["mid_developer", "devops_engineer"]),
        "High": (60, ["senior_developer", "mid_developer", "devops_engineer"]),
    },
    "third_party_integration": {
        "Low": (15, ["mid_developer"]),
        "Medium": (40, ["senior_developer", "mid_developer"]),
        "High": (80, ["senior_developer", "mid_developer", "qa_engineer"]),
    },
    "migration": {
        "Low": (25, ["mid_developer"]),
        "Medium": (60, ["senior_developer", "data_engineer"]),
        "High": (120, ["senior_developer", "data_engineer", "devops_engineer", "qa_engineer"]),
    },
    "security_compliance": {
        "Low": (15, ["senior_developer"]),
        "Medium": (40, ["senior_developer", "devops_engineer"]),
        "High": (80, ["senior_developer", "devops_engineer", "qa_engineer"]),
    },
    "general": {
        "Low": (20, ["mid_developer"]),
        "Medium": (50, ["senior_developer", "mid_developer"]),
        "High": (100, ["senior_developer", "mid_developer", "qa_engineer"]),
    },
}

# Project management overhead percentage
PM_OVERHEAD_PERCENT = 12


def calculate_pricing(milestones: list[dict]) -> dict:
    """
    Calculate deterministic pricing from LLM-generated milestones.

    Each milestone should have:
        - name: str
        - features: list of { feature_type: str, complexity: "Low"|"Medium"|"High" }

    Returns a pricing breakdown with line items and totals.
    """
    line_items = []
    total_hours = 0
    total_cost = 0

    for milestone in milestones:
        milestone_items = []
        milestone_hours = 0
        milestone_cost = 0

        for feature in milestone.get("features", []):
            feature_type = feature.get("feature_type", "general").lower().replace(" ", "_")
            complexity = feature.get("complexity", "Medium")

            if feature_type not in FEATURE_EFFORT_MAP:
                feature_type = "general"

            if complexity not in ("Low", "Medium", "High"):
                complexity = "Medium"

            hours, roles = FEATURE_EFFORT_MAP[feature_type][complexity]
            avg_rate = sum(HOURLY_RATES[r] for r in roles) / len(roles)
            cost = round(hours * avg_rate)

            milestone_items.append({
                "feature": feature.get("name", feature_type.replace("_", " ").title()),
                "feature_type": feature_type,
                "complexity": complexity,
                "hours": hours,
                "roles": [r.replace("_", " ").title() for r in roles],
                "avg_hourly_rate": round(avg_rate),
                "cost": cost,
            })

            milestone_hours += hours
            milestone_cost += cost

        line_items.append({
            "milestone": milestone.get("name", "Unnamed Milestone"),
            "items": milestone_items,
            "subtotal_hours": milestone_hours,
            "subtotal_cost": milestone_cost,
        })

        total_hours += milestone_hours
        total_cost += milestone_cost

    pm_cost = round(total_cost * PM_OVERHEAD_PERCENT / 100)
    grand_total = total_cost + pm_cost

    return {
        "line_items": line_items,
        "subtotal_hours": total_hours,
        "subtotal_cost": total_cost,
        "project_management_overhead": {
            "percentage": PM_OVERHEAD_PERCENT,
            "cost": pm_cost,
        },
        "grand_total": grand_total,
        "currency": "USD",
    }
