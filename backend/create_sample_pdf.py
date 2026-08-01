import os
import fitz  # PyMuPDF

pdf_path = os.path.join("..", "knowledge_base", "Nexora_University_Admission_Handbook.pdf")

doc = fitz.open()

# Page 1: Cover & General Information
page1 = doc.new_page()
p1_text = """
NEXORA UNIVERSITY
OFFICIAL ADMISSION HANDBOOK 2026-2027

Welcome to Nexora University, a premier institution dedicated to academic excellence, innovation, and career success.

1. GENERAL ADMISSION ELIGIBILITY
- Undergraduate Programs (B.Tech, B.Sc, BBA, BCA):
  Applicants must have completed 10+2 or equivalent with a minimum of 60% aggregate marks in relevant subjects.
- Postgraduate Programs (M.Tech, M.Sc, MBA, MCA):
  Applicants must hold a Bachelor's degree in a relevant discipline with a minimum CGPA of 6.5 or 60% aggregate marks.

2. ADMISSION PROCEDURE & APPLICATION FEES
- Online Application Fee: INR 1,200 (Non-refundable).
- Entrance Examination: Candidates must clear the Nexora University Scholastic Aptitude Test (NUXSAT) or valid national entrance scores (JEE Main / GATE / CAT).
- Counseling & Verification: Merit list based counseling will be conducted online followed by document verification.
"""
page1.insert_text((50, 50), p1_text, fontsize=11)

# Page 2: Programs, Fee Structure & Scholarships
page2 = doc.new_page()
p2_text = """
NEXORA UNIVERSITY ADMISSION HANDBOOK 2026-2027

3. TUITION & FEE STRUCTURE (ANNUAL)
- School of Computer Science & Engineering: INR 1,80,000 per year
- School of Electronics & Communication: INR 1,60,000 per year
- School of Business Administration: INR 1,50,000 per year
- School of Humanities & Basic Sciences: INR 90,000 per year

Caution Deposit (Refundable): INR 10,000 payable at admission.

4. SCHOLARSHIP SCHEMES
- Merit Scholarship: 50% tuition waiver for students scoring above 95% in qualifying exams.
- Need-based Aid: Up to 30% fee reduction for families with annual income below INR 3.5 Lakhs.
- Sports & Innovation Merit: Special grants awarded to national level athletes and patent holders.

5. HOSTEL & CAMPUS FACILITIES
- Accommodation Fee: INR 75,000 per year (including mess, Wi-Fi, laundry, and sports complex access).
"""
page2.insert_text((50, 50), p2_text, fontsize=11)

# Page 3: Important Dates & Contact Details
page3 = doc.new_page()
p3_text = """
NEXORA UNIVERSITY ADMISSION HANDBOOK 2026-2027

6. KEY ADMISSION DATES FOR 2026
- Application Portal Opens: January 15, 2026
- Application Submission Deadline: May 30, 2026
- NUXSAT Entrance Exam Date: June 15, 2026
- Merit List Declaration: June 25, 2026
- Semester Commencement: August 1, 2026

7. CONTACT INFORMATION
Admission Helpdesk: admissions@nexorauniversity.edu
Toll Free Number: 1800-123-NEXORA
Campus Address: Nexora University, Innovation District, Hyderabad, Telangana 500032.
"""
page3.insert_text((50, 50), p3_text, fontsize=11)

doc.save(pdf_path)
doc.close()
print(f"Created sample PDF at: {pdf_path}")
