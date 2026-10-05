def calculate_match_score(context, career):
    score = 30  # Baseline discovery score
    reasons = []

    # 1. Assessment Match
    recommended = (context.get("recommended_category") or "").strip().lower()
    if recommended:
        career_cat = (career.category or "").lower()
        career_title = (career.title or "").lower()
        if recommended in career_title or recommended in career_cat or career_title in recommended:
            score += 35
            reasons.append("Strong match with your career assessment results.")

    # 2. Academic Stream Match
    stream = (context.get("stream") or "").strip().lower()
    if stream:
        cat_lower = (career.category or "").lower()
        if any(k in stream for k in ["pcm", "engineering", "tech", "computer"]) and "tech" in cat_lower:
            score += 25
            reasons.append("Aligns directly with PCM / Technical stream.")
        elif any(k in stream for k in ["pcb", "medical", "bio"]) and any(k in cat_lower for k in ["medical", "health"]):
            score += 25
            reasons.append("Aligns with PCB / Healthcare science stream.")
        elif any(k in stream for k in ["commerce", "b.com", "finance"]) and any(k in cat_lower for k in ["finance", "commerce", "management"]):
            score += 25
            reasons.append("Aligns with Commerce & Financial stream.")
        elif any(k in stream for k in ["arts", "humanities"]) and any(k in cat_lower for k in ["government", "law", "education", "design"]):
            score += 20
            reasons.append("Aligns with Arts & Public Service stream.")

    # 3. Interests & Strengths Match
    interests = (context.get("interests") or "").lower()
    strengths = (context.get("strengths") or "").lower()
    student_text = f"{interests} {strengths} {context.get('career_interest', '')}".lower()

    career_text = f"{career.title} {career.category} {career.skills_required or ''}".lower()

    matched_keywords = []
    for kw in ["python", "coding", "design", "finance", "medicine", "biology", "math", "law", "teaching", "business", "research"]:
        if kw in student_text and kw in career_text:
            matched_keywords.append(kw.capitalize())

    if matched_keywords:
        score += min(len(matched_keywords) * 6, 20)
        reasons.append(f"Skills & interests overlap in: {', '.join(matched_keywords)}.")

    # 4. Saved Career Check
    saved = context.get("saved_careers", [])
    if career.title in saved:
        score += 15
        reasons.append("Marked as saved interest in your student profile.")

    if not reasons:
        reasons.append("Discovered based on popular career avenues for your academic level.")

    score = min(score, 98)

    return score, reasons