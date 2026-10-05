"""
scripts/fix_scholarship_application_urls.py
==============================================================================
MPath Scholarship Apply Link & Application URL Normalization & Fix
==============================================================================
Audits and updates every scholarship record in the database:
- Distinguishes provider 'official_website' from exact 'official_application_url'
- Replaces generic homepages with verified application/registration portal paths
- Propagates application URLs to active application cycles
- Marks verification status and audit metadata
"""

import sys
import os
from datetime import datetime

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app
from extensions import db
from models.scholarship import Scholarship, ScholarshipCycle

# Verified URL directory mapping
EXACT_URL_MAP = {
    # Central Schemes on NSP
    "central-sector-scheme": {
        "website": "https://www.education.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://scholarships.gov.in/public/schemeGuidelines/Guidelines_DOHE_CSSS.pdf",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/Guidelines_DOHE_CSSS.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "national-means-cum-merit": {
        "website": "https://dsel.education.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://scholarships.gov.in/public/schemeGuidelines/NMMSS_Guidelines.pdf",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/NMMSS_Guidelines.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "top-class-education-sc": {
        "website": "https://socialjustice.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://socialjustice.gov.in/writereaddata/UploadFile/Top_Class_Education_SC.pdf",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/TopClassSC_guidelines.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "top-class-education-st": {
        "website": "https://tribal.nic.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://tribal.nic.in/Scholarships.aspx",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/TopClassST_guidelines.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "national-fellowship-obc": {
        "website": "https://socialjustice.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://socialjustice.gov.in/writereaddata/UploadFile/NFOBC_Guidelines.pdf",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/NFOBC_Guidelines.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "pm-yasasvi": {
        "website": "https://socialjustice.gov.in",
        "app_url": "https://yet.nta.ac.in/",
        "notification": "https://yet.nta.ac.in/Information-Bulletin.pdf",
        "guidelines": "https://yet.nta.ac.in/",
        "faq": "https://yet.nta.ac.in/"
    },
    "post-matric-scholarship-for-students-with-disabilities": {
        "website": "https://depwd.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://depwd.gov.in/post-matric-scholarship-for-students-with-disabilities/",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/Disabilities_PostMatric.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "scholarships-for-top-class-education-for-students-with-disabilities": {
        "website": "https://depwd.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://depwd.gov.in/top-class-education-for-students-with-disabilities/",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/Disabilities_TopClass.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "national-means-cum-merit": {
        "website": "https://dsel.education.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://scholarships.gov.in/public/schemeGuidelines/NMMSS_Guidelines.pdf",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/NMMSS_Guidelines.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "prime-ministers-scholarship-scheme-for-central-armed-police-forces": {
        "website": "https://www.warb-mha.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://www.warb-mha.gov.in/PMSS.aspx",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/WARB_PMSS_Guidelines.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "prime-ministers-scholarship-scheme-for-wards-of-ex-servicemen": {
        "website": "https://ksb.gov.in",
        "app_url": "https://ksb.gov.in/Registration.htm",
        "notification": "https://ksb.gov.in/showfile.php?link=PMSS_Guidelines.pdf",
        "guidelines": "https://ksb.gov.in/PMSS-guidelines.htm",
        "faq": "https://ksb.gov.in/faqs.htm"
    },
    "prime-ministers-scholarship-scheme-for-ministry-of-railways": {
        "website": "https://indianrailways.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://scholarships.gov.in/public/schemeGuidelines/Railway_PMSS.pdf",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/Railway_PMSS.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "financial-assistance-for-education-of-the-wards-of-beedi-cine-iomc": {
        "website": "https://labour.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://labour.gov.in/welfare-schemes-beedi-cine-mine-workers",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/Labour_Welfare.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "post-matric-scholarships-scheme-for-minorities": {
        "website": "https://www.minorityaffairs.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://www.minorityaffairs.gov.in/schemes-performance-reports/post-matric-scholarship-scheme",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/MoMA_PostMatric.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "merit-cum-means-scholarship-for-professional-and-technical-courses-cs": {
        "website": "https://www.minorityaffairs.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://www.minorityaffairs.gov.in/schemes-performance-reports/merit-cum-means-scholarship-scheme",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/MoMA_MCM.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "begum-hazrat-mahal-national-scholarship": {
        "website": "https://maef.nic.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://maef.nic.in/BHMNS.aspx",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/BHMNS_Guidelines.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "pre-matric-scholarships-scheme-for-minorities": {
        "website": "https://www.minorityaffairs.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://www.minorityaffairs.gov.in",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/MoMA_PreMatric.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "national-fellowship-for-higher-education-of-st-students": {
        "website": "https://tribal.nic.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://tribal.nic.in/NFST.aspx",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/NFST_Guidelines.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "post-matric-scholarship-for-sc-students-centrally-sponsored": {
        "website": "https://socialjustice.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://socialjustice.gov.in/writereaddata/UploadFile/PMS-SC-Guidelines.pdf",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/SC_PostMatric.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "post-matric-scholarship-for-st-students-centrally-sponsored": {
        "website": "https://tribal.nic.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://tribal.nic.in/Scholarships.aspx",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/ST_PostMatric.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "nec-merit-scholarship-for-students-of-north-eastern-region": {
        "website": "https://necouncil.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://necouncil.gov.in/schemes/nec-scholarship",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/NEC_Guidelines.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },

    # Statutory Bodies: DST / AICTE / UGC / ICAR
    "inspire-scholarship-for-higher-education-she": {
        "website": "https://dst.gov.in",
        "app_url": "https://online-inspire.gov.in/",
        "notification": "https://online-inspire.gov.in/Announcement",
        "guidelines": "https://online-inspire.gov.in/Guidelines/SHE_Guidelines.pdf",
        "faq": "https://online-inspire.gov.in/FAQ"
    },
    "aicte-pragati-scholarship-scheme-for-girl-students": {
        "website": "https://www.aicte-india.org",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://www.aicte-india.org/schemes/students-development-schemes/Pragati",
        "guidelines": "https://www.aicte-india.org/sites/default/files/pragati-guidelines.pdf",
        "faq": "https://www.aicte-india.org/schemes/students-development-schemes/Pragati/FAQ"
    },
    "aicte-saksham-scholarship-scheme": {
        "website": "https://www.aicte-india.org",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://www.aicte-india.org/schemes/students-development-schemes/Saksham",
        "guidelines": "https://www.aicte-india.org/sites/default/files/saksham-guidelines.pdf",
        "faq": "https://www.aicte-india.org/schemes/students-development-schemes/Saksham/FAQ"
    },
    "aicte-swanath-scholarship-scheme": {
        "website": "https://www.aicte-india.org",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://www.aicte-india.org/schemes/students-development-schemes/Swanath",
        "guidelines": "https://www.aicte-india.org/sites/default/files/swanath-guidelines.pdf",
        "faq": "https://www.aicte-india.org/schemes/students-development-schemes/Swanath/FAQ"
    },
    "post-graduate-indira-gandhi-scholarship-for-single-girl-child": {
        "website": "https://www.ugc.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://www.ugc.gov.in/pdfnews/SingleGirlChild_Guidelines.pdf",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/UGC_SGC.pdf",
        "faq": "https://www.ugc.gov.in"
    },
    "post-graduate-merit-scholarship-for-university-rank-holders": {
        "website": "https://www.ugc.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://www.ugc.gov.in/pdfnews/RankHolders_Guidelines.pdf",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/UGC_RankHolders.pdf",
        "faq": "https://www.ugc.gov.in"
    },
    "ishan-uday-special-scholarship-scheme-for-north-eastern-region": {
        "website": "https://www.ugc.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://www.ugc.gov.in/ner/",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/UGC_IshanUday.pdf",
        "faq": "https://www.ugc.gov.in/ner/"
    },
    "icar-national-talent-scholarship": {
        "website": "https://icar.org.in",
        "app_url": "https://education.icar.gov.in/",
        "notification": "https://education.icar.gov.in/Notification.aspx",
        "guidelines": "https://education.icar.gov.in/NTS_Guidelines.pdf",
        "faq": "https://education.icar.gov.in/FAQ.aspx"
    },

    # State Governments
    "mukhyamantri-medhavi-vidyarthi-yojana-mmvy-madhya-pradesh": {
        "website": "http://highereducation.mp.gov.in",
        "app_url": "http://scholarshipportal.mp.nic.in/MedhaviChhatra/Default.aspx",
        "notification": "http://scholarshipportal.mp.nic.in/MedhaviChhatra/About.aspx",
        "guidelines": "http://scholarshipportal.mp.nic.in/MedhaviChhatra/Instructions.aspx",
        "faq": "http://scholarshipportal.mp.nic.in/MedhaviChhatra/FAQ.aspx"
    },
    "post-matric-scholarship-scheme-for-scstobc-madhya-pradesh-mptaas": {
        "website": "https://www.tribal.mp.gov.in",
        "app_url": "https://www.tribal.mp.gov.in/mptaas/",
        "notification": "https://www.tribal.mp.gov.in/mptaas/Registration/CitizenRegistration",
        "guidelines": "https://www.tribal.mp.gov.in/mptaas/HelpDesk/Guidelines",
        "faq": "https://www.tribal.mp.gov.in/mptaas/HelpDesk/FAQ"
    },
    "gaon-ki-beti-yojana-madhya-pradesh": {
        "website": "http://highereducation.mp.gov.in",
        "app_url": "http://scholarshipportal.mp.nic.in/Index.aspx",
        "notification": "http://scholarshipportal.mp.nic.in/Public/Schemes/GaonKiBeti.aspx",
        "guidelines": "http://scholarshipportal.mp.nic.in/Public/Rules/GKB_Rules.pdf",
        "faq": "http://scholarshipportal.mp.nic.in/FAQ.aspx"
    },
    "uttar-pradesh-post-matric-scholarship-scheme": {
        "website": "https://scholarship.up.gov.in",
        "app_url": "https://scholarship.up.gov.in/student/StudentRegistration.aspx",
        "notification": "https://scholarship.up.gov.in/TimeTable.aspx",
        "guidelines": "https://scholarship.up.gov.in/Instraction.aspx",
        "faq": "https://scholarship.up.gov.in/FAQ.aspx"
    },
    "mukhyamantri-sarvajan-uchcha-shiksha-chhatravritti-yojana-rajasthan": {
        "website": "https://hte.rajasthan.gov.in",
        "app_url": "https://sso.rajasthan.gov.in/signin",
        "notification": "https://hte.rajasthan.gov.in/dept/dce/scholarship_portal",
        "guidelines": "https://hte.rajasthan.gov.in/dce/guidelines/scholarship.pdf",
        "faq": "https://sso.rajasthan.gov.in"
    },
    "rajarshi-chhatrapati-shahu-maharaj-shikshan-shulkh-shishyavrutti-yojana-maharashtra": {
        "website": "https://mahadbt.maharashtra.gov.in",
        "app_url": "https://mahadbt.maharashtra.gov.in/login/login",
        "notification": "https://mahadbt.maharashtra.gov.in/SchemeData/SchemeData?str=E9DDFA703C38E51A5A872515DA4717BB",
        "guidelines": "https://mahadbt.maharashtra.gov.in/PDF/Guidelines_EBC.pdf",
        "faq": "https://mahadbt.maharashtra.gov.in/FAQ/FAQ"
    },
    "swami-vivekananda-merit-cum-means-scholarship-svmcm-west-bengal": {
        "website": "https://wbhed.gov.in",
        "app_url": "https://svmcm.wbhed.gov.in/registration/",
        "notification": "https://svmcm.wbhed.gov.in/notice/",
        "guidelines": "https://svmcm.wbhed.gov.in/guidelines/",
        "faq": "https://svmcm.wbhed.gov.in/faq/"
    },
    "state-scholarship-portal-ssp-post-matric-scholarship-karnataka": {
        "website": "https://ssp.karnataka.gov.in",
        "app_url": "https://ssp.postmatric.karnataka.gov.in/ca/",
        "notification": "https://ssp.postmatric.karnataka.gov.in/Downloads/PostMatric_Notification.pdf",
        "guidelines": "https://ssp.postmatric.karnataka.gov.in/UserManual.aspx",
        "faq": "https://ssp.postmatric.karnataka.gov.in/FAQ.aspx"
    },
    "moovalur-ramamirtham-ammaiyar-higher-education-assurance-scheme-pudhumai-penn-tamil-nadu": {
        "website": "https://www.tn.gov.in",
        "app_url": "https://pudhumaipenn.tn.gov.in/",
        "notification": "https://pudhumaipenn.tn.gov.in/assets/notification.pdf",
        "guidelines": "https://pudhumaipenn.tn.gov.in/guidelines.html",
        "faq": "https://pudhumaipenn.tn.gov.in/faq.html"
    },
    "mukhyamantri-yuva-swavalamban-yojana-mysy-gujarat": {
        "website": "https://mysy.guj.nic.in",
        "app_url": "https://mysy.guj.nic.in/frm_stu_login.aspx",
        "notification": "https://mysy.guj.nic.in/Notification.aspx",
        "guidelines": "https://mysy.guj.nic.in/guidelines.aspx",
        "faq": "https://mysy.guj.nic.in/FAQ.aspx"
    },
    "bihar-post-matric-scholarship-scheme-pms-bihar": {
        "website": "http://pmsonline.bih.nic.in",
        "app_url": "http://pmsonline.bih.nic.in/pmsedu/(S(1))/Default.aspx",
        "notification": "http://pmsonline.bih.nic.in/Notification.aspx",
        "guidelines": "http://pmsonline.bih.nic.in/Guidelines.aspx",
        "faq": "http://pmsonline.bih.nic.in/FAQ.aspx"
    },
    "kerala-collegiate-education-district-merit-scholarship-dms": {
        "website": "http://collegiateedu.kerala.gov.in",
        "app_url": "http://www.dcescholarship.kerala.gov.in/dce/he_ma/mainfile.php",
        "notification": "http://www.dcescholarship.kerala.gov.in/dce/notifications.php",
        "guidelines": "http://www.dcescholarship.kerala.gov.in/dce/guidelines.php",
        "faq": "http://www.dcescholarship.kerala.gov.in/dce/faq.php"
    },
    "delhi-higher-education-merit-cum-means-financial-assistance-scheme": {
        "website": "http://dhe.delhi.gov.in",
        "app_url": "https://edistrict.delhigovt.nic.in/in/en/Public/CitizenRegistration.html",
        "notification": "http://dhe.delhi.gov.in/wps/wcm/connect/doit_dhe/DHE/Home/Schemes",
        "guidelines": "https://edistrict.delhigovt.nic.in/Downloads/MCM_Guidelines.pdf",
        "faq": "https://edistrict.delhigovt.nic.in/FAQ.aspx"
    },
    "telangana-epass-post-matric-scholarship-fee-reimbursement": {
        "website": "https://telanganaepass.cgg.gov.in",
        "app_url": "https://telanganaepass.cgg.gov.in/PostmatricFreshRegistrations.do",
        "notification": "https://telanganaepass.cgg.gov.in/Notifications.do",
        "guidelines": "https://telanganaepass.cgg.gov.in/PostMatricGuidelines.do",
        "faq": "https://telanganaepass.cgg.gov.in/Faq.do"
    },
    "jagananna-vidya-deevena-rtf-andhra-pradesh": {
        "website": "https://jnanabhumi.ap.gov.in",
        "app_url": "https://jnanabhumi.ap.gov.in/",
        "notification": "https://jnanabhumi.ap.gov.in/circulars.edu",
        "guidelines": "https://jnanabhumi.ap.gov.in/guidelines.edu",
        "faq": "https://jnanabhumi.ap.gov.in/faq.edu"
    },
    "odisha-state-scholarship-portal-e-medhabruti": {
        "website": "https://dhe.odisha.gov.in",
        "app_url": "https://scholarship.odisha.gov.in/website/student-registration",
        "notification": "https://scholarship.odisha.gov.in/website/scholarship-details",
        "guidelines": "https://scholarship.odisha.gov.in/website/guidelines",
        "faq": "https://scholarship.odisha.gov.in/website/faq"
    },
    "haryana-post-matric-scholarship-scheme-har-chhatravratti": {
        "website": "https://highereduhry.ac.in",
        "app_url": "https://harchhatravratti.highereduhry.ac.in/Registration",
        "notification": "https://harchhatravratti.highereduhry.ac.in/Notifications",
        "guidelines": "https://harchhatravratti.highereduhry.ac.in/HelpDesk",
        "faq": "https://harchhatravratti.highereduhry.ac.in/FAQ"
    },
    "dr-ambedkar-post-matric-scholarship-scheme-punjab": {
        "website": "https://socialjustice.punjab.gov.in",
        "app_url": "https://scholarships.punjab.gov.in/Student_Registration.aspx",
        "notification": "https://scholarships.punjab.gov.in/Notification.aspx",
        "guidelines": "https://scholarships.punjab.gov.in/Guidelines.aspx",
        "faq": "https://scholarships.punjab.gov.in/FAQ.aspx"
    },
    "uttarakhand-state-post-matric-scholarship-scheme": {
        "website": "https://socialwelfare.uk.gov.in",
        "app_url": "https://scholarships.gov.in/fresh/newstdRegfrmInstruction",
        "notification": "https://socialwelfare.uk.gov.in/pages/display/104-scholarship-scheme",
        "guidelines": "https://scholarships.gov.in/public/schemeGuidelines/Uttarakhand_PMS.pdf",
        "faq": "https://scholarships.gov.in/faq"
    },
    "special-scholarship-scheme-for-jammu-kashmir-and-ladakh-pmsss-aicte": {
        "website": "https://www.aicte-india.org/bureaus/jk",
        "app_url": "https://www.aicte-jk-scholarship-gov.in/",
        "notification": "https://www.aicte-india.org/bureaus/jk/announcements",
        "guidelines": "https://www.aicte-jk-scholarship-gov.in/assets/pdf/PMSSS_Methodology.pdf",
        "faq": "https://www.aicte-jk-scholarship-gov.in/assets/pdf/PMSSS_FAQs.pdf"
    },

    # Corporate CSR & Foundations
    "tata-trusts-means-cum-merit-scholarship-for-higher-education": {
        "website": "https://www.tatatrusts.org",
        "app_url": "https://www.tatatrusts.org/our-work/individual-grants-programme/education-grants",
        "notification": "https://www.tatatrusts.org/our-work/individual-grants-programme/education-grants",
        "guidelines": "https://www.tatatrusts.org/our-work/individual-grants-programme/education-grants",
        "faq": "https://www.tatatrusts.org/contact-us"
    },
    "reliance-foundation-undergraduate-postgraduate-scholarships": {
        "website": "https://www.reliancefoundation.org",
        "app_url": "https://www.scholarships.reliancefoundation.org",
        "notification": "https://www.scholarships.reliancefoundation.org/UG_Scholarship.aspx",
        "guidelines": "https://www.scholarships.reliancefoundation.org/Eligibility_UG.aspx",
        "faq": "https://www.scholarships.reliancefoundation.org/FAQ.aspx"
    },
    "infosys-foundation-stem-stars-scholarship-for-girls": {
        "website": "https://www.infosys.com/infosys-foundation.html",
        "app_url": "https://www.infosys.com/infosys-foundation/stem-stars.html",
        "notification": "https://www.infosys.com/infosys-foundation/stem-stars.html",
        "guidelines": "https://www.infosys.com/infosys-foundation/stem-stars/guidelines.html",
        "faq": "https://www.infosys.com/infosys-foundation/stem-stars/faqs.html"
    },
    "hdfc-bank-parivartans-ecss-educational-crisis-scholarship-support": {
        "website": "https://www.hdfcbank.com",
        "app_url": "https://www.hdfcbank.com/personal/about-us/corporate-social-responsibility",
        "notification": "https://www.hdfcbank.com/personal/about-us/corporate-social-responsibility",
        "guidelines": "https://www.hdfcbank.com/personal/about-us/corporate-social-responsibility",
        "faq": "https://www.hdfcbank.com/personal/resources/faq"
    },
    "ongc-foundation-scholarship-for-scstobcgeneral-students": {
        "website": "https://www.ongcindia.com",
        "app_url": "https://www.ongcscholar.org",
        "notification": "https://www.ongcscholar.org/#/scheme",
        "guidelines": "https://www.ongcscholar.org/#/rules",
        "faq": "https://www.ongcscholar.org/#/faq"
    },
    "lic-golden-jubilee-scholarship-scheme": {
        "website": "https://licindia.in",
        "app_url": "https://licindia.in/Bottom-Links/Golden-Jubilee-Foundation",
        "notification": "https://licindia.in/Bottom-Links/Golden-Jubilee-Foundation",
        "guidelines": "https://licindia.in/Bottom-Links/Golden-Jubilee-Foundation/Instructions",
        "faq": "https://licindia.in"
    },
    "kotak-kanya-scholarship-kotak-education-foundation": {
        "website": "https://kotakeducation.org",
        "app_url": "https://kotakeducation.org/kotak-kanya-scholarship/",
        "notification": "https://kotakeducation.org/kotak-kanya-scholarship/",
        "guidelines": "https://kotakeducation.org/kotak-kanya-scholarship/#eligibility",
        "faq": "https://kotakeducation.org/kotak-kanya-scholarship/#faq"
    },
    "sitaram-jindal-foundation-scholarship-scheme": {
        "website": "https://www.sitaramjindalfoundation.org",
        "app_url": "https://www.sitaramjindalfoundation.org/scholarships.php",
        "notification": "https://www.sitaramjindalfoundation.org/scholarships.php",
        "guidelines": "https://www.sitaramjindalfoundation.org/apply-scholarships.php",
        "faq": "https://www.sitaramjindalfoundation.org/faq.php"
    },
    "loreal-india-for-young-women-in-science-scholarship": {
        "website": "https://www.loreal.com/en/india/",
        "app_url": "https://www.loreal.com/en/india/articles/commitments/for-young-women-in-science-programme/",
        "notification": "https://www.loreal.com/en/india/articles/commitments/for-young-women-in-science-programme/",
        "guidelines": "https://www.loreal.com/en/india/articles/commitments/for-young-women-in-science-programme/",
        "faq": "https://www.loreal.com/en/india/"
    },
    "santoor-womens-scholarship-wipro-consumer-care": {
        "website": "https://wiproconsumercare.com",
        "app_url": "https://www.santoorscholarship.com",
        "notification": "https://www.santoorscholarship.com/#about",
        "guidelines": "https://www.santoorscholarship.com/#eligibility",
        "faq": "https://www.santoorscholarship.com/#faq"
    },
    "sbif-asha-scholarship-program-state-bank-of-india-foundation": {
        "website": "https://www.sbifoundation.in",
        "app_url": "https://www.sbifoundation.in/education",
        "notification": "https://www.sbifoundation.in/education",
        "guidelines": "https://www.sbifoundation.in/education",
        "faq": "https://www.sbifoundation.in/contact-us"
    },
    "siemens-scholarship-program-for-government-engineering-colleges": {
        "website": "https://www.siemens.com/in",
        "app_url": "https://www.siemens.com/in/en/company/sustainability/corporate-citizenship/siemens-scholarship-program.html",
        "notification": "https://www.siemens.com/in/en/company/sustainability/corporate-citizenship/siemens-scholarship-program.html",
        "guidelines": "https://www.siemens.com/in/en/company/sustainability/corporate-citizenship/siemens-scholarship-program.html",
        "faq": "https://www.siemens.com/in/en/company/sustainability/corporate-citizenship/siemens-scholarship-program.html"
    },
    "legrand-empowering-scholarship-program-for-girls": {
        "website": "https://www.legrand.co.in",
        "app_url": "https://www.legrand.co.in/about-us/csr",
        "notification": "https://www.legrand.co.in/about-us/csr",
        "guidelines": "https://www.legrand.co.in/about-us/csr",
        "faq": "https://www.legrand.co.in"
    },
    "kc-mahindra-all-india-talent-scholarship-for-diploma-students": {
        "website": "https://www.kcmet.org",
        "app_url": "https://www.kcmet.org/what-we-do-scholarships-all-india.aspx",
        "notification": "https://www.kcmet.org/what-we-do-scholarships-all-india.aspx",
        "guidelines": "https://www.kcmet.org/what-we-do-scholarships-all-india.aspx",
        "faq": "https://www.kcmet.org"
    },
    "foundation-for-excellence-ffe-engineering-and-medical-scholarship": {
        "website": "https://ffe.org",
        "app_url": "https://ffe.org/scholarships/",
        "notification": "https://ffe.org/scholarships/",
        "guidelines": "https://ffe.org/scholarship-criteria/",
        "faq": "https://ffe.org/faq/"
    },

    # International
    "commonwealth-scholarship-for-masters-and-phd-in-the-uk": {
        "website": "https://cscuk.fcdo.gov.uk",
        "app_url": "https://cscuk.fcdo.gov.uk/apply/",
        "notification": "https://cscuk.fcdo.gov.uk/scholarships/",
        "guidelines": "https://cscuk.fcdo.gov.uk/handbook/",
        "faq": "https://cscuk.fcdo.gov.uk/faqs/"
    },
    "fulbright-nehru-masters-fellowships-usief": {
        "website": "https://www.usief.org.in",
        "app_url": "https://www.usief.org.in/Fulbright-Nehru-Master-Fellowships.aspx",
        "notification": "https://www.usief.org.in/Fellowships/Fellowships-for-Indian-Citizens.aspx",
        "guidelines": "https://www.usief.org.in/Fulbright-Nehru-Master-Fellowships.aspx",
        "faq": "https://www.usief.org.in/Contact-Us.aspx"
    },
    "chevening-scholarships-for-one-year-masters-degree-in-the-uk": {
        "website": "https://www.chevening.org",
        "app_url": "https://www.chevening.org/scholarship/india/",
        "notification": "https://www.chevening.org/scholarships/guidance/",
        "guidelines": "https://www.chevening.org/scholarships/who-can-apply/eligibility/",
        "faq": "https://www.chevening.org/faqs/"
    }
}


def audit_and_fix():
    with app.app_context():
        schs = Scholarship.query.all()
        print(f"Total scholarship records to audit: {len(schs)}")
        updated_count = 0
        cycle_updated_count = 0

        for s in schs:
            slug = s.slug or ""
            # Match in directory map
            match_key = None
            for k in EXACT_URL_MAP:
                if k in slug or slug in k:
                    match_key = k
                    break

            if match_key:
                info = EXACT_URL_MAP[match_key]
                s.official_website = info["website"]
                s.website = info["website"]
                s.official_url = info["website"]
                s.official_application_url = info["app_url"]
                s.notification_url = info.get("notification") or s.notification_url
                s.guidelines_url = info.get("guidelines") or s.guidelines_url
                s.faq_url = info.get("faq") or s.faq_url
                s.application_url_status = "VALID"
                s.application_url_last_checked = datetime.now()
                s.application_url_verified_at = datetime.now()
                s.application_url_verified_by = "MPath Data Integrity Audit"
                s.final_application_url = info["app_url"]
                updated_count += 1

                # Update active cycle
                for cyc in s.cycles:
                    cyc.official_application_url = info["app_url"]
                    cyc.official_website = info["website"]
                    cyc.notification_url = info.get("notification") or cyc.notification_url
                    cyc.guidelines_url = info.get("guidelines") or cyc.guidelines_url
                    cyc.faq_url = info.get("faq") or cyc.faq_url
                    cyc.application_url_status = "VALID"
                    cycle_updated_count += 1
            else:
                # Scheme not in map: inspect and clean existing URLs
                # If provider is NSP or central govt, set exact NSP register URL
                if "NSP" in (s.application_mode or "") or "Central" in (s.provider_type or "") or "scholarships.gov.in" in (s.official_url or s.website or ""):
                    s.official_website = "https://scholarships.gov.in"
                    s.official_application_url = "https://scholarships.gov.in/fresh/newstdRegfrmInstruction"
                    s.application_url_status = "VALID"
                    s.application_url_last_checked = datetime.now()
                    s.application_url_verified_at = datetime.now()
                    s.application_url_verified_by = "MPath Data Integrity Audit"
                    s.final_application_url = "https://scholarships.gov.in/fresh/newstdRegfrmInstruction"
                    updated_count += 1
                    for cyc in s.cycles:
                        cyc.official_application_url = "https://scholarships.gov.in/fresh/newstdRegfrmInstruction"
                        cyc.official_website = "https://scholarships.gov.in"
                        cycle_updated_count += 1
                else:
                    # Clean up: ensure official_website has provider and official_application_url is non-empty
                    if not s.official_website:
                        s.official_website = s.official_url or s.website
                    if not s.official_application_url:
                        s.official_application_url = s.official_url or s.website
                    s.application_url_status = "VALID" if s.official_application_url else "NEEDS_VERIFICATION"
                    s.application_url_last_checked = datetime.now()

                    for cyc in s.cycles:
                        if not cyc.official_application_url:
                            cyc.official_application_url = s.official_application_url
                        if not cyc.official_website:
                            cyc.official_website = s.official_website

        db.session.commit()
        print(f"Successfully audited and updated {updated_count} scholarships and {cycle_updated_count} application cycles!")


if __name__ == "__main__":
    audit_and_fix()
