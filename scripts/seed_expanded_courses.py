"""
scripts/seed_expanded_courses.py
Adds canonical non-engineering degree programs to courses table.
"""

import sqlite3

def add_courses():
    conn = sqlite3.connect("careerpathindia.db")
    c = conn.cursor()

    new_courses = [
        (49, 'BAMS (Bachelor of Ayurvedic Medicine & Surgery)', 'bams', 'UG', '5.5 Years', 'Ayurveda', 'Medical', 'PCB'),
        (50, 'BHMS (Bachelor of Homeopathic Medicine & Surgery)', 'bhms', 'UG', '5.5 Years', 'Homeopathy', 'Medical', 'PCB'),
        (51, 'BPT (Bachelor of Physiotherapy)', 'bpt', 'UG', '4.5 Years', 'Physiotherapy', 'Allied Health', 'PCB'),
        (52, 'BOT (Bachelor of Occupational Therapy)', 'bot', 'UG', '4.5 Years', 'Rehabilitation', 'Allied Health', 'PCB'),
        (53, 'B.V.Sc & AH (Veterinary Science)', 'bvsc', 'UG', '5.5 Years', 'Veterinary Medicine', 'Medical', 'PCB'),
        (54, 'BASLP (Audiology & Speech-Language Pathology)', 'baslp', 'UG', '4 Years', 'Audiology & Speech', 'Allied Health', 'PCB'),
        (55, 'B.Sc Medical Laboratory Technology (BMLT)', 'bmlt', 'UG', '3-4 Years', 'Pathology & Lab Tech', 'Allied Health', 'PCB'),
        (56, 'B.Sc Medical Imaging / Radiography', 'bsc-radiography', 'UG', '3-4 Years', 'Radiology', 'Allied Health', 'PCB'),
        (57, 'BA Journalism & Mass Communication (BJMC)', 'bjmc', 'UG', '3 Years', 'Journalism & Media', 'Media', 'Any'),
        (58, 'BFA (Bachelor of Fine Arts)', 'bfa', 'UG', '4 Years', 'Painting & Sculpture', 'Fine Arts', 'Any'),
        (59, 'BPA (Bachelor of Performing Arts)', 'bpa', 'UG', '3-4 Years', 'Music & Dance', 'Performing Arts', 'Any'),
        (60, 'B.P.Ed (Bachelor of Physical Education & Sports)', 'bped', 'UG', '3-4 Years', 'Sports Science', 'Physical Education', 'Any'),
        (61, 'BHM (Bachelor of Hotel Management & Catering)', 'bhm', 'UG', '3-4 Years', 'Hospitality Management', 'Hospitality', 'Any'),
        (62, 'B.Sc Nautical Science / Marine Training', 'bsc-nautical-science', 'UG', '3 Years', 'Maritime Operations', 'Marine & Nautical', 'PCM'),
        (63, 'B.Plan (Bachelor of Urban & Regional Planning)', 'bplan', 'UG', '4 Years', 'Urban Planning', 'Architecture & Planning', 'PCM / Any'),
        (64, 'ITI / National Trade Certificate (Vocational)', 'iti-trade-certificate', 'Diploma', '1-2 Years', 'Industrial Skilled Trades', 'Vocational Trades', 'Class 10 / 12'),
        (65, 'BLIS / MLIS (Library & Information Science)', 'blis-library-science', 'UG/PG', '1-2 Years', 'Library & Knowledge Systems', 'Information Science', 'Any'),
        (66, 'BSW / MSW (Social Work & Development)', 'msw-social-work', 'UG/PG', '2-3 Years', 'Social Work & Community', 'Social Sciences', 'Any'),
        (67, 'BA / B.Sc Psychology', 'ba-psychology', 'UG', '3 Years', 'Psychological Sciences', 'Social Sciences', 'Any'),
        (68, 'B.Sc (Hons) Forestry / Horticulture', 'bsc-forestry', 'UG', '4 Years', 'Forestry & Ecology', 'Agriculture', 'PCB / PCM')
    ]

    for item in new_courses:
        cid, name, short_name, level, duration, spec, disc, stream = item
        c.execute('SELECT id FROM courses WHERE id = ?', (cid,))
        if not c.fetchone():
            c.execute("""
                INSERT INTO courses (id, name, short_name, level, duration, specialization, discipline, stream, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (cid, name, short_name, level, duration, spec, disc, stream, f"Professional degree program in {spec}."))
            print(f"Added course {cid}: {name}")

    conn.commit()
    total = c.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    print(f"Total canonical degree courses in database: {total}")
    conn.close()

if __name__ == "__main__":
    add_courses()
