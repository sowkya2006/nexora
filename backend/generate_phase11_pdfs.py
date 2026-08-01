import fitz
import os

pdf_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "knowledge_base"))
os.makedirs(pdf_dir, exist_ok=True)

def draw_header_footer(page, title, category, page_num, total_pages):
    # Header banner
    page.draw_rect(fitz.Rect(0, 0, 595, 75), color=(0.01, 0.22, 0.42), fill=(0.01, 0.22, 0.42))
    page.insert_text((30, 32), "NEXORA UNIVERSITY", fontsize=16, color=(1, 1, 1), fontname="hebo")
    page.insert_text((30, 52), "Official Knowledge Base Document · Academic Session 2026–2027", fontsize=9, color=(0.8, 0.9, 1), fontname="helv")
    
    # Category Pill Tag
    page.draw_rect(fitz.Rect(440, 22, 565, 52), color=(0.1, 0.55, 0.85), fill=(0.1, 0.55, 0.85))
    page.insert_text((450, 39), category.upper()[:14], fontsize=8.5, color=(1, 1, 1), fontname="hebo")

    # Document Title Sub-banner
    page.insert_text((30, 95), title[:65], fontsize=13, color=(0.05, 0.15, 0.3), fontname="hebo")
    page.insert_text((30, 112), f"Document Code: NX-2026-{category[:3].upper()} · Issued by Office of Academic Governance", fontsize=8.5, color=(0.4, 0.4, 0.4), fontname="helv")
    page.draw_line(fitz.Point(30, 120), fitz.Point(565, 120), color=(0.8, 0.8, 0.8), width=1)

    # Footer
    page.draw_line(fitz.Point(30, 800), fitz.Point(565, 800), color=(0.8, 0.8, 0.8), width=0.8)
    page.insert_text((30, 815), "Nexora University · Confidential & Official Public Release · UniSphere AI RAG Indexed", fontsize=8, color=(0.5, 0.5, 0.5), fontname="helv")
    page.insert_text((505, 815), f"Page {page_num} of {total_pages}", fontsize=8, color=(0.5, 0.5, 0.5), fontname="helv")

def draw_cover_page(doc, title, subtitle, category, author, total_pages):
    page = doc.new_page(width=595, height=842)
    # Background accents
    page.draw_rect(fitz.Rect(0, 0, 595, 842), color=(0.98, 0.99, 1.0), fill=(0.98, 0.99, 1.0))
    page.draw_rect(fitz.Rect(0, 0, 595, 240), color=(0.01, 0.22, 0.42), fill=(0.01, 0.22, 0.42))
    
    page.insert_text((40, 90), "NEXORA UNIVERSITY", fontsize=28, color=(1, 1, 1), fontname="hebo")
    page.insert_text((40, 120), "OFFICIAL POLICY & INSTITUTIONAL HANDBOOK 2026-2027", fontsize=11, color=(0.7, 0.85, 1), fontname="helv")
    page.draw_line(fitz.Point(40, 140), fitz.Point(300, 140), color=(0.2, 0.6, 0.9), width=3)

    # Center Box
    page.draw_rect(fitz.Rect(40, 290, 555, 520), color=(0.9, 0.93, 0.98), fill=(1, 1, 1))
    page.draw_rect(fitz.Rect(40, 290, 555, 520), color=(0.01, 0.22, 0.42), width=1.5)
    
    page.insert_text((60, 340), title, fontsize=18, color=(0.01, 0.22, 0.42), fontname="hebo")
    page.insert_text((60, 375), subtitle[:70], fontsize=11, color=(0.3, 0.3, 0.3), fontname="helv")
    
    page.insert_text((60, 430), f"Category: {category}", fontsize=10, color=(0.1, 0.55, 0.85), fontname="hebo")
    page.insert_text((60, 450), f"Authority: {author}", fontsize=10, color=(0.4, 0.4, 0.4), fontname="helv")
    page.insert_text((60, 470), "Publication Date: July 2026 · Academic Year 2026-2027", fontsize=10, color=(0.4, 0.4, 0.4), fontname="helv")

    # Bottom Footer
    page.insert_text((40, 780), "Nexora University Governance & Administrative Division", fontsize=10, color=(0.3, 0.3, 0.3), fontname="hebo")
    page.insert_text((40, 798), "Main Campus, Knowledge Corridor, Tech City · Web: www.nexorauniversity.edu", fontsize=9, color=(0.5, 0.5, 0.5), fontname="helv")

def render_sections_to_page(page, sections):
    y_cursor = 140
    for section in sections:
        if section.get("heading"):
            page.insert_text((30, y_cursor), section["heading"], fontsize=11, color=(0.01, 0.22, 0.42), fontname="hebo")
            y_cursor += 16
        
        if section.get("text"):
            words = section["text"].split(" ")
            line = ""
            for w in words:
                if len(line + " " + w) > 82:
                    page.insert_text((30, y_cursor), line, fontsize=9, color=(0.2, 0.2, 0.2), fontname="helv")
                    y_cursor += 13.5
                    line = w
                else:
                    line = (line + " " + w).strip()
            if line:
                page.insert_text((30, y_cursor), line, fontsize=9, color=(0.2, 0.2, 0.2), fontname="helv")
                y_cursor += 15
        
        if section.get("bullets"):
            for bullet in section["bullets"]:
                lines = bullet.split("\n")
                for subline_idx, subline in enumerate(lines):
                    words = subline.split(" ")
                    line = "•  " if subline_idx == 0 else "   "
                    for w in words:
                        if len(line + " " + w) > 80:
                            page.insert_text((40, y_cursor), line, fontsize=8.5, color=(0.25, 0.25, 0.25), fontname="helv")
                            y_cursor += 13
                            line = "   " + w
                        else:
                            line = (line + " " + w).strip()
                    if line:
                        page.insert_text((40, y_cursor), line, fontsize=8.5, color=(0.25, 0.25, 0.25), fontname="helv")
                        y_cursor += 14
            y_cursor += 4

        if section.get("table"):
            table_headers = section["table"]["headers"]
            table_rows = section["table"]["rows"]
            col_widths = section["table"].get("widths", [130, 130, 130, 145])
            
            # Header row
            page.draw_rect(fitz.Rect(30, y_cursor, 565, y_cursor + 18), color=(0.9, 0.93, 0.97), fill=(0.9, 0.93, 0.97))
            x_pos = 35
            for idx, th in enumerate(table_headers):
                page.insert_text((x_pos, y_cursor + 13), th, fontsize=8.5, color=(0.05, 0.15, 0.3), fontname="hebo")
                x_pos += col_widths[idx]
            y_cursor += 20

            # Data rows
            for r_idx, row in enumerate(table_rows):
                bg_col = (0.97, 0.98, 1.0) if r_idx % 2 == 0 else (1, 1, 1)
                page.draw_rect(fitz.Rect(30, y_cursor, 565, y_cursor + 16), color=(0.9, 0.9, 0.9), fill=bg_col)
                x_pos = 35
                for idx, cell in enumerate(row):
                    page.insert_text((x_pos, y_cursor + 12), str(cell)[:30], fontsize=8, color=(0.25, 0.25, 0.25), fontname="helv")
                    x_pos += col_widths[idx]
                y_cursor += 17.5
            y_cursor += 8

def create_multi_page_pdf(filename, title, subtitle, category, author, pages_content_list):
    doc = fitz.open()
    total_pages = len(pages_content_list) + 1 # Include cover page
    
    # 1. Cover Page
    draw_cover_page(doc, title, subtitle, category, author, total_pages)
    
    # 2. Content Pages
    for page_idx, page_sections in enumerate(pages_content_list, start=2):
        page = doc.new_page(width=595, height=842)
        draw_header_footer(page, title, category, page_idx, total_pages)
        render_sections_to_page(page, page_sections)

    filepath = os.path.join(pdf_dir, filename)
    doc.save(filepath)
    doc.close()
    print(f"Generated {filename} ({total_pages} pages)")
    return total_pages

# Helper to generate N realistic content pages for generic documents
def build_generic_expanded_pages(doc_title, category_name, num_content_pages=11):
    pages = []
    # Page 1: Table of Contents & Executive Summary
    pages.append([
        {"heading": "TABLE OF CONTENTS & CHAPTER OVERVIEW", "bullets": [
            "Chapter 1: Institutional Vision, Governance & Executive Summary",
            "Chapter 2: Statutory Provisions, Regulatory Approvals & Legal Scope",
            "Chapter 3: Standard Operating Procedures (SOP) & Administrative Framework",
            "Chapter 4: Detailed Operational Guidelines & Fee Schedules",
            "Chapter 5: Student Responsibilities, Ethics & Code of Compliance",
            "Chapter 6: Emergency Protocols, Grievance Redressal & Helpdesk"
        ]},
        {"heading": "1.1 Executive Summary", "text": f"This official document establishes the governing framework, guidelines, operational procedures, and policies for {doc_title} at Nexora University for the academic session 2026-2027. All enrolled students, faculty members, and administrative staff are required to adhere to the standards outlined herein."},
        {"heading": "1.2 Institutional Mandate", "text": "Nexora University is dedicated to delivering world-class higher education, encouraging interdisciplinary innovation, and nurturing high-impact technological and managerial research."}
    ])

    # Page 2: Regulatory Approvals & Authorities
    pages.append([
        {"heading": "2.1 Statutory Approvals & Accreditations", "text": "Nexora University is recognized by the University Grants Commission (UGC) under Section 2(f) and accredited with Grade A++ status by NAAC. All technical degree courses are approved by AICTE."},
        {"heading": "2.2 Governance Hierarchy", "table": {
            "headers": ["Governance Body", "Head of Authority", "Key Responsibility", "Office Location"],
            "widths": [140, 130, 140, 125],
            "rows": [
                ["Board of Management", "Vice Chancellor", "Strategic Policies & Curricula", "Administrative Block 4th Fl"],
                ["Academic Council", "Dean of Academics", "Course Structure & Credits", "Academic Block A"],
                ["Student Affairs Cell", "Dean Student Welfare", "Campus Discipline & Facilities", "Student Activity Center"],
                ["Finance Committee", "Chief Finance Officer", "Tuition & Mess Fee Management", "Finance Wing Room 102"]
            ]
        }},
        {"heading": "2.3 Scope of Application", "text": "The policies outlined in this manual apply to all full-time undergraduate (B.Tech, BBA, B.Sc), postgraduate (M.Tech, MBA, MCA), and doctoral candidates registered at Nexora Main Campus."}
    ])

    # Pages 3 to num_content_pages - 1: Detailed policies, tables, procedures
    for p in range(3, num_content_pages):
        pages.append([
            {"heading": f"{p}.1 Specific Policy Guidelines — Section {p}", "text": f"Detailed clause {p}.1 regarding {doc_title}. Nexora University enforces strict quality standards and administrative compliance. Students must submit all requisite verification documentation within 15 days of enrollment."},
            {"heading": f"{p}.2 Operational Requirements & Schedule", "table": {
                "headers": ["Activity Parameter", "Compliance Target", "Responsible Department", "Status Metric"],
                "widths": [140, 130, 130, 135],
                "rows": [
                    [f"Phase {p} Verification", "100% On-time submission", "Registrar Office", "Verified"],
                    [f"Semester Review {p}", "Bi-annual Audit", "Internal Quality Cell", "Approved"],
                    [f"Compliance Report {p}", "Monthly Status Check", "Office of Dean", "Published"],
                    [f"Student Feedback {p}", "End of Term Assessment", "Academic Council", "Actioned"]
                ]
            }},
            {"heading": f"{p}.3 Key Student Guidelines & Directives", "bullets": [
                f"Guideline {p}-A: Maintain a minimum of 75% attendance in lectures, practical laboratories, and workshops.",
                f"Guideline {p}-B: Official identity cards must be worn at all times while present on campus premises.",
                f"Guideline {p}-C: Any grievance or official request must be routed through the UniSphere Student Portal.",
                f"Guideline {p}-D: Strictly follow anti-ragging and gender safety protocols established by the Advisory Board."
            ]}
        ])

    # Final Page: FAQ & Contact Information
    pages.append([
        {"heading": f"{num_content_pages + 1}.1 Frequently Asked Questions (FAQ)", "bullets": [
            "Q: How do I submit an official query regarding this document?\nA: Submit a digital ticket via the UniSphere AI portal or visit the Administration Helpdesk.",
            "Q: What happens in case of non-compliance with these guidelines?\nA: Non-compliance attracts administrative warnings, penalty fines, or referral to the Disciplinary Committee.",
            "Q: Can I request an official physical copy of this handbook?\nA: Yes, physical copies are available at the Central Library desk upon request."
        ]},
        {"heading": f"{num_content_pages + 1}.2 Official Contact Directory", "table": {
            "headers": ["Department Office", "Email Contact", "Helpline Number", "Office Hours"],
            "widths": [140, 150, 115, 130],
            "rows": [
                ["Central Helpdesk", "helpdesk@nexorauniversity.edu", "+91-40-2345-6700", "09:00 AM - 05:00 PM"],
                ["Dean of Academics", "academics@nexorauniversity.edu", "+91-40-2345-6711", "10:00 AM - 04:00 PM"],
                ["Student Welfare", "welfare@nexorauniversity.edu", "+91-40-2345-6722", "09:00 AM - 05:00 PM"],
                ["Emergency Line", "security@nexorauniversity.edu", "+91-40-2345-6999", "24 Hours / 7 Days"]
            ]
        }},
        {"heading": f"{num_content_pages + 1}.3 Document Approval & Version Control", "text": "Approved by the Nexora Executive Governance Board. Document Version: 2026.1. Effective Date: 01-July-2026. Valid until 30-June-2027."}
    ])

    return pages

# Specialized content builder for each document type to match PRD & Part 3 specs
def build_admission_handbook_pages():
    pages = []
    # P1: TOC & Overview
    pages.append([
        {"heading": "TABLE OF CONTENTS & CHAPTER OVERVIEW", "bullets": [
            "Chapter 1: Institutional Vision & Executive Summary",
            "Chapter 2: Undergraduate & Postgraduate Admission Workflows",
            "Chapter 3: Statutory Reservation & Quota Policies",
            "Chapter 4: International & NRI Admissions Framework",
            "Chapter 5: Transfer Admissions & Lateral Entry Guidelines",
            "Chapter 6: Mandatory Verification Documents",
            "Chapter 7: Fee Refund Rules & Seat Cancellation SOP",
            "Chapter 8: Frequently Asked Questions (FAQ) & Admission Helpdesk"
        ]},
        {"heading": "1.1 Executive Summary", "text": "Nexora University offers comprehensive degree programs across engineering, computer applications, management, and basic sciences. Admissions are governed by transparent merit-based criteria and strict regulatory guidelines."},
        {"heading": "1.2 Institutional Governance", "text": "All admissions are processed centrally through the Directorate of Admissions in coordination with the Academic Council and state regulatory bodies."}
    ])
    # P2: Workflow & Eligibility
    pages.append([
        {"heading": "2.1 Admission Workflow & Step-by-Step SOP", "bullets": [
            "Step 1: Submission of online application via UniSphere Portal with non-refundable fee of INR 1,200.",
            "Step 2: Generation of NUXSAT Entrance Examination Hall Ticket or submission of national scores (JEE Main / GATE / CAT).",
            "Step 3: Publication of Merit Ranks and Category Rank Lists.",
            "Step 4: Centralized Online Counseling and Seat Allotment based on candidate preference and score.",
            "Step 5: Physical Document Verification and Provisional Fee Deposit."
        ]},
        {"heading": "2.2 Eligibility Criteria Matrix", "table": {
            "headers": ["Program Level", "Qualifying Degree", "Minimum Marks", "Accepted Entrance Exams"],
            "widths": [110, 150, 120, 165],
            "rows": [
                ["B.Tech (All Branches)", "10+2 with PCM", "60% Aggregate", "NUXSAT / JEE Main"],
                ["BBA / B.Com", "10+2 (Any Stream)", "55% Aggregate", "NUXSAT / Merit Based"],
                ["M.Tech (All Branches)", "B.E. / B.Tech in relevant field", "6.5 CGPA / 60%", "GATE / NUXSAT-PG"],
                ["MBA (Dual Spec)", "Bachelor Degree (3 or 4 yrs)", "50% Aggregate", "CAT / MAT / NUXSAT-MBA"]
            ]
        }}
    ])
    # P3: Reservation & Quota Policy
    pages.append([
        {"heading": "3.1 Reservation & Category Quota Distribution", "text": "Nexora University complies with government directives regarding statutory reservations. Category certificates issued by competent authorities must be submitted at the time of counseling."},
        {"heading": "3.2 Category Breakdown", "table": {
            "headers": ["Category Code", "Category Description", "Percentage Reservation", "Verification Document"],
            "widths": [110, 160, 130, 145],
            "rows": [
                ["GEN", "General / Unreserved", "40.5%", "Identity Proof"],
                ["OBC-NCL", "Other Backward Classes (Non-Creamy)", "27.0%", "Valid Caste & Income Certificate"],
                ["SC", "Scheduled Castes", "15.0%", "Sub-divisional Caste Certificate"],
                ["ST", "Scheduled Tribes", "7.5%", "District Tribal Officer Certificate"],
                ["EWS", "Economically Weaker Section", "10.0%", "Income & Asset Certificate"]
            ]
        }},
        {"heading": "3.3 Persons with Disabilities (PwD) & Sports Quota", "text": "A 5% horizontal reservation is provided across all categories for PwD candidates with minimum 40% disability certified by a Medical Board."}
    ])
    # P4: International & NRI Admissions
    pages.append([
        {"heading": "4.1 International & Foreign Nationals Admission SOP", "text": "Foreign nationals, PIO, OCI cardholders, and Non-Resident Indians (NRI) can apply under the International Student Quota. 15% supernumerary seats are allocated for international candidates."},
        {"heading": "4.2 International Admission Eligibility & Language Proficiency", "bullets": [
            "Equivalent secondary / senior secondary school certification recognized by the Association of Indian Universities (AIU).",
            "Demonstrated English language proficiency via TOEFL (Minimum Score: 80) or IELTS (Minimum Band: 6.5) or certificate of English medium instruction.",
            "Valid passport with at least 18 months of remaining validity prior to student visa application."
        ]},
        {"heading": "4.3 NRI Sponsored Quota", "text": "NRI sponsored candidates must produce a notarized affidavit from the sponsor guaranteeing financial support for tuition and living expenses during the entire program duration."}
    ])
    # P5: Transfer Admissions & Lateral Entry
    pages.append([
        {"heading": "5.1 Lateral Entry to 2nd Year (3rd Semester) B.Tech", "text": "Candidates holding a 3-year Diploma in Engineering/Technology with at least 60% aggregate marks are eligible for lateral entry into 2nd year B.Tech courses."},
        {"heading": "5.2 Migration & Credit Transfer Policy", "text": "Students seeking inter-university transfer must have completed 1st year with clear credits. Credit equivalence is assessed by the Academic Equivalence Committee."},
        {"heading": "5.3 Credit Mapping Matrix", "table": {
            "headers": ["Discipline", "Diploma Stream", "Eligible B.Tech Branch", "Max Credit Waiver"],
            "widths": [120, 140, 150, 135],
            "rows": [
                ["Computer Engg", "Diploma in CS / IT", "B.Tech CSE / AI", "42 Credits"],
                ["Electrical Engg", "Diploma in EE / EEE", "B.Tech EEE / ECE", "40 Credits"],
                ["Mechanical Engg", "Diploma in Mechanical", "B.Tech Mechanical", "44 Credits"],
                ["Civil Engg", "Diploma in Civil", "B.Tech Civil", "40 Credits"]
            ]
        }}
    ])
    # P6: Required Documents Checklists
    pages.append([
        {"heading": "6.1 Mandatory Verification Documents Checklist", "bullets": [
            "10th Standard (SSLC) Marksheet and Passing Certificate (Proof of Age).",
            "12th Standard (HSC) Marksheet and Passing Certificate.",
            "Qualifying Examination Admit Card and Score Card (NUXSAT / JEE Main / GATE / CAT).",
            "Transfer Certificate (TC) and Migration Certificate from previous institution.",
            "Category / Reservation Certificate (OBC-NCL / SC / ST / EWS / PwD) if applicable.",
            "Recent Passport Size Photographs (8 copies with white background).",
            "Aadhaar Card or Passport (Original & 3 self-attested photocopies).",
            "Anti-Ragging Undertaking by Student and Parent (Notarized Stamp Paper)."
        ]},
        {"heading": "6.2 Document Verification Process", "text": "Original documents will be inspected by the Verification Committee. Copies will be retained in the university student archive."}
    ])
    # P7: Refund Policy & Seat Cancellation
    pages.append([
        {"heading": "7.1 Fee Refund Schedule & UGC Compliance Rules", "text": "Nexora University strictly enforces the UGC Refund Policy guidelines for seat withdrawal and cancellation requested prior to or after formal program commencement."},
        {"heading": "7.2 Withdrawal Timeline & Refund Percentage Table", "table": {
            "headers": ["Notice Period", "Refund Percentage", "Deduction Charge", "Processing Days"],
            "widths": [160, 130, 125, 130],
            "rows": [
                ["15 days before last date", "100% Refund", "INR 1,000 Handling Fee", "7 Working Days"],
                ["Less than 15 days before last date", "90% Refund", "10% Tuition Fee", "10 Working Days"],
                ["15 days or less after last date", "80% Refund", "20% Tuition Fee", "15 Working Days"],
                ["30 days or less after last date", "50% Refund", "50% Tuition Fee", "15 Working Days"],
                ["More than 30 days after last date", "0% Refund", "100% Retention", "N/A"]
            ]
        }},
        {"heading": "7.3 Cancellation Procedure", "text": "Cancellation requests must be submitted online through the UniSphere Student Portal followed by submission of the physical refund form."}
    ])
    # P8-10: Detailed Regulations & SOPs
    for p in range(8, 11):
        pages.append([
            {"heading": f"{p}.1 Special Admission Guidelines — Section {p}", "text": f"Clause {p}.1: Additional administrative protocols governing special seats, scholarships, and fee waivers for high-performing candidates in entrance exams."},
            {"heading": f"{p}.2 Counseling Session Regulations", "table": {
                "headers": ["Counseling Round", "Target Rank Range", "Seat Allocation Date", "Reporting Deadline"],
                "widths": [140, 140, 130, 135],
                "rows": [
                    [f"Round {p-7} Counseling", f"Rank 1 to {p*1500}", "August 5, 2026", "August 10, 2026"],
                    [f"Round {p-6} Counseling", f"Rank {p*1500+1} to {p*3000}", "August 12, 2026", "August 17, 2026"],
                    ["Spot Allotment", "Open Merit Ranks", "August 22, 2026", "August 25, 2026"]
                ]
            }},
            {"heading": f"{p}.3 Candidate Compliance Terms", "bullets": [
                f"Term {p}-A: Submission of fraudulent documents results in immediate cancellation of seat and legal action.",
                f"Term {p}-B: Fee payment must be completed within 48 hours of seat allotment.",
                f"Term {p}-C: Students must report to campus for orientation on the date specified in the admission letter."
            ]}
        ])
    # P11: FAQ & Helpdesk Contacts
    pages.append([
        {"heading": "11.1 Frequently Asked Questions (FAQ)", "bullets": [
            "Q: Can I apply for multiple programs in a single application form?\nA: Yes, candidates can select up to 3 preferences in a single application.",
            "Q: What is NUXSAT and is it compulsory?\nA: NUXSAT is Nexora University's entrance exam. Candidates with JEE Main/GATE/CAT valid scores are exempt.",
            "Q: How is the fee refund processed?\nA: Refunds are directly credited to the bank account specified during cancellation application."
        ]},
        {"heading": "11.2 Admission Helpdesk Directory", "table": {
            "headers": ["Office / Cell", "Email Address", "Phone Line", "Location"],
            "widths": [140, 160, 115, 130],
            "rows": [
                ["Directorate of Admissions", "admissions@nexorauniversity.edu", "+91-40-2345-6701", "Admin Block Ground Fl"],
                ["International Students Office", "iso@nexorauniversity.edu", "+91-40-2345-6702", "Admin Block 2nd Fl"],
                ["Verification Cell", "verify@nexorauniversity.edu", "+91-40-2345-6703", "Counseling Hall B"],
                ["Toll Free Helpline", "info@nexorauniversity.edu", "1800-123-NEXORA", "Central Desk"]
            ]
        }},
        {"heading": "11.3 Approval & Version Information", "text": "Issued by Directorate of Admissions, Nexora University. Document Code: NX-2026-ADM-HB. Version 2026.1."}
    ])
    return pages

def build_hostel_handbook_pages():
    pages = []
    # P1: Overview & TOC
    pages.append([
        {"heading": "TABLE OF CONTENTS & CHAPTER OVERVIEW", "bullets": [
            "Chapter 1: Hostel Administration, Code of Conduct & Living Standards",
            "Chapter 2: Allotment Policy, Room Types & Fee Structure",
            "Chapter 3: Mess Timings, Menu Specifications & Hygiene Rules",
            "Chapter 4: Laundry, Housekeeping & Infrastructure Facilities",
            "Chapter 5: Campus Security, Gate Pass SOP & Visitor Policy",
            "Chapter 6: Emergency Contacts, Medical Aid & Health Center Protocols",
            "Chapter 7: Fine Structure, Penalty Matrix & Disciplinary SOP",
            "Chapter 8: Complaint Resolution Portal & Grievance Redressal"
        ]},
        {"heading": "1.1 Executive Summary", "text": "Nexora University provides safe, modern, and comfortable residential accommodation for male and female students. Residence life is structured to foster community, academic discipline, and personal growth."},
        {"heading": "1.2 Governance Structure", "text": "Hostels are governed by the Chief Hostel Warden in coordination with Block Wardens, Resident Tutors, and Student Hostel Committees."}
    ])
    # P2: Rules & Conduct
    pages.append([
        {"heading": "2.1 Code of Conduct & Living Rules", "bullets": [
            "Strict adherence to quiet hours between 10:00 PM and 6:00 AM daily.",
            "Consuming or possessing alcohol, narcotics, tobacco, or contraband is strictly illegal and results in expulsion.",
            "Electric appliances exceeding 500W (heaters, irons, induction cookers) are strictly prohibited inside rooms.",
            "Students are responsible for the safety of personal belongings. Room doors must be kept locked."
        ]},
        {"heading": "2.2 Room Allocation Matrix & Fee Structure", "table": {
            "headers": ["Accommodation Type", "Occupancy", "Annual Room Fee", "Mess Charges (Annual)"],
            "widths": [140, 110, 140, 155],
            "rows": [
                ["Block A & B (AC)", "Double Sharing", "INR 95,000", "INR 45,000"],
                ["Block C & D (Non-AC)", "Double Sharing", "INR 70,000", "INR 45,000"],
                ["Block E (Non-AC)", "Triple Sharing", "INR 55,000", "INR 45,000"],
                ["Single Suite (PG/Ph.D)", "Single Occupancy", "INR 1,20,000", "INR 45,000"]
            ]
        }}
    ])
    # P3: Mess & Dining
    pages.append([
        {"heading": "3.1 Mess Operations & Meal Timings SOP", "text": "The university operates modern central dining halls serving nutritious vegetarian and non-vegetarian meals prepared in hygienic kitchens."},
        {"heading": "3.2 Daily Mess Timings Schedule", "table": {
            "headers": ["Meal Session", "Weekdays Timing", "Weekends / Holidays", "Special Menu Item"],
            "widths": [120, 140, 145, 140],
            "rows": [
                ["Breakfast", "07:30 AM - 09:00 AM", "08:00 AM - 09:30 AM", "South / North Indian Dishes"],
                ["Lunch", "12:30 PM - 02:00 PM", "12:30 PM - 02:30 PM", "Full Meals + Salad & Dessert"],
                ["Evening Snacks", "05:00 PM - 06:00 PM", "05:00 PM - 06:15 PM", "Tea / Coffee & Snacks"],
                ["Dinner", "07:30 PM - 09:00 PM", "07:30 PM - 09:30 PM", "Rotis, Curry & Special Dish"]
            ]
        }},
        {"heading": "3.3 Dining Hall Rules", "text": "Food must be consumed within the dining area. Taking mess utensils or food to hostel rooms is strictly forbidden except during approved illness."}
    ])
    # P4: Laundry & Housekeeping
    pages.append([
        {"heading": "4.1 Laundry & Linen Service Guidelines", "text": "Automated laundry services are available for all residents. Each student is allowed up to 30 clothes per month as part of the laundry quota."},
        {"heading": "4.2 Laundry Pickup Schedule", "table": {
            "headers": ["Hostel Block", "Collection Day", "Delivery Day", "Counter Location"],
            "widths": [130, 135, 135, 145],
            "rows": [
                ["Boys Block A & B", "Monday & Thursday", "Wednesday & Saturday", "Block A Ground Fl Laundry"],
                ["Boys Block C & D", "Tuesday & Friday", "Thursday & Sunday", "Block C Ground Fl Laundry"],
                ["Girls Block Girls-1", "Monday & Thursday", "Wednesday & Saturday", "Girls Hostel Annex 1"],
                ["Girls Block Girls-2", "Tuesday & Friday", "Thursday & Sunday", "Girls Hostel Annex 2"]
            ]
        }},
        {"heading": "4.3 Housekeeping SOP", "text": "Rooms are cleaned twice weekly by authorized housekeeping staff. Common areas and washrooms are disinfected daily."}
    ])
    # P5: Security, Gate Pass & Visitors
    pages.append([
        {"heading": "5.1 Security & Curfew Timings", "text": "Curfew for all resident students is strictly 09:30 PM. Attendance is recorded via biometric scanners between 09:30 PM and 10:00 PM daily."},
        {"heading": "5.2 Outstation Leave & Night Gate Pass SOP", "bullets": [
            "Outstation leave applications must be submitted via UniSphere Portal at least 24 hours in advance.",
            "Automated SMS approval is triggered to parents. Gate pass is activated only after parental approval.",
            "Local day passes must be registered at the warden desk before exiting campus."
        ]},
        {"heading": "5.3 Visitor & Guest Policy", "table": {
            "headers": ["Visitor Category", "Allowed Area", "Permitted Timings", "Max Duration"],
            "widths": [140, 140, 140, 105],
            "rows": [
                ["Parents / Guardian", "Central Visitor Lounge", "04:00 PM - 07:00 PM", "2 Hours"],
                ["Local Relatives", "Visitor Reception Desk", "04:00 PM - 06:30 PM", "1 Hour"],
                ["Day Scholar Students", "Hostel Common Area", "04:30 PM - 06:30 PM", "1 Hour"],
                ["Non-Registered Guests", "Not Allowed", "N/A", "N/A"]
            ]
        }}
    ])
    # P6: Emergency Contacts & Health Services
    pages.append([
        {"heading": "6.1 Campus Health Center & Emergency Protocols", "text": "The campus health center operates 24/7 with resident medical officers, nurses, and an equipped emergency ambulance."},
        {"heading": "6.2 Emergency Phone Directory", "table": {
            "headers": ["Service / Office", "Contact Person", "Phone Helpline", "Location"],
            "widths": [140, 140, 130, 135],
            "rows": [
                ["Hostel Ambulance Line", "Emergency Driver", "+91-40-2345-6991", "Main Gate Station"],
                ["Campus Health Center", "Dr. S. Mehta (RMO)", "+91-40-2345-6992", "Health Center Block"],
                ["Chief Warden Desk", "Prof. V. Sharma", "+91-40-2345-6750", "Central Hostel Office"],
                ["Girls Hostel Warden", "Dr. K. Anitha", "+91-40-2345-6755", "Girls Block Office"]
            ]
        }},
        {"heading": "6.3 Medical Leave Approval SOP", "text": "Medical certificates for class attendance exemption must be counter-signed by the University Resident Medical Officer within 48 hours."}
    ])
    # P7: Fine Structure & Penalty Matrix
    pages.append([
        {"heading": "7.1 Fine Structure & Disciplinary Penalty Matrix", "text": "Violations of hostel regulations attract monetary fines and administrative actions as prescribed by the Warden Advisory Committee."},
        {"heading": "7.2 Infraction & Penalty Table", "table": {
            "headers": ["Violation Infraction", "1st Offense Fine", "2nd Offense Action", "Repeat Offense Action"],
            "widths": [160, 115, 135, 135],
            "rows": [
                ["Late Entry past 09:30 PM", "INR 500 Fine", "INR 1,000 + Parent Call", "Referral to Disciplinary Board"],
                ["Using Heavy Appliances", "INR 1,000 + Seizure", "INR 2,500 Fine", "Room Cancellation"],
                ["Substance / Alcohol Usage", "INR 5,000 Fine", "Suspension from Hostel", "Expulsion from University"],
                ["Unapproved Guest in Room", "INR 2,000 Fine", "INR 5,000 Fine", "Hostel Membership Revoked"]
            ]
        }}
    ])
    # P8-10: Facility Management & SOPs
    for p in range(8, 11):
        pages.append([
            {"heading": f"{p}.1 Operational Regulations — Section {p}", "text": f"Clause {p}.1: Maintenance guidelines for common rooms, sports facilities, and study halls inside residential blocks."},
            {"heading": f"{p}.2 Maintenance Request Process", "table": {
                "headers": ["Service Required", "Resolution SLA", "Responsible Contractor", "Helpdesk Code"],
                "widths": [145, 135, 150, 115],
                "rows": [
                    ["Electrical Repair", "24 Hours", "Campus Electrical Wing", f"MAINT-E{p}"],
                    ["Plumbing Issue", "12 Hours", "Campus Plumbing Wing", f"MAINT-P{p}"],
                    ["Wi-Fi Network Issue", "6 Hours", "IT Infrastructure Team", f"NET-W{p}"]
                ]
            }},
            {"heading": f"{p}.3 Resident Responsibilities", "bullets": [
                f"Responsibility {p}-A: Switch off lights and fans when leaving the room.",
                f"Responsibility {p}-B: Report any plumbing leakages or structural damage immediately.",
                f"Responsibility {p}-C: Keep personal study spaces clean and tidy."
            ]}
        ])
    # P11: Complaint Portal & FAQs
    pages.append([
        {"heading": "11.1 Frequently Asked Questions (FAQ)", "bullets": [
            "Q: Can I change my room after allotment?\nA: Room swap requests are considered only at the end of the semester upon Warden approval.",
            "Q: Are guests allowed to stay overnight?\nA: No overnight guests are permitted inside student rooms under any circumstances.",
            "Q: What is the procedure for mess fee rebate?\nA: Mess rebates are applicable for approved leave of 5 continuous days or more."
        ]},
        {"heading": "11.2 Administration Directory", "table": {
            "headers": ["Office Designation", "Email Address", "Phone Extension", "Office Location"],
            "widths": [150, 160, 115, 120],
            "rows": [
                ["Chief Hostel Warden", "chiefwarden@nexorauniversity.edu", "Ext 6750", "Hostel Complex"],
                ["Boys Block Warden", "boyswarden@nexorauniversity.edu", "Ext 6752", "Block A Ground Fl"],
                ["Girls Block Warden", "girlswarden@nexorauniversity.edu", "Ext 6755", "Girls Block 1"],
                ["Hostel Finance Desk", "hostelfinance@nexorauniversity.edu", "Ext 6760", "Admin Room 104"]
            ]
        }},
        {"heading": "11.3 Version Information", "text": "Issued by Chief Hostel Warden Office, Nexora University. Document Code: NX-2026-HST-HB. Version 2026.1."}
    ])
    return pages

def build_course_catalog_pages():
    pages = []
    # P1: Overview & TOC
    pages.append([
        {"heading": "TABLE OF CONTENTS & CURRICULUM OVERVIEW", "bullets": [
            "Chapter 1: Institutional Academic Mission & Choice Based Credit System (CBCS)",
            "Chapter 2: School of Computer Science & Engineering (B.Tech & M.Tech)",
            "Chapter 3: School of Electronics & Electrical Engineering (B.Tech ECE & EEE)",
            "Chapter 4: School of Mechanical Engineering & Robotics",
            "Chapter 5: School of Business Administration (BBA & MBA Curriculum)",
            "Chapter 6: School of Basic Sciences & Humanities (B.Sc & M.Sc)",
            "Chapter 7: Interdisciplinary Open Electives & Industry Certifications",
            "Chapter 8: Laboratory Specifications, Project Evaluation & Credits"
        ]},
        {"heading": "1.1 Executive Summary", "text": "The Nexora Academic Course Catalog presents the complete curriculum, semester-wise credit distribution, elective options, and laboratory specifications for all degree programs offered in 2026-2027."},
        {"heading": "1.2 CBCS Framework", "text": "All programs adopt the Choice Based Credit System (CBCS) aligned with UGC guidelines, allowing students flexibility in choosing electives and interdisciplinary minors."}
    ])
    # P2: CSE Curriculum
    pages.append([
        {"heading": "2.1 School of Computer Science & Engineering Curriculum", "text": "The CSE curriculum combines strong theoretical computer science foundations with state-of-the-art specialization courses in AI, Machine Learning, Cybersecurity, and Cloud Architecture."},
        {"heading": "2.2 B.Tech CSE Semester-Wise Credit Matrix", "table": {
            "headers": ["Semester", "Core Courses Count", "Elective Count", "Lab Courses", "Total Credits"],
            "widths": [110, 130, 110, 110, 105],
            "rows": [
                ["Semester I", "5 Courses", "0 Electives", "3 Labs", "22 Credits"],
                ["Semester II", "5 Courses", "0 Electives", "3 Labs", "22 Credits"],
                ["Semester III", "4 Courses", "1 Elective", "3 Labs", "23 Credits"],
                ["Semester IV", "4 Courses", "1 Elective", "3 Labs", "23 Credits"],
                ["Semester V", "3 Courses", "2 Electives", "2 Labs", "21 Credits"],
                ["Semester VI", "3 Courses", "2 Electives", "2 Labs + Mini Proj", "22 Credits"],
                ["Semester VII", "2 Courses", "3 Electives", "Major Project Ph 1", "20 Credits"],
                ["Semester VIII", "0 Courses", "2 Electives", "Major Project Ph 2", "17 Credits"]
            ]
        }},
        {"heading": "2.3 Core CSE Subjects List", "bullets": [
            "Data Structures & Algorithms (CS-201) — 4 Credits",
            "Computer Organization & Architecture (CS-202) — 3 Credits",
            "Database Management Systems (CS-301) — 4 Credits",
            "Operating Systems & Systems Programming (CS-302) — 4 Credits",
            "Artificial Intelligence & Machine Learning (CS-401) — 4 Credits"
        ]}
    ])
    # P3: ECE & EEE Curriculum
    pages.append([
        {"heading": "3.1 School of Electronics & Electrical Engineering Curriculum", "text": "Focused on signal processing, VLSI design, embedded microcontrollers, smart electrical grids, and renewable energy systems."},
        {"heading": "3.2 B.Tech ECE & EEE Credit Structure", "table": {
            "headers": ["Degree Track", "Basic Sciences", "Engineering Core", "Specialization", "Total Degree Credits"],
            "widths": [125, 125, 125, 125, 135],
            "rows": [
                ["B.Tech ECE", "24 Credits", "68 Credits", "32 Credits", "170 Credits"],
                ["B.Tech EEE", "24 Credits", "70 Credits", "30 Credits", "170 Credits"],
                ["M.Tech VLSI", "0 Credits", "36 Credits", "24 Credits", "80 Credits"],
                ["M.Tech Power Systems", "0 Credits", "36 Credits", "24 Credits", "80 Credits"]
            ]
        }}
    ])
    # P4: Mechanical & Robotics
    pages.append([
        {"heading": "4.1 Department of Mechanical Engineering & Robotics", "text": "Integrates traditional thermodynamics and kinematics with modern CAD/CAM, additive manufacturing, industrial automation, and robotics."},
        {"heading": "4.2 Key Specialization Tracks", "bullets": [
            "Track A: Robotics & Autonomous Systems (Sensors, Actuators, ROS).",
            "Track B: Computer Aided Design & Manufacturing (CATIA, ANSYS, CNC Programming).",
            "Track C: Thermal & Renewable Energy Systems (Solar, Wind, Computational Fluid Dynamics)."
        ]}
    ])
    # P5: Business Administration (BBA/MBA)
    pages.append([
        {"heading": "5.1 School of Business Administration Curriculum", "text": "Prepares future corporate leaders through case-study pedagogy, industry internships, business analytics, and entrepreneurial incubation projects."},
        {"heading": "5.2 MBA Course Structure", "table": {
            "headers": ["Specialization", "Major Electives", "Minor Electives", "Industry Internship", "Credits"],
            "widths": [140, 130, 120, 140, 105],
            "rows": [
                ["Business Analytics", "6 Courses", "3 Courses", "8 Weeks Full-Time", "96 Credits"],
                ["Finance & Fintech", "6 Courses", "3 Courses", "8 Weeks Full-Time", "96 Credits"],
                ["Marketing & Digital Strategy", "6 Courses", "3 Courses", "8 Weeks Full-Time", "96 Credits"],
                ["Human Resource Mgmt", "6 Courses", "3 Courses", "8 Weeks Full-Time", "96 Credits"]
            ]
        }}
    ])
    # P6: Basic Sciences & Humanities
    pages.append([
        {"heading": "6.1 School of Basic Sciences & Humanities", "text": "Provides foundational science training for engineering students alongside dedicated B.Sc and M.Sc degree programs in Physics, Chemistry, and Mathematics."},
        {"heading": "6.2 Course Modules", "bullets": [
            "Applied Physics & Quantum Mechanics (PH-101) — 4 Credits",
            "Engineering Chemistry & Environmental Science (CH-101) — 4 Credits",
            "Linear Algebra & Multivariable Calculus (MA-101) — 4 Credits",
            "Professional Ethics & English Communication (HU-101) — 3 Credits"
        ]}
    ])
    # P7: Interdisciplinary Electives
    pages.append([
        {"heading": "7.1 Open Electives & Minor Specialization Scheme", "text": "Students can earn a Minor Degree in AI, Fintech, or Robotics by completing 18 additional credits of designated open electives across semesters IV to VII."},
        {"heading": "7.2 Popular Open Electives List", "table": {
            "headers": ["Course Code", "Course Title", "Offering Department", "Pre-requisite"],
            "widths": [115, 185, 140, 125],
            "rows": [
                ["OE-501", "Introduction to Quantum Computing", "Department of CSE", "Linear Algebra"],
                ["OE-502", "Financial Technology & Blockchain", "School of Business", "None"],
                ["OE-503", "Industrial Internet of Things (IIoT)", "Department of ECE", "Basic Electronics"],
                ["OE-504", "Renewable Energy & Solar Tech", "Department of EEE", "None"]
            ]
        }}
    ])
    # P8-13: Lab Specs & Detailed Modules
    for p in range(8, 14):
        pages.append([
            {"heading": f"{p}.1 Academic Laboratory & Assessment SOP — Section {p}", "text": f"Clause {p}.1: Guidelines for laboratory experiments, continuous internal evaluation (40% weightage), and end-semester practical examinations (60% weightage)."},
            {"heading": f"{p}.2 Laboratory Infrastructure Specifications", "table": {
                "headers": ["Laboratory Name", "Software / Equipment", "Capacity", "Lab Supervisor"],
                "widths": [140, 160, 110, 145],
                "rows": [
                    [f"Advanced Computing Lab {p-7}", "NVIDIA A100 GPUs, PyTorch", "60 Workstations", "Prof. R. Kumar"],
                    [f"VLSI Design Center {p-7}", "Cadence Design Suite", "45 Workstations", "Dr. A. Sen"],
                    [f"Robotics Simulation Lab {p-7}", "KUKA Robotic Arms, ROS2", "30 Students", "Dr. M. Patel"]
                ]
            }},
            {"heading": f"{p}.3 Student Evaluation Standards", "bullets": [
                f"Standard {p}-A: Minimum 85% lab experiment completion is mandatory for exam hall ticket.",
                f"Standard {p}-B: Project code and reports must be uploaded to UniSphere GitHub repository.",
                f"Standard {p}-C: Continuous assessment marks are published bi-weekly on the student portal."
            ]}
        ])
    # P14: FAQ & Contacts
    pages.append([
        {"heading": "14.1 Frequently Asked Questions (FAQ)", "bullets": [
            "Q: Can I drop an elective course after semester registration?\nA: Elective drop/add is permitted within 10 days of semester commencement.",
            "Q: What is the criteria for awarded a Distinction?\nA: CGPA of 8.5 and above without any backlog clears in first attempt.",
            "Q: Where can I find detailed syllabus for individual subjects?\nA: Complete syllabus PDFs are available on the UniSphere Academic Portal."
        ]},
        {"heading": "14.2 Academic Council Directory", "table": {
            "headers": ["Academic Office", "Email Contact", "Extension", "Office Location"],
            "widths": [150, 160, 115, 120],
            "rows": [
                ["Dean of Academics", "dean.academics@nexorauniversity.edu", "Ext 6710", "Academic Block A"],
                ["Controller of Exams", "coe@nexorauniversity.edu", "Ext 6715", "Exam Wing 2nd Fl"],
                ["UG Program Coordinator", "ug.coord@nexorauniversity.edu", "Ext 6720", "Academic Block B"],
                ["PG Program Coordinator", "pg.coord@nexorauniversity.edu", "Ext 6725", "Academic Block B"]
            ]
        }},
        {"heading": "14.3 Approval & Version Information", "text": "Issued by Academic Council, Nexora University. Document Code: NX-2026-CRS-CAT. Version 2026.1."}
    ])
    return pages

def build_placement_brochure_pages():
    pages = []
    # P1: Overview & TOC
    pages.append([
        {"heading": "TABLE OF CONTENTS & CHAPTER OVERVIEW", "bullets": [
            "Chapter 1: Vice Chancellor's Message & Placement Overview 2026",
            "Chapter 2: Key Placement Statistics & Salary Package Highlights",
            "Chapter 3: Sector-Wise Recruiter Directory & Industry Partners",
            "Chapter 4: Summer Internship Program (SIP) & Stipend Metrics",
            "Chapter 5: Training & Career Development Cell (TDC) SOP",
            "Chapter 6: Alumni Success Stories & Global Placements",
            "Chapter 7: Campus Placement Eligibility Rules & Code of Conduct",
            "Chapter 8: Recruiter Registration Portal & Placement Contact Directory"
        ]},
        {"heading": "1.1 Executive Summary", "text": "The Training & Placement Cell at Nexora University connects graduating talent with leading multinational corporations, technology giants, financial institutions, and innovative startups."},
        {"heading": "1.2 Placement Highlights 2025-2026", "text": "Nexora University recorded 94.2% overall placement across engineering and management disciplines with participation from over 220 recruiting partners."}
    ])
    # P2: Placement Stats & Salary Packages
    pages.append([
        {"heading": "2.1 Placement Salary Package Statistics 2025-2026", "text": "Comprehensive report of packages offered across Computer Science, Electronics, Mechanical, and Business Management programs."},
        {"heading": "2.2 Salary Metrics Breakdown Table", "table": {
            "headers": ["Degree Program", "Highest Package (CTC)", "Average Package (CTC)", "Median Package", "Placement %"],
            "widths": [140, 125, 125, 105, 70],
            "rows": [
                ["B.Tech CSE / AI", "INR 48.5 LPA", "INR 14.2 LPA", "INR 12.0 LPA", "98.5%"],
                ["B.Tech ECE / EEE", "INR 32.0 LPA", "INR 10.8 LPA", "INR 9.5 LPA", "94.0%"],
                ["B.Tech Mechanical", "INR 22.0 LPA", "INR 8.5 LPA", "INR 7.8 LPA", "91.2%"],
                ["MBA (Analytics/Fin)", "INR 28.0 LPA", "INR 12.5 LPA", "INR 11.0 LPA", "96.0%"],
                ["M.Tech (All Streams)", "INR 35.0 LPA", "INR 15.0 LPA", "INR 13.5 LPA", "95.5%"]
            ]
        }},
        {"heading": "2.3 Top Offer Highlights", "bullets": [
            "Highest Domestic Package: INR 48.5 LPA offered by Microsoft India.",
            "Highest International Package: USD 115,000 offered by Amazon Web Services USA.",
            "Over 120 students received pre-placement offers (PPOs) during summer internships."
        ]}
    ])
    # P3: Recruiter Directory
    pages.append([
        {"heading": "3.1 Sector-Wise Recruiting Partners Directory", "text": "Leading organizations visiting Nexora University for campus recruitment drives annually."},
        {"heading": "3.2 Corporate Recruiter Matrix", "table": {
            "headers": ["Industry Sector", "Key Recruiting Companies", "Roles Offered", "Selection Process"],
            "widths": [120, 175, 135, 135],
            "rows": [
                ["IT & Software", "Microsoft, Google, Amazon, TCS, Infosys", "SDE, AI Engineer, Cloud Dev", "Coding Test + Technical + HR"],
                ["Core Electronics", "Texas Instruments, Intel, Qualcomm, AMD", "VLSI Designer, Embedded Dev", "Tech Test + Technical Interview"],
                ["Consulting & BFSI", "Deloitte, PwC, Goldman Sachs, JP Morgan", "Business Analyst, Fintech Associate", "Aptitude + Case Study + HR"],
                ["Automotive & Core", "Tata Motors, L&T, Mahindra, Bosch", "Design Engineer, GET Trainee", "Written Test + Tech Interview"]
            ]
        }}
    ])
    # P4: Summer Internship Program
    pages.append([
        {"heading": "4.1 Summer Internship Program (SIP) SOP", "text": "Mandatory 8-12 week industrial internship for pre-final year B.Tech and MBA candidates to gain hands-on corporate experience."},
        {"heading": "4.2 Internship Stipend Breakdown", "table": {
            "headers": ["Stipend Bracket", "Percentage of Students", "Top Intern Employers", "Average Duration"],
            "widths": [130, 135, 170, 130],
            "rows": [
                ["> INR 50,000 / month", "18% Candidates", "Amazon, Microsoft, Adobe", "10 Weeks"],
                ["INR 25,000 - 50,000", "45% Candidates", "Salesforce, Oracle, Bosch", "8 Weeks"],
                ["INR 15,000 - 25,000", "30% Candidates", "Cognizant, Wipro, Startups", "8 Weeks"],
                ["Research Internships", "7% Candidates", "IISc, IITs, Foreign Universities", "12 Weeks"]
            ]
        }}
    ])
    # P5: Career Development Cell SOP
    pages.append([
        {"heading": "5.1 Training & Placement Cell Programs", "bullets": [
            "Technical Skill Building: Competitive Coding bootcamps in Python, C++, Java, and Data Structures.",
            "Aptitude & Reasoning: 100+ hours of quantitative aptitude and logical reasoning training.",
            "Soft Skills & Communication: Mock interviews, GD sessions, and executive resume building.",
            "Domain Certifications: Sponsored certifications in AWS, Azure, and Salesforce."
        ]}
    ])
    # P6: Alumni Success Stories
    pages.append([
        {"heading": "6.1 Global Alumni Network & Success Stories", "text": "Nexora University alumni occupy leadership positions in global tech giants, research institutions, and successful entrepreneurial ventures."},
        {"heading": "6.2 Notable Alumni Profiles", "table": {
            "headers": ["Alumnus Name", "Graduation Year", "Current Designation", "Organization / Location"],
            "widths": [130, 110, 160, 165],
            "rows": [
                ["Mr. Vikram Malhotra", "Class of 2018", "Senior AI Researcher", "Google DeepMind, UK"],
                ["Ms. Ritu Deshmukh", "Class of 2019", "Director of Product", "Salesforce, USA"],
                ["Mr. Arjan Singh", "Class of 2020", "Co-founder & CTO", "TechFlow Unicorn Startup"],
                ["Ms. Ananya Roy", "Class of 2021", "VP Quantitative Finance", "Goldman Sachs, London"]
            ]
        }}
    ])
    # P7: Placement Code of Conduct & Rules
    pages.append([
        {"heading": "7.1 Student Placement Rules & Policy", "bullets": [
            "One Student One Job Policy: Once a candidate secures an offer exceeding INR 8 LPA, they are placed and ineligible for further core drives.",
            "Dream Company Exemption: Candidates placed in tier-2 companies (below 8 LPA) can attempt up to 2 Dream Company drives (above 15 LPA).",
            "Strict Attendance SOP: Absenteeism after registering for a company drive results in immediate debarment from placement season.",
            "Professional Dress Code: Formal business attire is compulsory for all interview rounds."
        ]}
    ])
    # P8-12: Training Details & Drives
    for p in range(8, 13):
        pages.append([
            {"heading": f"{p}.1 Placement Operations SOP — Section {p}", "text": f"Clause {p}.1: Detailed procedures for company registration, pre-placement talks (PPT), online assessment labs, and venue management."},
            {"heading": f"{p}.2 Assessment Infrastructure Matrix", "table": {
                "headers": ["Facility Room", "Seating Capacity", "Terminal Spec", "Usage Purpose"],
                "widths": [140, 110, 150, 165],
                "rows": [
                    [f"Placement Lab {p-7}", "120 Workstations", "Core i7, 16GB RAM, Fiber Net", "Online Coding Tests"],
                    [f"Interview Suite {p-7}", "15 Private Rooms", "Video Conf Equipment", "Technical / HR Interviews"],
                    ["Auditorium", "600 Seats", "Dolby Audio, Dual Projectors", "Pre-Placement Talks"]
                ]
            }},
            {"heading": f"{p}.3 Student Responsibilities", "bullets": [
                f"Rule {p}-A: Keep UniSphere placement profile updated with verified CGPA and backlogs count.",
                f"Rule {p}-B: Produce original marksheets during physical interview verification.",
                f"Rule {p}-C: Submit copy of offer letter to Placement Cell within 24 hours of receipt."
            ]}
        ])
    # P13: FAQ & Contact Directory
    pages.append([
        {"heading": "13.1 Frequently Asked Questions (FAQ)", "bullets": [
            "Q: Can students with active backlogs participate in campus placements?\nA: Eligibility depends on company criteria. Many IT companies allow up to 1 active backlog.",
            "Q: How are internship PPOs converted into full-time offers?\nA: PPOs are validated upon submission of company evaluation feedback to the Placement Cell.",
            "Q: Is there support for higher studies (GATE / GRE / CAT)?\nA: Yes, the T&P Cell conducts dedicated GATE and GRE preparation coaching classes."
        ]},
        {"heading": "13.2 Training & Placement Cell Directory", "table": {
            "headers": ["Designation / Office", "Contact Person", "Email Address", "Phone Helpline"],
            "widths": [140, 135, 165, 125],
            "rows": [
                ["Head - Training & Placement", "Prof. K. R. Sharma", "placement.head@nexorauniversity.edu", "+91-40-2345-6800"],
                ["Deputy Placement Officer", "Mr. S. V. Rao", "placements@nexorauniversity.edu", "+91-40-2345-6801"],
                ["Internship Coordinator", "Ms. Neha Gupta", "internships@nexorauniversity.edu", "+91-40-2345-6802"],
                ["Corporate Relations Desk", "Corporate Cell", "corporate@nexorauniversity.edu", "+91-40-2345-6805"]
            ]
        }},
        {"heading": "13.3 Approval & Version Information", "text": "Issued by Directorate of Training & Placement, Nexora University. Document Code: NX-2026-PLC-BR. Version 2026.1."}
    ])
    return pages

# Generate all 17 PDFs
automated_files_config = [
    ("Admission_Brochure_2026.pdf", "Nexora University Admission Brochure 2026-2027", "Complete Admission Guide, Eligibility & Selection Criteria", "Admissions", "Office of Admissions", build_admission_handbook_pages()),
    ("Admission_Handbook_2026.pdf", "Detailed Admission Rules & Candidate Handbook 2026", "Reservation Quotas, NRI Seats, Counseling SOP & Refunds", "Admissions", "Directorate of Admissions", build_admission_handbook_pages()),
    ("Fee_Structure_2026.pdf", "Official Tuition & Institutional Fee Structure 2026-2027", "Degree Tuition, Lab Fees, Hostel Rent & Refund Rules", "Fees", "Office of Finance", build_generic_expanded_pages("Official Tuition & Institutional Fee Structure 2026", "Fees", 9)),
    ("Hostel_Rules_and_Fees_2026.pdf", "Hostel Regulations, Residence Guidelines & Mess Fee Structure", "Living Regulations, Curfew, Laundry, Mess & Visitor SOP", "Hostel", "Chief Hostel Warden", build_hostel_handbook_pages()),
    ("Academic_Calendar_2026.pdf", "Official Academic Calendar & Examination Timetable 2026", "Semester Dates, Mid-Terms, End-Terms & Holidays", "Academics", "Controller of Examinations", build_generic_expanded_pages("Official Academic Calendar 2026", "Academics", 9)),
    ("Course_Catalog_and_Programs.pdf", "Nexora Academic Course Catalog & Syllabus 2026", "Curriculum, Credits, Electives & Lab Specifications", "Academics", "Academic Council", build_course_catalog_pages()),
    ("Department_Handbook_2026.pdf", "Department Information, Labs & Faculty Profiles 2026", "CSE, ECE, EEE, Mechanical, Biotech & Management Specs", "Departments", "Deans of Schools", build_generic_expanded_pages("Department Information & Faculty Specs 2026", "Departments", 12)),
    ("Examination_Regulations_2026.pdf", "University Examination Rules & Evaluation Policy 2026", "Credit Evaluation, Grading Scale, Backlogs & Revaluation", "Examination", "Examination Cell", build_generic_expanded_pages("University Examination Rules & Policy 2026", "Examination", 12)),
    ("Placement_Brochure_2026.pdf", "Annual Placement & Career Advancement Report 2026", "Recruiter Directory, Salary Packages & Internship SOP", "Placements", "Training & Placement Cell", build_placement_brochure_pages()),
    ("Scholarship_Handbook_2026.pdf", "Institutional Scholarship & Financial Aid Guidelines 2026", "Merit Scholarships, Need-based Assistance & Waivers", "Scholarships", "Scholarship Committee", build_generic_expanded_pages("Institutional Scholarship Handbook 2026", "Scholarships", 10)),
    ("Library_Guide_2026.pdf", "Central Library Guide & Digital Knowledge Base Rules", "Membership, Book Borrowing, E-Journals & Working Hours", "Library", "University Librarian", build_generic_expanded_pages("Central Library Guide 2026", "Library", 9)),
    ("Transport_Handbook_2026.pdf", "Campus Bus Routes, Timings & Transport Pass Rules 2026", "Bus Routes, Fleet Management, Bus Pass & Safety SOP", "Transport", "Transport Manager", build_generic_expanded_pages("Campus Transport Handbook 2026", "Transport", 9)),
    ("Student_Code_of_Conduct_2026.pdf", "Student Code of Ethics, Anti-Ragging & Campus Rules 2026", "Disciplinary Rules, Gender Equality & Campus Ethics", "General", "Disciplinary Committee", build_generic_expanded_pages("Student Code of Conduct 2026", "General", 12)),
    ("Campus_Facilities_Guide_2026.pdf", "Campus Facilities, Sports Infrastructure & Health Services", "Gymnasium, Swimming Pool, Cafeteria & Medical Center", "Campus", "Estate & Facilities Dept", build_generic_expanded_pages("Campus Facilities Guide 2026", "Campus", 10)),
    ("Faculty_Directory_2026.pdf", "Complete University Faculty Directory 2026", "Professor Profiles, Designations, Research & Email Contacts", "General", "Office of Human Resources", build_generic_expanded_pages("Faculty Directory 2026", "General", 11)),
    ("Clubs_and_Student_Activities_2026.pdf", "Student Clubs, Societies & Extracurricular Activities", "Technical Clubs, Cultural Fest, Sports & Leadership SOP", "Events", "Student Activity Council", build_generic_expanded_pages("Clubs and Student Activities 2026", "Events", 10)),
    ("Research_and_Innovation_Handbook_2026.pdf", "Research Grants, Innovation Hub & Patent Guidelines", "Seed Funding, Incubation Center & Patent Support SOP", "Research", "Research & Development Cell", build_generic_expanded_pages("Research and Innovation Handbook 2026", "Research", 11)),
]

print("Starting generation of expanded, highly professional multi-page PDFs (~10-15 pages each)...")
for fname, title, subtitle, cat, auth, content_pages in automated_files_config:
    create_multi_page_pdf(fname, title, subtitle, cat, auth, content_pages)

print("All 17 multi-page PDFs generated successfully in knowledge_base/!")
