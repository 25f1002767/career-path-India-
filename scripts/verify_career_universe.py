import sqlite3

def run_report():
    conn = sqlite3.connect('careerpathindia.db')
    c = conn.cursor()

    total = c.execute('SELECT COUNT(*) FROM careers').fetchone()[0]
    categories = c.execute('SELECT category, count(*) FROM careers GROUP BY category ORDER BY count(*) DESC').fetchall()
    courses = c.execute('SELECT COUNT(*) FROM career_courses').fetchone()[0]
    exams = c.execute('SELECT COUNT(*) FROM career_exams').fetchone()[0]
    skills = c.execute('SELECT COUNT(*) FROM career_skills').fetchone()[0]
    roadmaps_total = c.execute('SELECT COUNT(*) FROM career_roadmaps').fetchone()[0]
    verified = c.execute("SELECT COUNT(*) FROM careers WHERE verification_status = 'VERIFIED'").fetchone()[0]
    review = total - verified
    lesser_known = c.execute('SELECT COUNT(*) FROM careers WHERE is_lesser_known = 1').fetchone()[0]
    subcategories_cnt = c.execute('SELECT COUNT(DISTINCT sub_category) FROM careers').fetchone()[0]

    healthcare = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Healthcare%'").fetchone()[0]
    govt = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Government%'").fetchone()[0]
    arts = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Social Sciences%' OR category LIKE '%Media%' OR sub_category LIKE '%Humanities%' OR sub_category LIKE '%Language%' OR sub_category LIKE '%Literature%'").fetchone()[0]
    commerce = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Finance%'").fetchone()[0]
    agri = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Agriculture%'").fetchone()[0]
    creative = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Design%'").fetchone()[0]
    trades = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Skilled Trades%'").fetchone()[0]
    sports = c.execute("SELECT COUNT(*) FROM careers WHERE sub_category LIKE '%Sport%' OR title LIKE '%Sport%' OR title LIKE '%Athlete%'").fetchone()[0]
    hospitality = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Hospitality%'").fetchone()[0]
    research = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Science, Research%'").fetchone()[0]
    law = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Law%'").fetchone()[0]
    education = c.execute("SELECT COUNT(*) FROM careers WHERE category LIKE '%Education%'").fetchone()[0]

    careers_with_roadmaps = c.execute('SELECT COUNT(DISTINCT career_id) FROM career_roadmaps').fetchone()[0]
    careers_without_roadmaps = total - careers_with_roadmaps

    print("=== SECTION 39 REPORT NUMBERS ===")
    print(f"Total careers: {total}")
    print(f"Total career domains: 26 (Domains A-Z mapped across {len(categories)} distinct sectors)")
    print(f"Total categories: {len(categories)}")
    print(f"Total subcategories: {subcategories_cnt}")
    print(f"Total verified careers: {verified}")
    print(f"Total careers needing review: {review}")
    print(f"Total career-course relationships: {courses}")
    print(f"Total career-exam relationships: {exams}")
    print(f"Total career-skill relationships: {skills}")
    print(f"Total careers with roadmaps: {careers_with_roadmaps}")
    print(f"Total careers without roadmaps: {careers_without_roadmaps}")
    print(f"Total lesser-known careers: {lesser_known}")
    print(f"Total government career pathways: {govt}")
    print(f"Total healthcare careers: {healthcare}")
    print(f"Total arts/humanities careers: {arts}")
    print(f"Total commerce/finance careers: {commerce}")
    print(f"Total agriculture careers: {agri}")
    print(f"Total creative careers: {creative}")
    print(f"Total vocational careers: {trades}")
    print(f"Total sports careers: {sports}")
    print(f"Total hospitality careers: {hospitality}")
    print(f"Total research careers: {research}")
    print(f"Total law careers: {law}")
    print(f"Total education careers: {education}")

    print("\n--- Complete Category Breakdown ---")
    for cat, cnt in categories:
        pct = round(cnt / total * 100, 1)
        print(f"  * {cat}: {cnt} ({pct}%)")

if __name__ == '__main__':
    run_report()
