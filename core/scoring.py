# core/scoring.py


FREQUENCY_MULTIPLIERS = {
    "Daily": 22,
    "Weekly": 4.33,
    "Monthly": 1,
    "Quarterly": 1 / 3,
    "Yearly": 1 / 12,
    "Ad hoc": 1,
}


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))


def calculate_monthly_executions(task):
    """
    Convert task frequency into estimated monthly executions.
    """

    frequency = task.get("frequency", "Monthly")
    executions = float(task.get("executions_per_period", 0) or 0)

    multiplier = FREQUENCY_MULTIPLIERS.get(frequency, 1)

    return executions * multiplier


def calculate_monthly_hours(task):
    """
    Estimate hours spent on the task every month.
    """

    monthly_executions = calculate_monthly_executions(task)

    minutes = float(task.get("minutes_per_execution", 0) or 0)

    return (monthly_executions * minutes) / 60


def calculate_automation_score(task):
    """
    Estimate how suitable the task is for automation.

    Score: 0-100
    """

    repetitiveness = float(task.get("repetitiveness", 1) or 1)
    standardization = float(task.get("standardization", 1) or 1)
    manual_effort = float(task.get("manual_effort", 1) or 1)
    judgement = float(task.get("judgement_required", 5) or 5)
    error_probability = float(task.get("error_probability", 1) or 1)
    digital_input = int(task.get("digital_input", 0) or 0)

    # Convert 1-5 values into 0-100
    repetitive_score = (repetitiveness - 1) / 4 * 100
    standardization_score = (standardization - 1) / 4 * 100
    manual_score = (manual_effort - 1) / 4 * 100

    # Less human judgement = easier to automate
    rule_based_score = (5 - judgement) / 4 * 100

    error_score = (error_probability - 1) / 4 * 100

    digital_score = 100 if digital_input else 25

    score = (
        repetitive_score * 0.25
        + standardization_score * 0.25
        + rule_based_score * 0.20
        + digital_score * 0.15
        + manual_score * 0.10
        + error_score * 0.05
    )

    return round(clamp(score), 1)


def calculate_impact_score(task):
    """
    Estimate business impact based primarily on time consumed
    and manual/error burden.
    """

    monthly_hours = calculate_monthly_hours(task)

    manual_effort = float(task.get("manual_effort", 1) or 1)
    error_probability = float(task.get("error_probability", 1) or 1)

    # 20 monthly hours is considered very high impact
    time_score = min(monthly_hours / 20, 1) * 100

    manual_score = (manual_effort - 1) / 4 * 100
    error_score = (error_probability - 1) / 4 * 100

    score = (
        time_score * 0.70
        + manual_score * 0.20
        + error_score * 0.10
    )

    return round(clamp(score), 1)


def calculate_complexity_score(task):
    """
    Rough estimate of implementation complexity.

    Higher score = harder to automate.
    """

    judgement = float(task.get("judgement_required", 5) or 5)
    standardization = float(task.get("standardization", 1) or 1)
    digital_input = int(task.get("digital_input", 0) or 0)

    judgement_complexity = (judgement - 1) / 4 * 100

    non_standard_complexity = (
        (5 - standardization) / 4 * 100
    )

    physical_input_complexity = (
        0 if digital_input else 100
    )

    score = (
        judgement_complexity * 0.45
        + non_standard_complexity * 0.35
        + physical_input_complexity * 0.20
    )

    return round(clamp(score), 1)


def calculate_saving_rate(automation_score):
    """
    Convert automation potential into a conservative
    estimated percentage of time that could be saved.
    """

    if automation_score >= 85:
        return 0.80

    if automation_score >= 70:
        return 0.65

    if automation_score >= 55:
        return 0.45

    if automation_score >= 40:
        return 0.25

    return 0.10


def calculate_priority_score(
    automation_score,
    impact_score,
    complexity_score,
):
    """
    High automation potential + high impact + low complexity
    produces a high priority score.
    """

    ease_score = 100 - complexity_score

    score = (
        automation_score * 0.45
        + impact_score * 0.35
        + ease_score * 0.20
    )

    return round(clamp(score), 1)


def get_priority_label(priority_score):
    if priority_score >= 75:
        return "HIGH"

    if priority_score >= 50:
        return "MEDIUM"

    return "LOW"


def get_opportunity_label(
    automation_score,
    impact_score,
    complexity_score,
):
    """
    Categorize the automation opportunity.
    """

    if (
        automation_score >= 70
        and impact_score >= 50
        and complexity_score <= 40
    ):
        return "QUICK WIN"

    if (
        automation_score >= 70
        and impact_score >= 50
    ):
        return "STRATEGIC AUTOMATION"

    if automation_score >= 60:
        return "GOOD CANDIDATE"

    if impact_score >= 60:
        return "INVESTIGATE"

    return "LOW PRIORITY"


def analyze_task(task):
    """
    Run the complete WorkLens scoring engine.
    """

    monthly_executions = calculate_monthly_executions(task)
    monthly_hours = calculate_monthly_hours(task)

    automation_score = calculate_automation_score(task)
    impact_score = calculate_impact_score(task)
    complexity_score = calculate_complexity_score(task)

    saving_rate = calculate_saving_rate(
        automation_score
    )

    potential_hours_saved = (
        monthly_hours * saving_rate
    )

    priority_score = calculate_priority_score(
        automation_score,
        impact_score,
        complexity_score,
    )

    priority = get_priority_label(
        priority_score
    )

    opportunity = get_opportunity_label(
        automation_score,
        impact_score,
        complexity_score,
    )

    return {
        "monthly_executions": round(monthly_executions, 1),
        "monthly_hours": round(monthly_hours, 1),
        "automation_score": automation_score,
        "impact_score": impact_score,
        "complexity_score": complexity_score,
        "priority_score": priority_score,
        "priority": priority,
        "saving_rate": saving_rate,
        "potential_hours_saved": round(
            potential_hours_saved,
            1
        ),
        "opportunity": opportunity,
    }