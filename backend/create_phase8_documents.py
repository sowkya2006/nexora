import os
import fitz  # PyMuPDF

kb_dir = os.path.join(os.path.dirname(__file__), "..", "knowledge_base")
os.makedirs(kb_dir, exist_ok=True)

documents_data = [
    {
        "filename": "Admission_Brochure_2026.pdf",
        "title": "Nexora University Admission Brochure 2026",
        "pages": [
            """NEXORA UNIVERSITY ADMISSION BROCHURE 2026-2027
1. OVERVIEW & ADMISSION REQUIREMENTS
Welcome to Nexora University admissions. To be eligible for undergraduate programs (B.Tech, B.Sc, BBA), applicants must have completed 10+2 with a minimum of 60% aggregate marks in PCM/PCB or relevant streams.
For Postgraduate programs (M.Tech, MBA, MCA), a relevant Bachelor's degree with at least 60% aggregate or 6.5 CGPA is mandatory.

2. ADMISSION SELECTION CRITERIA
- Entrance Exam: Clearance of NUXSAT (Nexora University Scholastic Aptitude Test) or valid scores in JEE Main, GATE, or CAT.
- Application Fee: INR 1,200 non-refundable.
- Document Verification: Class 10/12 mark sheets, Transfer Certificate, and Identity Proof required during counseling.""",

            """NEXORA UNIVERSITY ADMISSION BROCHURE 2026-2027
3. HOW TO APPLY
Applications must be submitted online through the Nexora Admissions Portal at https://nexorauniversity.edu/admissions.
Required documents for upload:
- Scanned copy of 10+2 Marksheet
- Passport size photograph
- Entrance scorecard
- Category certificate (if applicable)

Contact Admission Office: admissions@nexorauniversity.edu | Toll Free: 1800-123-NEXORA"""
        ]
    },
    {
        "filename": "Hostel_Rules_and_Fees_2026.pdf",
        "title": "Nexora University Hostel Rules and Fee Structure 2026",
        "pages": [
            """NEXORA UNIVERSITY HOSTEL ACCOMMODATION & FEES 2026
1. HOSTEL FEE STRUCTURE
- Annual Hostel Accommodation Fee: INR 75,000 per academic year.
- This hostel fee includes: Fully furnished room, 4-time meal mess facility, 24/7 High-speed Wi-Fi, laundry service, and access to sports complex facilities.
- Refundable Hostel Security Deposit: INR 5,000 (one-time during check-in).

2. HOSTEL RULES & REGULATIONS
- Curfew timing for all resident students is strictly 9:30 PM.
- Visitors are allowed only in the central visitor lounge between 4:00 PM and 7:00 PM.
- Cooking appliances and heavy electrical equipment are prohibited inside rooms.""",

            """NEXORA UNIVERSITY HOSTEL ACCOMMODATION & FEES 2026
3. MESS & DINING GUIDELINES
- Mess provides vegetarian and non-vegetarian balanced meal options.
- Special dietary requests can be submitted to the Hostel Warden.
- Mess timing: Breakfast (7:30 AM - 9:00 AM), Lunch (12:30 PM - 2:00 PM), Snacks (5:00 PM - 6:00 PM), Dinner (7:30 PM - 9:00 PM)."""
        ]
    },
    {
        "filename": "Course_Catalog_and_Programs.pdf",
        "title": "Nexora University Academic Course Catalog 2026",
        "pages": [
            """NEXORA UNIVERSITY ACADEMIC COURSE CATALOG 2026
1. UNDERGRADUATE DEGREE PROGRAMS OFFERED
Nexora University offers a wide range of undergraduate degree programs:
- School of Computer Science & Engineering: B.Tech in Computer Science and Engineering (CSE), B.Tech in Artificial Intelligence & Data Science, B.Tech in Cybersecurity.
- School of Electronics & Electrical Engineering: B.Tech in Electronics & Communication Engineering (ECE), B.Tech in Electrical & Electronics Engineering (EEE).
- School of Business Administration: Bachelor of Business Administration (BBA), B.Com (Honours).
- School of Humanities & Basic Sciences: B.Sc in Mathematics, B.Sc in Physics, B.A. in Journalism & Mass Communication.

2. POSTGRADUATE DEGREE PROGRAMS OFFERED
- Master of Technology (M.Tech) in Computer Science, M.Tech in VLSI Design.
- Master of Business Administration (MBA) in Finance, Marketing, and Business Analytics.
- Master of Computer Applications (MCA).""",

            """NEXORA UNIVERSITY ACADEMIC COURSE CATALOG 2026
3. ELECTIVE COURSES & SPECIALIZATIONS
Students can choose interdisciplinary electives including Cloud Computing, Quantum Computing, Financial Technology, and Robotics. All programs follow the Choice Based Credit System (CBCS)."""
        ]
    },
    {
        "filename": "Department_Information_and_Faculty.pdf",
        "title": "Nexora University Department Information & Faculty Guide 2026",
        "pages": [
            """NEXORA UNIVERSITY DEPARTMENT INFORMATION 2026
1. DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (CSE)
The Department of CSE at Nexora University is equipped with state-of-the-art AI Research Labs, High-Performance Computing (HPC) Clusters, and Cybersecurity Simulation Labs.
Department Head: Dr. Rajesh Sharma, Ph.D. (IIT Bombay).
Key Research Areas: Machine Learning, Distributed Systems, Computer Vision, and Blockchain Technology.

2. DEPARTMENT OF ELECTRONICS & COMMUNICATION (ECE)
Equipped with VLSI Design Suite, IoT Prototyping Labs, and Embedded Systems Research Center.
Department Head: Dr. Ananya Sen, Ph.D. (IISc Bangalore).""",

            """NEXORA UNIVERSITY DEPARTMENT INFORMATION 2026
3. SCHOOL OF BUSINESS MANAGEMENT
Focuses on case-study driven learning, incubation support, and executive leadership workshops.
Department Head: Prof. Vikramaditya Rao, MBA (IIM Ahmedabad)."""
        ]
    },
    {
        "filename": "Fee_Structure_2026.pdf",
        "title": "Nexora University Annual Fee Structure 2026-2027",
        "pages": [
            """NEXORA UNIVERSITY ANNUAL FEE STRUCTURE 2026-2027
1. SCHOOL-WISE ANNUAL TUITION FEES
- School of Computer Science & Engineering (B.Tech CSE / AI): INR 1,80,000 per year. (CSE fees: INR 1,80,000 per annum).
- School of Electronics & Communication Engineering (B.Tech ECE): INR 1,60,000 per year.
- School of Business Administration (BBA / MBA): INR 1,50,000 per year.
- School of Humanities & Basic Sciences (B.Sc / B.A.): INR 90,000 per year.

2. ADDITIONAL ONE-TIME FEES
- Admission Registration Fee: INR 5,000 (one-time).
- Refundable Caution Deposit: INR 10,000 (refundable upon course completion).
- Examination & Library Fee: INR 8,000 per year.""",

            """NEXORA UNIVERSITY ANNUAL FEE STRUCTURE 2026-2027
3. PAYMENT SCHEDULE & INSTALMENT OPTIONS
Fees can be paid annually or in two equal semester instalments (50% before Semester registration).
Online payment modes accepted: Credit/Debit Cards, NetBanking, UPI, and Demand Draft."""
        ]
    },
    {
        "filename": "Academic_Calendar_2026.pdf",
        "title": "Nexora University Official Academic Calendar 2026-2027",
        "pages": [
            """NEXORA UNIVERSITY OFFICIAL ACADEMIC CALENDAR 2026-2027
1. ODD SEMESTER SCHEDULE (FALL 2026)
- Orientation & Registration: August 1 - August 3, 2026
- Commencement of Classes: August 4, 2026
- Mid-Semester Examinations: October 12 - October 18, 2026
- Annual Cultural Fest (NexFiesta 2026): November 20 - November 22, 2026
- End-Semester Examinations: December 1 - December 15, 2026
- Winter Vacation: December 16, 2026 - January 3, 2027

2. EVEN SEMESTER SCHEDULE (SPRING 2027)
- Commencement of Classes: January 4, 2027
- Mid-Semester Examinations: March 15 - March 20, 2027
- End-Semester Examinations: May 10 - May 25, 2027""",

            """NEXORA UNIVERSITY OFFICIAL ACADEMIC CALENDAR 2026-2027
3. OFFICIAL HOLIDAYS
- Independence Day: August 15, 2026
- Mahatma Gandhi Jayanti: October 2, 2026
- Diwali Break: November 8 - November 12, 2026
- New Year Day: January 1, 2027"""
        ]
    }
]

for doc_info in documents_data:
    file_path = os.path.join(kb_dir, doc_info["filename"])
    doc = fitz.open()
    for page_idx, page_text in enumerate(doc_info["pages"]):
        page = doc.new_page()
        page.insert_text((50, 50), page_text.strip(), fontsize=11)
    doc.save(file_path)
    doc.close()
    print(f"[CREATED] {doc_info['filename']} in knowledge_base (Pages: {len(doc_info['pages'])})")

print("All 6 Phase 8 University PDF documents created successfully.")
