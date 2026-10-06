from typing import List, Dict, Any, Optional
from sqlalchemy import or_, and_, func
from extensions import db
from models.career import Career
from models.course import Course, CollegeCourse
from models.college import College
from models.exam import GovernmentExam
from models.scholarship import Scholarship
from models.internship import Internship
from models.career_course import CareerCourse
from models.career_exam import CareerExam
from models.career_skill import CareerSkill
from models.roadmap import CareerRoadmap


class MPathRetriever:
    """
    Precision Hybrid Retrieval Engine for MPath Career Ecosystem.
    Executes parameterized database queries across 7 distinct opportunity domains.
    """

    @staticmethod
    def search_careers(
        query: str = "",
        stream: Optional[str] = None,
        category: Optional[str] = None,
        negative_keywords: Optional[List[str]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieves careers matching query with anti-preference filtering and stream constraints.
        """
        q = Career.query

        STOP_WORDS = {
            "i", "am", "in", "class", "12", "11", "10", "12th", "10th", "pcm", "pcb", 
            "like", "love", "want", "dont", "don't", "not", "but", "what", "can", "do", 
            "how", "to", "for", "me", "my", "is", "a", "an", "the", "and", "or", "options", 
            "kya", "karu", "batao", "hai", "mujhe", "karna", "baad", "after", "which", "best", "good"
        }

        # Normalize negative keywords
        neg_set = {n.lower().strip() for n in (negative_keywords or [])}

        if query:
            raw_tokens = [t.lower().strip("?,.!") for t in query.split() if len(t.strip("?,.!")) > 2]
            content_tokens = [t for t in raw_tokens if t not in STOP_WORDS and t not in neg_set]
            
            if content_tokens:
                token_filters = []
                for token in content_tokens[:6]:
                    pattern = f"%{token}%"
                    token_filters.append(Career.title.ilike(pattern))
                    token_filters.append(Career.short_description.ilike(pattern))
                    token_filters.append(Career.category.ilike(pattern))
                    token_filters.append(Career.technical_skills.ilike(pattern))
                    token_filters.append(Career.required_subjects.ilike(pattern))
                q = q.filter(or_(*token_filters))

        if category:
            q = q.filter(Career.category.ilike(f"%{category}%"))

        if stream:
            q = q.filter(
                or_(
                    Career.preferred_streams.ilike(f"%{stream}%"),
                    Career.preferred_streams.ilike("%Any Stream%"),
                    Career.preferred_streams.is_(None)
                )
            )

        # Apply negative filters (e.g. without engineering)
        if negative_keywords:
            for neg in negative_keywords:
                neg_pat = f"%{neg}%"
                q = q.filter(
                    and_(
                        ~Career.title.ilike(neg_pat),
                        ~Career.category.ilike(neg_pat),
                        ~Career.description.ilike(neg_pat)
                    )
                )

        if content_tokens:
            first_tok = f"%{content_tokens[0]}%"
            q = q.order_by(Career.title.ilike(first_tok).desc(), Career.id.asc())

        careers = q.limit(limit).all()
        results = []
        for c in careers:
            results.append({
                "id": c.id,
                "title": c.title,
                "slug": c.slug,
                "category": c.category,
                "short_description": c.short_description or (c.description[:180] + "..." if c.description else ""),
                "average_salary": c.average_salary or "Competitive industry standard",
                "education_required": c.education_required or c.minimum_qualification,
                "preferred_streams": c.preferred_streams,
                "key_skills": c.technical_skills_list[:5],
                "verified": c.is_verified,
                "url": f"/careers/{c.slug}"
            })
        return results

    @staticmethod
    def get_career_details(slug_or_id: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves complete multi-relational career dossier:
        Career -> Skills -> Courses -> Top Colleges -> Exams -> Roadmap.
        """
        if isinstance(slug_or_id, int) or (isinstance(slug_or_id, str) and slug_or_id.isdigit()):
            c = Career.query.get(int(slug_or_id))
        else:
            c = Career.query.filter_by(slug=str(slug_or_id)).first()

        if not c:
            return None

        # Fetch skills
        skills = CareerSkill.query.filter_by(career_id=c.id).all()
        tech_skills = [s.skill_name for s in skills if s.skill_category == "Technical"] or c.technical_skills_list
        soft_skills = [s.skill_name for s in skills if s.skill_category == "Soft Skill"] or c.soft_skills_list

        # Fetch linked courses and offering colleges
        career_courses = CareerCourse.query.filter_by(career_id=c.id).limit(4).all()
        linked_courses = []
        for cc in career_courses:
            if cc.course:
                course = cc.course
                # Query top 2 colleges for this course
                top_colleges = (
                    College.query.join(CollegeCourse, College.id == CollegeCourse.college_id)
                    .filter(CollegeCourse.course_id == course.id)
                    .order_by(College.nirf_rank.asc().nullslast(), College.name.asc())
                    .limit(2)
                    .all()
                )
                linked_courses.append({
                    "id": course.id,
                    "title": course.name if hasattr(course, "name") else getattr(course, "title", "Degree"),
                    "duration": getattr(course, "duration", ""),
                    "level": getattr(course, "degree_level", ""),
                    "url": f"/courses/{course.id}",
                    "colleges": [{"id": col.id, "name": col.name, "city": col.city, "state": col.state} for col in top_colleges]
                })

        # Fetch linked exams
        career_exams = CareerExam.query.filter_by(career_id=c.id).limit(3).all()
        linked_exams = []
        for ce in career_exams:
            if ce.exam:
                exam = ce.exam
                linked_exams.append({
                    "id": exam.id,
                    "name": exam.name,
                    "short_name": getattr(exam, "short_name", ""),
                    "exam_type": getattr(exam, "exam_type", ""),
                    "url": f"/exams/{exam.id}"
                })

        # Fetch roadmap
        roadmap = CareerRoadmap.query.filter_by(career_id=c.id).first()
        roadmap_data = None
        if roadmap:
            roadmap_data = {
                "overview": roadmap.overview,
                "required_skills": roadmap.required_skills,
                "projects": roadmap.projects,
                "internships": roadmap.internships,
                "future_scope": roadmap.future_scope,
                "steps": roadmap.roadmap_steps
            }

        return {
            "id": c.id,
            "title": c.title,
            "slug": c.slug,
            "category": c.category,
            "description": c.description,
            "what_they_do": c.what_they_do,
            "work_modes": c.work_modes,
            "education_required": c.education_required,
            "preferred_streams": c.preferred_streams,
            "technical_skills": tech_skills[:8],
            "soft_skills": soft_skills[:5],
            "average_salary": c.average_salary,
            "government_opportunities": c.government_opportunities,
            "private_opportunities": c.private_opportunities,
            "future_scope": c.future_scope,
            "linked_courses": linked_courses,
            "linked_exams": linked_exams,
            "roadmap": roadmap_data,
            "url": f"/careers/{c.slug}"
        }

    @staticmethod
    def search_courses(query: str = "", stream: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves matching courses from MPath Course repository.
        """
        q = Course.query
        if query:
            tokens = [t.strip() for t in query.split() if len(t.strip()) > 2]
            for token in tokens:
                pat = f"%{token}%"
                q = q.filter(
                    or_(
                        Course.name.ilike(pat),
                        Course.short_name.ilike(pat),
                        Course.description.ilike(pat),
                        Course.aliases.ilike(pat),
                        Course.specialization.ilike(pat)
                    )
                )

        if stream:
            q = q.filter(
                or_(
                    Course.stream.ilike(f"%{stream}%"),
                    Course.stream.is_(None)
                )
            )

        courses = q.limit(limit).all()
        results = []
        for c in courses:
            desc = c.description or ""
            results.append({
                "id": c.id,
                "name": c.name,
                "degree_level": c.level or "Undergraduate",
                "duration": c.duration or "3 Years",
                "eligibility": c.eligibility_summary or "Check official criteria",
                "overview": (desc[:160] + "...") if desc else "",
                "url": f"/courses/{c.id}"
            })
        return results

    @staticmethod
    def search_colleges(
        query: str = "",
        state: Optional[str] = None,
        course_name: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top accredited Indian colleges matching query, state, or course.
        """
        q = College.query

        if query:
            tokens = [t.strip() for t in query.split() if len(t.strip()) > 2]
            for token in tokens:
                pat = f"%{token}%"
                q = q.filter(
                    or_(
                        College.name.ilike(pat),
                        College.city.ilike(pat),
                        College.state.ilike(pat)
                    )
                )

        if state:
            q = q.filter(College.state.ilike(f"%{state}%"))

        if course_name:
            course = Course.query.filter(Course.name.ilike(f"%{course_name}%")).first()
            if course:
                q = q.join(CollegeCourse, College.id == CollegeCourse.college_id).filter(
                    CollegeCourse.course_id == course.id
                )

        colleges = q.order_by(College.nirf_rank.asc().nullslast(), College.name.asc()).limit(limit).all()
        results = []
        for col in colleges:
            results.append({
                "id": col.id,
                "name": col.name,
                "city": col.city,
                "state": col.state,
                "nirf_rank": col.nirf_rank,
                "ownership": col.ownership,
                "accreditation": col.accreditation,
                "url": f"/colleges/{col.id}"
            })
        return results

    @staticmethod
    def search_exams(
        query: str = "",
        stream: Optional[str] = None,
        exam_type: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieves verified government entrance examinations from MPath Exam registry.
        """
        q = GovernmentExam.query
        if query:
            tokens = [t.strip() for t in query.split() if len(t.strip()) > 2]
            for token in tokens:
                pat = f"%{token}%"
                q = q.filter(
                    or_(
                        GovernmentExam.exam_name.ilike(pat),
                        GovernmentExam.short_name.ilike(pat),
                        GovernmentExam.eligibility.ilike(pat),
                        GovernmentExam.career_opportunities.ilike(pat)
                    )
                )

        if stream:
            q = q.filter(
                or_(
                    GovernmentExam.streams.ilike(f"%{stream}%"),
                    GovernmentExam.streams.is_(None)
                )
            )

        if exam_type:
            q = q.filter(GovernmentExam.exam_type.ilike(f"%{exam_type}%"))

        exams = q.limit(limit).all()
        results = []
        for e in exams:
            results.append({
                "id": e.id,
                "name": e.name,
                "short_name": e.short_name or e.name,
                "exam_type": e.exam_type,
                "eligibility": (e.eligibility[:160] + "...") if e.eligibility else "",
                "exam_date": e.exam_date,
                "official_url": e.official_url or e.application_url,
                "url": f"/exams/{e.id}"
            })
        return results

    @staticmethod
    def search_scholarships(
        query: str = "",
        state: Optional[str] = None,
        education_level: Optional[str] = None,
        income_limit: Optional[float] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieves verified national and state scholarships with eligibility criteria.
        """
        q = Scholarship.query
        if query:
            tokens = [t.strip() for t in query.split() if len(t.strip()) > 2]
            for token in tokens:
                pat = f"%{token}%"
                q = q.filter(
                    or_(
                        Scholarship.title.ilike(pat),
                        Scholarship.provider.ilike(pat),
                        Scholarship.eligibility.ilike(pat),
                        Scholarship.description.ilike(pat)
                    )
                )

        if state:
            q = q.filter(
                or_(
                    Scholarship.state.ilike(f"%{state}%"),
                    Scholarship.national_or_state.ilike("%National%")
                )
            )

        if education_level:
            q = q.filter(Scholarship.education_level.ilike(f"%{education_level}%"))

        if income_limit:
            q = q.filter(
                or_(
                    Scholarship.family_income_limit >= income_limit,
                    Scholarship.family_income_limit.is_(None)
                )
            )

        scholarships = q.limit(limit).all()
        results = []
        for s in scholarships:
            results.append({
                "id": s.id,
                "title": s.title,
                "provider": s.provider,
                "amount": s.amount or s.amount_description or "Tuition Fee / Stipend",
                "deadline": s.deadline or "Refer official notification",
                "eligibility": (s.eligibility[:160] + "...") if s.eligibility else "",
                "official_url": s.official_url or s.final_application_url or s.website,
                "url": f"/scholarships/{s.slug if hasattr(s, 'slug') and s.slug else s.id}"
            })
        return results

    @staticmethod
    def search_internships(
        query: str = "",
        domain: Optional[str] = None,
        category: Optional[str] = None,
        mode: Optional[str] = None,
        org_type: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieves authentic national student internship opportunities from MPath.
        Supports statutory schemes (TULIP, Army, NHAI, C-DAC), research labs, and corporate drives.
        """
        q = Internship.query.filter(Internship.is_active == True)
        if query:
            tokens = [t.strip() for t in query.split() if len(t.strip()) > 2]
            for token in tokens:
                pat = f"%{token}%"
                q = q.filter(
                    or_(
                        Internship.title.ilike(pat),
                        Internship.organisation_name.ilike(pat),
                        Internship.scheme_name.ilike(pat),
                        Internship.description.ilike(pat),
                        Internship.category.ilike(pat),
                        Internship.skills.ilike(pat),
                        Internship.city.ilike(pat)
                    )
                )

        cat = category or domain
        if cat:
            q = q.filter(Internship.category.ilike(f"%{cat}%"))

        if mode and mode.lower() != "all":
            q = q.filter(Internship.work_mode.ilike(f"%{mode}%"))

        if org_type:
            q = q.filter(Internship.organisation_type.ilike(f"%{org_type}%"))

        if state:
            q = q.filter(or_(Internship.state.ilike(f"%{state}%"), Internship.is_pan_india == True, Internship.work_mode == "Remote"))

        internships = q.order_by(Internship.scheme_name.isnot(None).desc(), Internship.id.desc()).limit(limit).all()
        results = []
        for i in internships:
            results.append({
                "id": i.id,
                "title": i.title,
                "slug": i.slug,
                "organisation": i.organisation_name,
                "scheme_name": i.scheme_name,
                "category": i.category,
                "location": i.location or f"{i.city or ''}, {i.state or ''}",
                "mode": i.work_mode,
                "stipend": i.stipend or ("₹" + str(i.stipend_min) if i.stipend_min else "Provided"),
                "duration": i.duration_text or (str(i.duration_value) + " Months"),
                "deadline": i.deadline_text,
                "skills": i.skills_list[:4],
                "apply_url": i.primary_apply_url,
                "dossier_url": f"/internships/{i.slug}"
            })
        return results

    @staticmethod
    def get_internship_details(identifier: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves complete structured dossier for an internship opportunity.
        """
        i = None
        if identifier.isdigit():
            i = Internship.query.get(int(identifier))
        if not i:
            i = Internship.query.filter_by(slug=identifier).first()
        if not i:
            i = Internship.query.filter_by(source_record_id=identifier).first()
        if not i:
            i = Internship.query.filter(Internship.title.ilike(f"%{identifier}%")).first()

        if not i:
            return None

        status_label, _, _ = i.display_status
        return {
            "id": i.id,
            "title": i.title,
            "slug": i.slug,
            "organisation": i.organisation_name,
            "organisation_type": i.organisation_type,
            "scheme_name": i.scheme_name,
            "category": i.category,
            "location": i.location,
            "city": i.city,
            "state": i.state,
            "work_mode": i.work_mode,
            "stipend": i.stipend,
            "duration": i.duration_text or f"{i.duration_value} Months",
            "deadline": i.deadline_text,
            "status": status_label,
            "academic_credits": i.academic_credit_available,
            "ppo_available": i.ppo_available,
            "eligibility": i.eligibility,
            "eligible_degrees": i.eligible_degrees,
            "skills": i.skills_list,
            "responsibilities": i.responsibilities,
            "selection_process": i.selection_process,
            "official_apply_url": i.primary_apply_url,
            "source_name": i.source_name,
            "verification_status": i.verification_status,
            "dossier_url": f"/internships/{i.slug}"
        }

    @staticmethod
    def find_internships_for_student(student_profile: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Deterministic matching of verified internships for student profile.
        """
        from services.internship.matching_engine import InternshipMatchingEngine

        all_active = Internship.query.filter_by(is_active=True).all()
        scored = []
        for it in all_active:
            m = InternshipMatchingEngine.compute_match(student_profile, it)
            if m["eligibility_passed"] or m["score"] >= 45:
                scored.append((m["score"], it, m))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:limit]

        results = []
        for score, it, m in top:
            results.append({
                "id": it.id,
                "title": it.title,
                "slug": it.slug,
                "organisation": it.organisation_name,
                "scheme_name": it.scheme_name,
                "match_score": score,
                "match_tier": m["tier"],
                "work_mode": it.work_mode,
                "location": it.location,
                "stipend": it.stipend,
                "duration": it.duration_text or f"{it.duration_value} Months",
                "counselling_fit": m["counselling"]["why_fits"],
                "recommended_next_step": m["counselling"]["recommended_next_step"],
                "apply_url": it.primary_apply_url,
                "dossier_url": f"/internships/{it.slug}"
            })
        return results

    @staticmethod
    def get_exam_details(identifier: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves complete structured dossier for a specific examination from MPath.
        """
        e = None
        if str(identifier).strip().isdigit():
            e = GovernmentExam.query.get(int(str(identifier).strip()))
        if not e:
            e = GovernmentExam.query.filter_by(slug=identifier).first()
        if not e:
            e = GovernmentExam.query.filter(
                or_(
                    GovernmentExam.exam_name.ilike(f"%{identifier}%"),
                    GovernmentExam.short_name.ilike(f"%{identifier}%")
                )
            ).first()

        if not e:
            return None

        # Fetch latest cycle if available
        latest_cycle = e.cycles.order_by(db.desc("cycle_year")).first() if hasattr(e, "cycles") else None
        cycle_info = None
        if latest_cycle:
            cycle_info = {
                "year": latest_cycle.cycle_year,
                "cycle_name": latest_cycle.cycle_name,
                "status": latest_cycle.status,
                "notification_date": str(latest_cycle.notification_date) if latest_cycle.notification_date else None,
                "application_end_date": str(latest_cycle.application_end_date) if latest_cycle.application_end_date else None,
                "exam_date": str(latest_cycle.exam_date) if latest_cycle.exam_date else None,
                "notification_url": latest_cycle.official_notification_url,
                "application_url": latest_cycle.official_application_url
            }

        return {
            "id": e.id,
            "exam_name": e.exam_name,
            "short_name": e.short_name,
            "conducting_body": e.conducting_body,
            "category": e.category,
            "qualification": e.qualification or e.minimum_qualification,
            "streams": e.streams,
            "age_criteria": f"{e.age_min or 'Any'} to {e.age_max or 'Any'} years" if (e.age_min or e.age_max) else "As per notification",
            "age_relaxation": e.age_relaxation,
            "selection_process": e.selection_process,
            "syllabus_summary": e.syllabus[:300] if e.syllabus else "Prescribed syllabus available in notification",
            "salary": e.salary,
            "career_opportunities": e.career_opportunities,
            "official_portal": e.official_url or e.official_website,
            "notification_url": e.notification_url or (cycle_info["notification_url"] if cycle_info else None),
            "latest_cycle": cycle_info,
            "verification_status": e.verification_status,
            "url": f"/exams/{e.id}"
        }

    @staticmethod
    def discover_opportunities_for_student(
        education_level: Optional[str] = None,
        stream: Optional[str] = None,
        state: Optional[str] = None,
        age: Optional[int] = None,
        category: Optional[str] = None,
        course: Optional[str] = None,
        limit: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Deterministic multi-factor opportunity matching for Indian students.
        Zero hallucination. Matches real statutory exams and opportunities from DB.
        """
        from services.eligibility_engine import OpportunityEligibilityEvaluator

        student_data = {
            "education_level": education_level,
            "stream": stream,
            "state": state,
            "age": age,
            "category": category,
            "course": course
        }

        all_exams = GovernmentExam.query.all()
        matched = []

        for ex in all_exams:
            eval_res = OpportunityEligibilityEvaluator.evaluate(ex, student_data)
            if eval_res.get("status") in ("ELIGIBLE", "LIKELY_ELIGIBLE"):
                matched.append({
                    "id": ex.id,
                    "name": ex.exam_name,
                    "short_name": ex.short_name or ex.exam_name,
                    "conducting_body": ex.conducting_body,
                    "category": ex.category,
                    "status": eval_res.get("status"),
                    "match_score": eval_res.get("score"),
                    "reasons": eval_res.get("reasons", [])[:3],
                    "official_portal": ex.official_url or ex.official_website,
                    "qualification": ex.qualification or ex.minimum_qualification,
                    "salary": ex.salary,
                    "url": f"/exams/{ex.id}"
                })

        # Rank by match score descending
        matched.sort(key=lambda x: x["match_score"], reverse=True)
        return matched[:limit]

