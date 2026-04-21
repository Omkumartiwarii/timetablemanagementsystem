#from tkinter import ALL

from timetable_app.models import *
from datetime import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timetable_project.settings')
django.setup()


def seed_database():
    #duplicate data
    

    # =========================
    # DEPARTMENTS
    # =========================
    ALL, _ = Department.objects.get_or_create(name="ALL")
    CSE, _ = Department.objects.get_or_create(name="Computer Science Eng")
    ECE, _ = Department.objects.get_or_create(name="Electronics Communication Eng")
    ME, _ = Department.objects.get_or_create(name="Mechanical Eng")
    CE, _ = Department.objects.get_or_create(name="CIVIL")
    CECA, _ = Department.objects.get_or_create(name="Civil Engineering Computer Applied")
    EE, _ = Department.objects.get_or_create(name="Electrical Eng")
    APS, _ = Department.objects.get_or_create(name="Applied Science")

    
    departments = [ALL, CSE, ECE, ME, CE, CECA, EE, APS]

    # =========================
    # SEMESTERS
    # =========================
    semesters = {}

    for dept in departments:
        semesters[(dept,2)] = Semester.objects.create(department=dept,semester_number=2)
        semesters[(dept,3)] = Semester.objects.create(department=dept,semester_number=3)
        semesters[(dept,5)] = Semester.objects.create(department=dept,semester_number=5)
        semesters[(dept,8)] = Semester.objects.create(department=dept,semester_number=8)

    # =========================
    # FACULTY
    # =========================
    #-----CSE FAculties-------
    ANP = Faculty.objects.create(name="Prof. ANUPAM KUMAR", department=CSE)
    NCR = Faculty.objects.create(name="Prof. NISCHAY RANJAN", department=CSE)
    ARK = Faculty.objects.create(name="Prof. ARUN KUMAR", department=CSE)
    ASP = Faculty.objects.create(name="Prof. ANSHU PRIYA", department=CSE)
    DPI = Faculty.objects.create(name="Prof. DEEPA KUMARI", department=CSE)
    SDT = Faculty.objects.create(name="DR. SHAHADAT HUSSAIN", department=CSE)

    #-------ECE Faculties---------
    SJK = Faculty.objects.create(name="DR. SANJEEV KUMAR", department=ECE)
    MUK = Faculty.objects.create(name="DR. MUKESH KUMAR", department=ECE)
    ASK = Faculty.objects.create(name="	DR. ANSHU KUMARI", department=ECE)
    RVK = Faculty.objects.create(name="	DR. RAVINDRA KUMAR", department=ECE)
    BMK = Faculty.objects.create(name="Prof. BRIJ MOHAN KUMAR", department=ECE)
    RCV = Faculty.objects.create(name="DR. RUCHI VARMA", department=ECE)
    MKT = Faculty.objects.create(name="Prof. MUNAN KUMAR THAKUR", department=ECE)

    #-------ME Faculties----------
    KVC = Faculty.objects.create(name="Prof. (Dr.) KESHAVENDRA CHOUDHARY", department=ME)
    CDK = Faculty.objects.create(name="DR. CHANDAN KUMAR", department=ME)
    AMK = Faculty.objects.create(name="Prof. AMIT KUMAR", department=ME)
    SRJ = Faculty.objects.create(name="Prof. SERAJ AHMED", department=ME)
    AVK = Faculty.objects.create(name="Prof. AVINASH KUMAR", department=ME)
    VKK = Faculty.objects.create(name="Prof. VIKRAM KUMAR", department=ME)
    VSK = Faculty.objects.create(name="Prof. VINAY SHANKAR KUMAR", department=ME)
    RKS = Faculty.objects.create(name="Prof. RAJU KUMAR SHARMA", department=ME)
    SMK = Faculty.objects.create(name="Prof. SURYAMANI KUMAR", department=ME)

    #-------EE Faculties-------
    SDK = Faculty.objects.create(name="	Prof. SUDHIR KUMAR", department=EE)
    SKJ = Faculty.objects.create(name="	Prof. SAURABH KUMAR JHA", department=EE)
    JTK = Faculty.objects.create(name="Prof. JITENDRA KUMAR", department=EE)
    NSA = Faculty.objects.create(name="Prof. MD. NASIM AKHTER", department=EE)
    NTK = Faculty.objects.create(name="Prof. NISHANT KUMAR", department=EE)
    SNT = Faculty.objects.create(name="	Prof. SANAT", department=EE)

    #-------CIVIl Faculties-------
    DPK = Faculty.objects.create(name="	Prof. DEEPAK KUMAR", department=CE)
    MSA = Faculty.objects.create(name="Prof. MD. SHADAB ALAM", department=CE)
    RVS = Faculty.objects.create(name="Prof. RAVISHANKAR", department=CE)
    PNK = Faculty.objects.create(name="Prof. PANKAJ KUMAR", department=CE)
    RSR = Faculty.objects.create(name="	Prof. RAUSHAN KUMAR RAVI", department=CE)
    FKH = Faculty.objects.create(name="Prof. FAHIM AHMED KHAN", department=CE)
    RKR = Faculty.objects.create(name="Prof. RAKESH KUMAR RAVI", department=CE)
    SSU = Faculty.objects.create(name="	Prof. SAURABH SUMAN", department=CE)

    #-------APS----------
    DSS = Faculty.objects.create(name="DR. DINESH SAH", department=APS)
    ADP = Faculty.objects.create(name="	Prof. ADITYA NARAYAN PANDEY", department=APS)
    AKA = Faculty.objects.create(name="Prof. ANKUR ASHUTOSH", department=APS)
    RKD = Faculty.objects.create(name="DR. RAM KUMAR DAS", department=APS)
    RVR = Faculty.objects.create(name="Prof. RAVI RANJAN", department=APS)
    SSI = Faculty.objects.create(name="Prof. SUMIT SARDESAI", department=APS)
    ABK = Faculty.objects.create(name="	Prof. ABHISHEK KUMAR", department=APS)
    YGP = Faculty.objects.create(name="DR. YOGENDRA KUMAR PODDAR", department=APS)
    MKP = Faculty.objects.create(name="	DR. MUKESH KUMAR PANDEY", department=APS)
    KSM = Faculty.objects.create(name="Prof. KRISHNA MURARI", department=APS)
    MTD = Faculty.objects.create(name="Dr. MATIRAM DAS", department=APS)

    # =========================
    # SUBJECTS (CSE)
    # =========================
     # CSE SEM 2
    CHE=Subject.objects.create(name="Eng Chemistry", semester=semesters[(CSE,2)])
    M2=Subject.objects.create(name="Eng mathematics-2", semester=semesters[(CSE,2)])
    ENG=Subject.objects.create(name="Communicative English", semester=semesters[(CSE,2)])
    PYP=Subject.objects.create(name="Python Programming", semester=semesters[(CSE,2)])
    IWD=Subject.objects.create(name="Introduction to Web design", semester=semesters[(CSE,2)])
    
    # CSE SEM 3
    DSA=Subject.objects.create(name="Data Structures & Algorithms", semester=semesters[(CSE,3)])
    DM=Subject.objects.create(name="Discrete Mathematics", semester=semesters[(CSE,3)])
    DE=Subject.objects.create(name="Digital Logic", semester=semesters[(CSE,3)])
    OOPS=Subject.objects.create(name="OOPS using java", semester=semesters[(CSE,3)])
    OS=Subject.objects.create(name="Operating system", semester=semesters[(CSE,3)])
    UHV=Subject.objects.create(name="Universal Human Values", semester=semesters[(CSE,3)])

    # CSE SEM 5
    ML=Subject.objects.create(name="Machine Learning", semester=semesters[(CSE,5)])
    DBMS=Subject.objects.create(name="DBMS", semester=semesters[(CSE,5)])
    CN=Subject.objects.create(name="Computer Networks", semester=semesters[(CSE,5)])
    PYP=Subject.objects.create(name="Python Programming", semester=semesters[(CSE,5)])
    PPLE=Subject.objects.create(name="Professional Practice, Law & Ethics", semester=semesters[(CSE,5)])
    TOC=Subject.objects.create(name="Theory of Computation PE-I", semester=semesters[(CSE,5)])
  
    #CSE SEM 8
    AND=Subject.objects.create(name="Autonumous Drones", semester=semesters[(CSE,8)])
    RES=Subject.objects.create(name="Renewable Energy Systems", semester=semesters[(CSE,8)])
    AICS=Subject.objects.create(name="AI in Cyber Security", semester=semesters[(CSE,8)])
    DMS=Subject.objects.create(name="Digital Marketing and Search Engine Optimization", semester=semesters[(CSE,8)])

    # =========================
    # SUBJECTS (ECE)
    # =========================
    #ECE SEM 2
    BE=Subject.objects.create(name="Basic Electronics", semester=semesters[(ECE,2)])
    M1=Subject.objects.create(name="Eng mathematics-2", semester=semesters[(ECE,2)])
    ENG=Subject.objects.create(name="Communicative English", semester=semesters[(ECE,2)])
    CHE=Subject.objects.create(name="Eng Chemistry", semester=semesters[(ECE,2)])
    EGD=Subject.objects.create(name="EGD", semester=semesters[(ECE,2)])

    # ECE SEM 3
    SS=Subject.objects.create(name="Signals and Systems", semester=semesters[(ECE,3)])
    EDC=Subject.objects.create(name="Electronic Devices and Circuits", semester=semesters[(ECE,3)])
    IKS=Subject.objects.create(name="Indian Knowledge System", semester=semesters[(ECE,3)])
    NT=Subject.objects.create(name="Network Theory", semester=semesters[(ECE,3)])
    M3=Subject.objects.create(name="Eng Mathematics-3", semester=semesters[(ECE,3)])
    UHV=Subject.objects.create(name="Universal Human Values", semester=semesters[(ECE,3)])

    #ECE SEM 5
    DSP=Subject.objects.create(name="Digital Signal Processing", semester=semesters[(ECE,5)])
    MM=Subject.objects.create(name="Microprocessor & microcontrollers", semester=semesters[(ECE,5)])
    LCS=Subject.objects.create(name="Linear Control System", semester=semesters[(ECE,5)])
    LICA=Subject.objects.create(name="Linear Intergrated Circuita and application", semester=semesters[(ECE,5)])
    CNS=Subject.objects.create(name="Computer Network And Security", semester=semesters[(ECE,5)])
    PTSP=Subject.objects.create(name="Probability Theory", semester=semesters[(ECE,5)])

    #ECE SEM 8
    STLC=Subject.objects.create(name="Satellite Communication", semester=semesters[(ECE,8)])
    IOT=Subject.objects.create(name="Internet of Things", semester=semesters[(ECE,8)])
    MEMS=Subject.objects.create(name="Introduction to MEMS", semester=semesters[(ECE,8)])
    WSN=Subject.objects.create(name="Wireless Sensor Network", semester=semesters[(ECE,8)])

    # =========================
    # SUBJECTS (ME)
    # =========================
    # ME SEM 2
    M2=Subject.objects.create(name="Eng mathematics-2", semester=semesters[(ME,2)])
    PHY=Subject.objects.create(name="Engineering physics", semester=semesters[(ME,2)])
    PPS=Subject.objects.create(name="PPS", semester=semesters[(ME,2)])
    WP=Subject.objects.create(name="Workshop Practice", semester=semesters[(ME,2)])
    EME=Subject.objects.create(name="Elements of mechanical Eng", semester=semesters[(ME,2)])
    
                           
    # ME SEM 3
    TD=Subject.objects.create(name="Thermodynamics", semester=semesters[(ME,3)])
    EMC=Subject.objects.create(name="Engineering Mechanics", semester=semesters[(ME,3)])
    M3=Subject.objects.create(name="Eng mathematics-3", semester=semesters[(ME,3)])
    MSE=Subject.objects.create(name="Material Science & Engineering", semester=semesters[(ME,3)])
    BECE=Subject.objects.create(name="BEE", semester=semesters[(ME,3)])
    UHV=Subject.objects.create(name="Universal Human Values", semester=semesters[(ME,3)])

    # ME SEM 5
    FMC=Subject.objects.create(name="Fuild Machinery", semester=semesters[(ME,5)])
    HT=Subject.objects.create(name="Heat Transfer", semester=semesters[(ME,5)])
    KM=Subject.objects.create(name="Kinetics of Mechanics", semester=semesters[(ME,5)])
    MFP=Subject.objects.create(name="Manufacturing Process", semester=semesters[(ME,5)])

    # ME SEM 8
    POM=Subject.objects.create(name="POM", semester=semesters[(ME,8)])
    ECM=Subject.objects.create(name="ECM", semester=semesters[(ME,8)])
    SFM=Subject.objects.create(name="SFM", semester=semesters[(ME,8)])
    NCM=Subject.objects.create(name="NCM", semester=semesters[(ME,8)])

    # =========================
    # SUBJECTS (CE)
    # =========================
    # CE SEM 2
    M2=Subject.objects.create(name="Eng mathematics-2", semester=semesters[(CE,2)])
    PHY=Subject.objects.create(name="Engineering physics", semester=semesters[(CE,2)])
    PPS=Subject.objects.create(name="PPS", semester=semesters[(CE,2)])
    WP=Subject.objects.create(name="Workshop Practice", semester=semesters[(CE,2)])
    BEE=Subject.objects.create(name="BEE", semester=semesters[(CE,2)])
    SBM=Subject.objects.create(name="Swacha Bharat Mission", semester=semesters[(CE,2)])

    #CE SEM 3
    SM=Subject.objects.create(name="Solid mechanics", semester=semesters[(CE,3)])
    M3=Subject.objects.create(name="Eng mathematics-3", semester=semesters[(CE,3)])
    UHV=Subject.objects.create(name="Universal Human Values", semester=semesters[(CE,3)])
    SG=Subject.objects.create(name="Surveying and Geomatics", semester=semesters[(CE,3)])
    MTE=Subject.objects.create(name="Materials,testing & Evalution", semester=semesters[(CE,3)])
    FLM=Subject.objects.create(name="Fluid Mechanics", semester=semesters[(CE,3)])

    #CE SEM 5
    ADCS=Subject.objects.create(name="ADCS", semester=semesters[(CE,5)])
    EE1=Subject.objects.create(name="EE1", semester=semesters[(CE,5)])
    GE1=Subject.objects.create(name="GE1", semester=semesters[(CE,5)])
    HYE=Subject.objects.create(name="HYE", semester=semesters[(CE,5)])
    HWRE=Subject.objects.create(name="HWRE", semester=semesters[(CE,5)])
    MOM=Subject.objects.create(name="MOM", semester=semesters[(CE,5)])
    TE=Subject.objects.create(name="TE", semester=semesters[(CE,5)])

    #CE SEM 8
    REL=Subject.objects.create(name="REL", semester=semesters[(CE,8)])
    EPI=Subject.objects.create(name="EPI", semester=semesters[(CE,8)])
    CEM=Subject.objects.create(name="CEM", semester=semesters[(CE,8)])
    CNM=Subject.objects.create(name="CNM", semester=semesters[(CE,8)])


    # =========================
    # SUBJECTS (EE)
    # =========================
    #EE SEM 2
    BE=Subject.objects.create(name="Basic Electronics", semester=semesters[(EE,2)])
    M2=Subject.objects.create(name="Eng mathematics-2", semester=semesters[(EE,2)])
    ENG=Subject.objects.create(name="Communicative English", semester=semesters[(EE,2)])
    CHE=Subject.objects.create(name="Eng Chemistry", semester=semesters[(EE,2)])
    EGD=Subject.objects.create(name="EGD", semester=semesters[(EE,2)])

    #EE SEM 3
    ECA=Subject.objects.create(name="ECA", semester=semesters[(EE,3)])
    AE=Subject.objects.create(name="Analog Electronics", semester=semesters[(EE,3)])
    EM1=Subject.objects.create(name="EM-1", semester=semesters[(EE,3)])
    M3=Subject.objects.create(name="Eng mathematics-3", semester=semesters[(EE,3)])
    UHV=Subject.objects.create(name="Universal Human Values", semester=semesters[(EE,3)])
    EMC=Subject.objects.create(name="Engieering Mechanics", semester=semesters[(EE,3)])

    #EE SEM 5
    CS=Subject.objects.create(name="Control System", semester=semesters[(EE,5)])
    MP=Subject.objects.create(name="Microprocessor", semester=semesters[(EE,5)])
    PWE=Subject.objects.create(name="Power Electronics", semester=semesters[(EE,5)])
    PS1=Subject.objects.create(name="Power system-1", semester=semesters[(EE,5)])
    WSE=Subject.objects.create(name="Wind and solar energy systems", semester=semesters[(EE,5)])
    GESCC=Subject.objects.create(name="GESCC", semester=semesters[(EE,5)])
    
    #EE SEM 8
    DIP=Subject.objects.create(name="DIP", semester=semesters[(EE,8)])
    PQF=Subject.objects.create(name="PQF", semester=semesters[(EE,8)])
    CN=Subject.objects.create(name="CN", semester=semesters[(EE,8)])
    EHV=Subject.objects.create(name="EHV", semester=semesters[(EE,8)])

    # =========================
    # SUBJECT-FACULTY MAPPING
    # =========================
    #CE 2 SEM
    SubjectFaculty.objects.create(subject=SBM, faculty=AKA)
    SubjectFaculty.objects.create(subject=PHY, faculty=MKP)
    SubjectFaculty.objects.create(subject=M1, faculty=RKD)
    SubjectFaculty.objects.create(subject=BEE, faculty=JTK)
    SubjectFaculty.objects.create(subject=WP, faculty=VKK)
    SubjectFaculty.objects.create(subject=M2, faculty=RKD)
    SubjectFaculty.objects.create(subject=PPS, faculty=ARK)

    #CE 3 SEM
    SubjectFaculty.objects.create(subject=SM, faculty=RSR)
    SubjectFaculty.objects.create(subject=MTE, faculty=RKR)
    SubjectFaculty.objects.create(subject=SG, faculty=PNK)
    SubjectFaculty.objects.create(subject=SM, faculty=RSR)
    SubjectFaculty.objects.create(subject=IKS, faculty=RSR)
    SubjectFaculty.objects.create(subject=FLM, faculty=SSU)
    SubjectFaculty.objects.create(subject=UHV, faculty=SSI)
    SubjectFaculty.objects.create(subject=M3, faculty=RKD)
    # CE 5 SEM
    SubjectFaculty.objects.create(subject=ADCS, faculty=RVS)
    SubjectFaculty.objects.create(subject=EE1, faculty=RKR)
    SubjectFaculty.objects.create(subject=GE1, faculty=PNK)
    SubjectFaculty.objects.create(subject=HYE, faculty=SSU)
    SubjectFaculty.objects.create(subject=HWRE, faculty=DPK)
    SubjectFaculty.objects.create(subject=MOM, faculty=FKH)
    SubjectFaculty.objects.create(subject=TE, faculty=MSA)
    #CE 8 SEM
    SubjectFaculty.objects.create(subject=REL, faculty=FKH)
    SubjectFaculty.objects.create(subject=EPI, faculty=SSI)
    SubjectFaculty.objects.create(subject=CEM, faculty=RKR)
    SubjectFaculty.objects.create(subject=CNM, faculty=SSI)
    #CSE 2 SEM
    SubjectFaculty.objects.create(subject=CHE, faculty=DSS)
    SubjectFaculty.objects.create(subject=M2, faculty=MTD)
    SubjectFaculty.objects.create(subject=ENG, faculty=RVR)
    SubjectFaculty.objects.create(subject=PYP, faculty=DPI)
    SubjectFaculty.objects.create(subject=IWD, faculty=ASP)
    #CSE 3 SEM
    SubjectFaculty.objects.create(subject=DE, faculty=ASK)
    SubjectFaculty.objects.create(subject=DSA, faculty=ASP)
    SubjectFaculty.objects.create(subject=OOPS, faculty=DPI)
    SubjectFaculty.objects.create(subject=DM, faculty=ARK)
    SubjectFaculty.objects.create(subject=OS, faculty=NCR)
    SubjectFaculty.objects.create(subject=UHV, faculty=SSI)
    SubjectFaculty.objects.create(subject=IKS, faculty=ABK)
    #CSE 5 SEM
    SubjectFaculty.objects.create(subject=DBMS, faculty=ANP)
    SubjectFaculty.objects.create(subject=ML, faculty=SDT)
    SubjectFaculty.objects.create(subject=PYP, faculty=ASP)
    SubjectFaculty.objects.create(subject=CN, faculty=NCR)
    SubjectFaculty.objects.create(subject=PPLE, faculty=SSI)
    SubjectFaculty.objects.create(subject=TOC, faculty=ANP)
    #CSE 8 SEM
    SubjectFaculty.objects.create(subject=AND, faculty=MUK)
    SubjectFaculty.objects.create(subject=RES, faculty=NTK)
    SubjectFaculty.objects.create(subject=AICS, faculty=DPI)
    SubjectFaculty.objects.create(subject=DMS, faculty=SSI)
    #EE 2 SEM
    SubjectFaculty.objects.create(subject=CHE, faculty=YGP)
    SubjectFaculty.objects.create(subject=M1, faculty=ADP)
    SubjectFaculty.objects.create(subject=ENG, faculty=KSM)
    SubjectFaculty.objects.create(subject=BE, faculty=MUK)
    SubjectFaculty.objects.create(subject=EGD, faculty=VSK)
    #EE 3 SEM
    SubjectFaculty.objects.create(subject=ECA, faculty=SNT)
    SubjectFaculty.objects.create(subject=AE, faculty=SDK)
    SubjectFaculty.objects.create(subject=EM1, faculty=VSK)
    SubjectFaculty.objects.create(subject=M3, faculty=MTD)
    SubjectFaculty.objects.create(subject=EMC, faculty=SJK)
    SubjectFaculty.objects.create(subject=UHV, faculty=SSI)
    SubjectFaculty.objects.create(subject=IKS, faculty=ABK)
    # EE 5 SEM
    SubjectFaculty.objects.create(subject=CS, faculty=NSA)
    SubjectFaculty.objects.create(subject=MP, faculty=NTK)
    SubjectFaculty.objects.create(subject=PWE, faculty=SDK)
    SubjectFaculty.objects.create(subject=PS1, faculty=SNT)
    SubjectFaculty.objects.create(subject=WSE, faculty=JTK)
    # EE 8 SEM
    SubjectFaculty.objects.create(subject=EHV, faculty=SDK)
    SubjectFaculty.objects.create(subject=DIP, faculty=NSA)
    SubjectFaculty.objects.create(subject=CN, faculty=NCR)
    SubjectFaculty.objects.create(subject=PQF, faculty=SNT)
    #ME 2 SEM
    SubjectFaculty.objects.create(subject=PHY, faculty=MKP)
    SubjectFaculty.objects.create(subject=M2, faculty=ADP)
    SubjectFaculty.objects.create(subject=PPS, faculty=ARK)
    SubjectFaculty.objects.create(subject=WP, faculty=VKK)
    SubjectFaculty.objects.create(subject=EME, faculty=AVK)
    #ME 3 SEM
    SubjectFaculty.objects.create(subject=EMC, faculty=SRJ)
    SubjectFaculty.objects.create(subject=MSE, faculty=RKS)
    SubjectFaculty.objects.create(subject=M3, faculty=ADP)
    SubjectFaculty.objects.create(subject=TD, faculty=SMK)
    SubjectFaculty.objects.create(subject=BECE, faculty=MKT)
    SubjectFaculty.objects.create(subject=UHV, faculty=SSI)
    SubjectFaculty.objects.create(subject=IKS, faculty=AMK)
    #ME 5 SEM
    SubjectFaculty.objects.create(subject=FMC, faculty=SMK)
    SubjectFaculty.objects.create(subject=HT, faculty=AVK)
    SubjectFaculty.objects.create(subject=KM, faculty=CDK)
    SubjectFaculty.objects.create(subject=MFP, faculty=AMK)
    # ME 8 SEM
    SubjectFaculty.objects.create(subject=POM, faculty=SSI)
    SubjectFaculty.objects.create(subject=ECM, faculty=RKS)
    SubjectFaculty.objects.create(subject=SFM, faculty=SRJ)
    SubjectFaculty.objects.create(subject=NCM, faculty=AMK)
    #ECE 2 SEM
    SubjectFaculty.objects.create(subject=CHE, faculty=YGP)
    SubjectFaculty.objects.create(subject=M2, faculty=MTD)
    SubjectFaculty.objects.create(subject=ENG, faculty=KSM)
    SubjectFaculty.objects.create(subject=BE, faculty=RVK)
    SubjectFaculty.objects.create(subject=EGD, faculty=CDK)
    #ECE 3 SEM
    SubjectFaculty.objects.create(subject=EDC, faculty=RVK)
    SubjectFaculty.objects.create(subject=NT, faculty=MUK)
    SubjectFaculty.objects.create(subject=SS, faculty=MKT)
    SubjectFaculty.objects.create(subject=M3, faculty=ADP)
    SubjectFaculty.objects.create(subject=UHV, faculty=ABK)
    SubjectFaculty.objects.create(subject=IKS, faculty=ABK)
    #ECE 5 SEM
    SubjectFaculty.objects.create(subject=MM, faculty=ASK)
    SubjectFaculty.objects.create(subject=LICA, faculty=SJK)
    SubjectFaculty.objects.create(subject=LCS, faculty=SJK)
    SubjectFaculty.objects.create(subject=DSP, faculty=BMK)
    SubjectFaculty.objects.create(subject=PTSP, faculty=MKT)
    SubjectFaculty.objects.create(subject=CNS, faculty=NCR)
    #ECE 8 SEM
    SubjectFaculty.objects.create(subject=STLC, faculty=BMK)
    SubjectFaculty.objects.create(subject=WSN, faculty=SJK)
    SubjectFaculty.objects.create(subject=MEMS, faculty=RVK)
    SubjectFaculty.objects.create(subject=IOT, faculty=ARK)



    # =========================

    # CLASSROOMS
    # =========================
    if not Classroom.objects.exists():
        for i in range(1,15):
            Classroom.objects.create(room_number=str(i), capacity=60)

    # =========================
    # TIMESLOTS
    # =========================
    if not TimeSlot.objects.exists():
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"]

        time_slots = [
            (time(10, 0), time(11, 0)),
            (time(11, 0), time(12, 0)),
            (time(12, 0), time(13, 0)),
            (time(14, 0), time(15, 0)),
            (time(15, 0), time(16, 0)),
            (time(16, 0), time(17, 0)),
        ]

        for day in days:
            for start, end in time_slots:
                TimeSlot.objects.create(day=day, start_time=start, end_time=end)

    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_database()