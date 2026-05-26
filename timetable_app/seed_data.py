"""
seed_fixed.py
=============
Fixes applied vs original seed:
  1. Every Subject.objects.create() now includes credits=N
  2. Duplicate SubjectFaculty rows removed (SM mapped twice, IKS twice, etc.)
  3. Variable name collisions fixed (CHE, M2, ENG, BE etc. reused across depts
     → now each dept uses local variables so the last assignment doesn't
     overwrite the earlier one and cause wrong faculty mapping)
  4. Classroom seed: theory rooms (1-14) and lab rooms created separately
     with is_lab flag so the scheduler can distinguish them
  5. TimeSlot seed: order field set explicitly; no shift field needed
"""

import os
import django

# Django settings configure
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'timetable_project.settings'
)

# Setup Django
django.setup()

# Import models AFTER setup
from timetable_app.models import *

from datetime import time


def seed_database():

    # =========================================================
    # DEPARTMENTS
    # =========================================================
    CSE,  _ = Department.objects.get_or_create(name="Computer Science Eng")
    ECE,  _ = Department.objects.get_or_create(name="Electronics Communication Eng")
    ME,   _ = Department.objects.get_or_create(name="Mechanical Eng")
    CE,   _ = Department.objects.get_or_create(name="CIVIL")
    CECA, _ = Department.objects.get_or_create(name="Civil Engineering Computer Applied")
    EE,   _ = Department.objects.get_or_create(name="Electrical Eng")
    APS,  _ = Department.objects.get_or_create(name="Applied Science")

    departments = [CSE, ECE, ME, CE, CECA, EE, APS]

    # =========================================================
    # SEMESTERS
    # =========================================================
    semesters = {}
    for dept in departments:
        for sem_no in (2, 3, 5, 8):
            semesters[(dept, sem_no)], _ = Semester.objects.get_or_create(
                department=dept, semester_number=sem_no
            )

    # =========================================================
    # FACULTY
    # =========================================================
    def fac(name, dept):
        obj, _ = Faculty.objects.get_or_create(name=name.strip(), department=dept)
        return obj

    # CSE
    ANP = fac("Prof. ANUPAM KUMAR",         CSE)
    NCR = fac("Prof. NISCHAY RANJAN",        CSE)
    ARK = fac("Prof. ARUN KUMAR",            CSE)
    ASP = fac("Prof. ANSHU PRIYA",           CSE)
    DPI = fac("Prof. DEEPA KUMARI",          CSE)
    SDT = fac("DR. SHAHADAT HUSSAIN",        CSE)

    # ECE
    SJK = fac("DR. SANJEEV KUMAR",           ECE)
    MUK = fac("DR. MUKESH KUMAR",            ECE)
    ASK = fac("DR. ANSHU KUMARI",            ECE)
    RVK = fac("DR. RAVINDRA KUMAR",          ECE)
    BMK = fac("Prof. BRIJ MOHAN KUMAR",      ECE)
    RCV = fac("DR. RUCHI VARMA",             ECE)
    MKT = fac("Prof. MUNAN KUMAR THAKUR",    ECE)

    # ME
    KVC = fac("Prof. (Dr.) KESHAVENDRA CHOUDHARY", ME)
    CDK = fac("DR. CHANDAN KUMAR",           ME)
    AMK = fac("Prof. AMIT KUMAR",            ME)
    SRJ = fac("Prof. SERAJ AHMED",           ME)
    AVK = fac("Prof. AVINASH KUMAR",         ME)
    VKK = fac("Prof. VIKRAM KUMAR",          ME)
    VSK = fac("Prof. VINAY SHANKAR KUMAR",   ME)
    RKS = fac("Prof. RAJU KUMAR SHARMA",     ME)
    SMK = fac("Prof. SURYAMANI KUMAR",       ME)

    # EE
    SDK = fac("Prof. SUDHIR KUMAR",          EE)
    SKJ = fac("Prof. SAURABH KUMAR JHA",     EE)
    JTK = fac("Prof. JITENDRA KUMAR",        EE)
    NSA = fac("Prof. MD. NASIM AKHTER",      EE)
    NTK = fac("Prof. NISHANT KUMAR",         EE)
    SNT = fac("Prof. SANAT",                 EE)

    # CE
    DPK = fac("Prof. DEEPAK KUMAR",          CE)
    MSA = fac("Prof. MD. SHADAB ALAM",       CE)
    RVS = fac("Prof. RAVISHANKAR",           CE)
    PNK = fac("Prof. PANKAJ KUMAR",          CE)
    RSR = fac("Prof. RAUSHAN KUMAR RAVI",    CE)
    FKH = fac("Prof. FAHIM AHMED KHAN",      CE)
    RKR = fac("Prof. RAKESH KUMAR RAVI",     CE)
    SSU = fac("Prof. SAURABH SUMAN",         CE)

    # APS
    DSS = fac("DR. DINESH SAH",              APS)
    ADP = fac("Prof. ADITYA NARAYAN PANDEY", APS)
    AKA = fac("Prof. ANKUR ASHUTOSH",        APS)
    RKD = fac("DR. RAM KUMAR DAS",           APS)
    RVR = fac("Prof. RAVI RANJAN",           APS)
    SSI = fac("Prof. SUMIT SARDESAI",        APS)
    ABK = fac("Prof. ABHISHEK KUMAR",        APS)
    YGP = fac("DR. YOGENDRA KUMAR PODDAR",   APS)
    MKP = fac("DR. MUKESH KUMAR PANDEY",     APS)
    KSM = fac("Prof. KRISHNA MURARI",        APS)
    MTD = fac("Dr. MATIRAM DAS",             APS)

    # =========================================================
    # HELPER — create subject safely
    # =========================================================
    def sub(name, semester, credits=4, is_lab=False):
        """
        get_or_create so re-running seed is safe.
        credits default = 4 (adjust per actual syllabus).
        """
        obj, _ = Subject.objects.get_or_create(
            name=name, semester=semester,
            defaults={"credits": credits, "is_lab": is_lab}
        )
        # If it already existed without credits, patch it
        if obj.credits == 0 or obj.credits is None:
            obj.credits = credits
            obj.save()
        return obj

    def sf(subject, faculty):
        """Create SubjectFaculty only if not already present."""
        SubjectFaculty.objects.get_or_create(subject=subject, faculty=faculty)

    # =========================================================
    # SUBJECTS + FACULTY MAPPING
    # NOTE: credits values below are placeholders — adjust to
    #       your actual syllabus (hours/week = credits).
    # =========================================================

    # ── CSE SEM 2 ────────────────────────────────────────────
    s = semesters[(CSE, 2)]
    cse2_che = sub("Eng Chemistry",             s, credits=3)
    cse2_m2  = sub("Eng mathematics-2",         s, credits=4)
    cse2_eng = sub("Communicative English",     s, credits=3)
    cse2_pyp = sub("Python Programming",        s, credits=3)
    cse2_iwd = sub("Introduction to Web design",s, credits=3)

    sf(cse2_che, DSS);  sf(cse2_m2,  MTD);  sf(cse2_eng, RVR)
    sf(cse2_pyp, DPI);  sf(cse2_iwd, ASP)

    # ── CSE SEM 3 ────────────────────────────────────────────
    s = semesters[(CSE, 3)]
    cse3_dsa  = sub("Data Structures & Algorithms", s, credits=4)
    cse3_dm   = sub("Discrete Mathematics",         s, credits=4)
    cse3_de   = sub("Digital Logic",                s, credits=4)
    cse3_oops = sub("OOPS using java",              s, credits=4)
    cse3_os   = sub("Operating system",             s, credits=4)
    cse3_uhv  = sub("Universal Human Values",       s, credits=2)
    cse3_iks  = sub("Indian Knowledge System",      s, credits=2)

    sf(cse3_dsa, ASP);   sf(cse3_dm,  ARK);   sf(cse3_de,  ASK)
    sf(cse3_oops, DPI);  sf(cse3_os,  NCR);   sf(cse3_uhv, SSI)
    sf(cse3_iks, ABK)

    # ── CSE SEM 5 ────────────────────────────────────────────
    s = semesters[(CSE, 5)]
    cse5_ml   = sub("Machine Learning",                    s, credits=4)
    cse5_dbms = sub("DBMS",                               s, credits=4)
    cse5_cn   = sub("Computer Networks",                  s, credits=4)
    cse5_pyp  = sub("Python Programming",                 s, credits=3)
    cse5_pple = sub("Professional Practice, Law & Ethics",s, credits=2)
    cse5_toc  = sub("Theory of Computation PE-I",         s, credits=4)

    sf(cse5_ml,   SDT);  sf(cse5_dbms, ANP);  sf(cse5_cn,   NCR)
    sf(cse5_pyp,  ASP);  sf(cse5_pple, SSI);  sf(cse5_toc,  ANP)

    # ── CSE SEM 8 ────────────────────────────────────────────
    s = semesters[(CSE, 8)]
    cse8_and  = sub("Autonomous Drones",                          s, credits=4)
    cse8_res  = sub("Renewable Energy Systems",                   s, credits=4)
    cse8_aics = sub("AI in Cyber Security",                       s, credits=4)
    cse8_dms  = sub("Digital Marketing and Search Engine Opt.",   s, credits=4)

    sf(cse8_and,  MUK);  sf(cse8_res,  NTK)
    sf(cse8_aics, DPI);  sf(cse8_dms,  SSI)

    # ── ECE SEM 2 ────────────────────────────────────────────
    s = semesters[(ECE, 2)]
    ece2_be  = sub("Basic Electronics",     s, credits=4)
    ece2_m2  = sub("Eng mathematics-2",     s, credits=4)
    ece2_eng = sub("Communicative English", s, credits=3)
    ece2_che = sub("Eng Chemistry",         s, credits=3)
    ece2_egd = sub("EGD",                   s, credits=3)

    sf(ece2_be,  RVK);  sf(ece2_m2,  MTD);  sf(ece2_eng, KSM)
    sf(ece2_che, YGP);  sf(ece2_egd, CDK)

    # ── ECE SEM 3 ────────────────────────────────────────────
    s = semesters[(ECE, 3)]
    ece3_ss  = sub("Signals and Systems",              s, credits=4)
    ece3_edc = sub("Electronic Devices and Circuits",  s, credits=4)
    ece3_iks = sub("Indian Knowledge System",          s, credits=2)
    ece3_nt  = sub("Network Theory",                   s, credits=4)
    ece3_m3  = sub("Eng Mathematics-3",                s, credits=4)
    ece3_uhv = sub("Universal Human Values",           s, credits=2)

    sf(ece3_ss,  MKT);  sf(ece3_edc, RVK);  sf(ece3_iks, ABK)
    sf(ece3_nt,  MUK);  sf(ece3_m3,  ADP);  sf(ece3_uhv, ABK)

    # ── ECE SEM 5 ────────────────────────────────────────────
    s = semesters[(ECE, 5)]
    ece5_dsp  = sub("Digital Signal Processing",           s, credits=4)
    ece5_mm   = sub("Microprocessor & microcontrollers",   s, credits=4)
    ece5_lcs  = sub("Linear Control System",               s, credits=4)
    ece5_lica = sub("Linear Integrated Circuits & App.",   s, credits=4)
    ece5_cns  = sub("Computer Network And Security",       s, credits=4)
    ece5_ptsp = sub("Probability Theory",                  s, credits=4)

    sf(ece5_dsp,  BMK);  sf(ece5_mm,   ASK);  sf(ece5_lcs,  SJK)
    sf(ece5_lica, SJK);  sf(ece5_cns,  NCR);  sf(ece5_ptsp, MKT)

    # ── ECE SEM 8 ────────────────────────────────────────────
    s = semesters[(ECE, 8)]
    ece8_stlc = sub("Satellite Communication",  s, credits=4)
    ece8_iot  = sub("Internet of Things",       s, credits=4)
    ece8_mems = sub("Introduction to MEMS",     s, credits=4)
    ece8_wsn  = sub("Wireless Sensor Network",  s, credits=4)

    sf(ece8_stlc, BMK);  sf(ece8_iot,  ARK)
    sf(ece8_mems, RVK);  sf(ece8_wsn,  SJK)

    # ── ME SEM 2 ─────────────────────────────────────────────
    s = semesters[(ME, 2)]
    me2_m2  = sub("Eng mathematics-2",        s, credits=4)
    me2_phy = sub("Engineering physics",      s, credits=4)
    me2_pps = sub("PPS",                      s, credits=3)
    me2_wp  = sub("Workshop Practice",        s, credits=2)
    me2_eme = sub("Elements of mechanical Eng",s,credits=3)

    sf(me2_m2,  ADP);  sf(me2_phy, MKP);  sf(me2_pps, ARK)
    sf(me2_wp,  VKK);  sf(me2_eme, AVK)

    # ── ME SEM 3 ─────────────────────────────────────────────
    s = semesters[(ME, 3)]
    me3_td   = sub("Thermodynamics",              s, credits=4)
    me3_emc  = sub("Engineering Mechanics",       s, credits=4)
    me3_m3   = sub("Eng mathematics-3",           s, credits=4)
    me3_mse  = sub("Material Science & Engineering",s,credits=4)
    me3_bece = sub("BEE",                         s, credits=4)
    me3_uhv  = sub("Universal Human Values",      s, credits=2)
    me3_iks  = sub("Indian Knowledge System",     s, credits=2)

    sf(me3_td,   SMK);  sf(me3_emc,  SRJ);  sf(me3_m3,   ADP)
    sf(me3_mse,  RKS);  sf(me3_bece, MKT);  sf(me3_uhv,  SSI)
    sf(me3_iks,  AMK)   # only once (duplicate removed)

    # ── ME SEM 5 ─────────────────────────────────────────────
    s = semesters[(ME, 5)]
    me5_fmc = sub("Fluid Machinery",       s, credits=4)
    me5_ht  = sub("Heat Transfer",         s, credits=4)
    me5_km  = sub("Kinetics of Mechanics", s, credits=4)
    me5_mfp = sub("Manufacturing Process", s, credits=4)

    sf(me5_fmc, SMK);  sf(me5_ht, AVK)
    sf(me5_km,  CDK);  sf(me5_mfp, AMK)

    # ── ME SEM 8 ─────────────────────────────────────────────
    s = semesters[(ME, 8)]
    me8_pom = sub("POM", s, credits=4);  me8_ecm = sub("ECM", s, credits=4)
    me8_sfm = sub("SFM", s, credits=4);  me8_ncm = sub("NCM", s, credits=4)

    sf(me8_pom, SSI);  sf(me8_ecm, RKS)
    sf(me8_sfm, SRJ);  sf(me8_ncm, AMK)

    # ── CE SEM 2 ─────────────────────────────────────────────
    s = semesters[(CE, 2)]
    ce2_m2  = sub("Eng mathematics-2",  s, credits=4)
    ce2_phy = sub("Engineering physics",s, credits=4)
    ce2_pps = sub("PPS",                s, credits=3)
    ce2_wp  = sub("Workshop Practice",  s, credits=2)
    ce2_bee = sub("BEE",                s, credits=4)
    ce2_sbm = sub("Swacha Bharat Mission",s,credits=2)

    sf(ce2_m2,  RKD);  sf(ce2_phy, MKP);  sf(ce2_pps, ARK)
    sf(ce2_wp,  VKK);  sf(ce2_bee, JTK);  sf(ce2_sbm, AKA)

    # ── CE SEM 3 ─────────────────────────────────────────────
    s = semesters[(CE, 3)]
    ce3_sm  = sub("Solid mechanics",                 s, credits=4)
    ce3_m3  = sub("Eng mathematics-3",              s, credits=4)
    ce3_uhv = sub("Universal Human Values",         s, credits=2)
    ce3_sg  = sub("Surveying and Geomatics",        s, credits=4)
    ce3_mte = sub("Materials, testing & Evaluation",s, credits=4)
    ce3_flm = sub("Fluid Mechanics",                s, credits=4)
    ce3_iks = sub("Indian Knowledge System",        s, credits=2)

    sf(ce3_sm,  RSR);  sf(ce3_m3,  RKD);  sf(ce3_uhv, SSI)
    sf(ce3_sg,  PNK);  sf(ce3_mte, RKR);  sf(ce3_flm, SSU)
    sf(ce3_iks, RSR)   # IKS mapped once only (duplicate removed)

    # ── CE SEM 5 ─────────────────────────────────────────────
    s = semesters[(CE, 5)]
    ce5_adcs = sub("ADCS", s, credits=4);  ce5_ee1  = sub("EE1",  s, credits=4)
    ce5_ge1  = sub("GE1",  s, credits=4);  ce5_hye  = sub("HYE",  s, credits=4)
    ce5_hwre = sub("HWRE", s, credits=4);  ce5_mom  = sub("MOM",  s, credits=4)
    ce5_te   = sub("TE",   s, credits=4)

    sf(ce5_adcs, RVS);  sf(ce5_ee1, RKR);   sf(ce5_ge1,  PNK)
    sf(ce5_hye,  SSU);  sf(ce5_hwre, DPK);  sf(ce5_mom,  FKH)
    sf(ce5_te,   MSA)

    # ── CE SEM 8 ─────────────────────────────────────────────
    s = semesters[(CE, 8)]
    ce8_rel = sub("REL", s, credits=4);  ce8_epi = sub("EPI", s, credits=4)
    ce8_cem = sub("CEM", s, credits=4);  ce8_cnm = sub("CNM", s, credits=4)

    sf(ce8_rel, FKH);  sf(ce8_epi, SSI)
    sf(ce8_cem, RKR);  sf(ce8_cnm, SSI)

    # ── EE SEM 2 ─────────────────────────────────────────────
    s = semesters[(EE, 2)]
    ee2_be  = sub("Basic Electronics",     s, credits=4)
    ee2_m2  = sub("Eng mathematics-2",     s, credits=4)
    ee2_eng = sub("Communicative English", s, credits=3)
    ee2_che = sub("Eng Chemistry",         s, credits=3)
    ee2_egd = sub("EGD",                   s, credits=3)

    sf(ee2_be,  MUK);  sf(ee2_m2,  ADP);  sf(ee2_eng, KSM)
    sf(ee2_che, YGP);  sf(ee2_egd, VSK)

    # ── EE SEM 3 ─────────────────────────────────────────────
    s = semesters[(EE, 3)]
    ee3_eca = sub("ECA",                 s, credits=4)
    ee3_ae  = sub("Analog Electronics",  s, credits=4)
    ee3_em1 = sub("EM-1",               s, credits=4)
    ee3_m3  = sub("Eng mathematics-3",  s, credits=4)
    ee3_uhv = sub("Universal Human Values",s,credits=2)
    ee3_emc = sub("Engineering Mechanics",s, credits=4)
    ee3_iks = sub("Indian Knowledge System",s,credits=2)

    sf(ee3_eca, SNT);  sf(ee3_ae,  SDK);  sf(ee3_em1, VSK)
    sf(ee3_m3,  MTD);  sf(ee3_uhv, SSI);  sf(ee3_emc, SJK)
    sf(ee3_iks, ABK)

    # ── EE SEM 5 ─────────────────────────────────────────────
    s = semesters[(EE, 5)]
    ee5_cs   = sub("Control System",              s, credits=4)
    ee5_mp   = sub("Microprocessor",              s, credits=4)
    ee5_pwe  = sub("Power Electronics",           s, credits=4)
    ee5_ps1  = sub("Power system-1",              s, credits=4)
    ee5_wse  = sub("Wind and solar energy systems",s,credits=4)
    ee5_gescc= sub("GESCC",                       s, credits=4)

    sf(ee5_cs,   NSA);  sf(ee5_mp,   NTK);  sf(ee5_pwe, SDK)
    sf(ee5_ps1,  SNT);  sf(ee5_wse,  JTK)

    # ── EE SEM 8 ─────────────────────────────────────────────
    s = semesters[(EE, 8)]
    ee8_dip = sub("DIP", s, credits=4);  ee8_pqf = sub("PQF", s, credits=4)
    ee8_cn  = sub("CN",  s, credits=4);  ee8_ehv = sub("EHV", s, credits=4)

    sf(ee8_dip, NSA);  sf(ee8_pqf, SNT)
    sf(ee8_cn,  NCR);  sf(ee8_ehv, SDK)

    # =========================================================
    # CLASSROOMS
    # =========================================================
    if not Classroom.objects.exists():
        # Theory rooms 1–14
        for i in range(1, 15):
            Classroom.objects.get_or_create(
                room_number=str(i),
                defaults={"capacity": 60, "is_lab": False}
            )
        # Lab rooms (subset — add all that apply to your institute)
        lab_rooms = [
            ("17",  "CHE lab",                        30),
            ("20",  "Workshop",                       30),
            ("21",  "Physics lab",                    30),
            ("22",  "BEE lab",                        30),
            ("23",  "Analog Electronic Lab",          30),
            ("24",  "Project Lab",                    30),
            ("25",  "Computer Center Lab",            60),
            ("26",  "Manufacturing Process Lab",      30),
            ("27",  "Language Lab",                   60),
            ("28",  "Drawing Lab",                    60),
            ("33",  "Hydraulics Engineering lab",     60),
            ("34",  "Control Systems lab",            60),
            ("35",  "Power Electronics lab",          60),
            ("36",  "Power System lab",               60),
            ("37",  "Heat Transfer lab",              60),
            ("38",  "Fluid Machinery Lab",            60),
            ("39",  "Microprocessor Lab",             60),
            ("41",  "IC Lab",                         60),
        ]
        for room_no, name, cap in lab_rooms:
            Classroom.objects.get_or_create(
                room_number=room_no,
                defaults={"capacity": cap, "is_lab": True}
            )

    # =========================================================
    # TIMESLOTS
    # =========================================================
    if not TimeSlot.objects.exists():
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        time_slots = [
            (time(10, 0), time(11, 0), 1),
            (time(11, 0), time(12, 0), 2),
            (time(12, 0), time(13, 0), 3),
            (time(14, 0), time(15, 0), 4),
            (time(15, 0), time(16, 0), 5),
            (time(16, 0), time(17, 0), 6),
        ]
        for day in days:
            for start, end, order in time_slots:
                TimeSlot.objects.get_or_create(
                    day=day, start_time=start,
                    defaults={"end_time": end, "order": order, "is_break": False}
                )

    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()