"""
Nexora University - Generate All 17 Professional PDFs
Each PDF: 15-30 pages of rich university handbook content
"""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)

KB = Path(__file__).parent.parent / "knowledge_base"
KB.mkdir(exist_ok=True)
W, H = A4

DG = colors.HexColor("#44563E")   # dark green
MG = colors.HexColor("#4A5D45")   # mid green
LG = colors.HexColor("#EAF0E8")   # light green
GD = colors.HexColor("#D9B97A")   # gold
CR = colors.HexColor("#FFFDF8")   # cream
DT = colors.HexColor("#3E3A34")   # dark text
MU = colors.HexColor("#8C857C")   # muted
WH = colors.white
LA = colors.HexColor("#F1F5F9")   # light ash
BD = colors.HexColor("#CBD5E1")   # border

def S(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=10, textColor=DT, leading=15, spaceAfter=4)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

ST = {
    "cu": S("cu", fontName="Helvetica-Bold", fontSize=10, textColor=GD, alignment=TA_CENTER),
    "ct": S("ct", fontName="Helvetica-Bold", fontSize=22, textColor=WH, alignment=TA_CENTER, leading=28, spaceAfter=8),
    "cs": S("cs", fontName="Helvetica", fontSize=12, textColor=colors.HexColor("#D9E3D4"), alignment=TA_CENTER),
    "cv": S("cv", fontName="Helvetica", fontSize=9, textColor=GD, alignment=TA_CENTER),
    "h1": S("h1", fontName="Helvetica-Bold", fontSize=16, textColor=DG, spaceBefore=18, spaceAfter=6, leading=20),
    "h2": S("h2", fontName="Helvetica-Bold", fontSize=13, textColor=DG, spaceBefore=14, spaceAfter=4, leading=17),
    "h3": S("h3", fontName="Helvetica-BoldOblique", fontSize=11, textColor=MG, spaceBefore=10, spaceAfter=3),
    "bd": S("bd", fontName="Helvetica", fontSize=10, textColor=DT, leading=15, spaceAfter=4, alignment=TA_JUSTIFY),
    "bl": S("bl", fontName="Helvetica", fontSize=10, textColor=DT, leading=14, leftIndent=18, spaceAfter=2),
    "nt": S("nt", fontName="Helvetica-Oblique", fontSize=9, textColor=MU, leading=13, leftIndent=12, spaceAfter=3),
    "th": S("th", fontName="Helvetica-Bold", fontSize=9, textColor=WH, alignment=TA_CENTER),
    "td": S("td", fontName="Helvetica", fontSize=9, textColor=DT, alignment=TA_CENTER),
    "tl": S("tl", fontName="Helvetica", fontSize=9, textColor=DT, alignment=TA_LEFT),
    "to": S("to", fontName="Helvetica", fontSize=10, textColor=DT, leading=16, leftIndent=12),
}

def TS(alt=False):
    hdr = GD if alt else DG
    row_bg = [LG, LA] if alt else [CR, LA]
    return TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), hdr),
        ("TEXTCOLOR",     (0,0), (-1,0), DT if alt else WH),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), row_bg),
        ("GRID",          (0,0), (-1,-1), 0.4, BD),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ])

def page_decor(canvas, doc, title=""):
    canvas.saveState()
    canvas.setFillColor(DG)
    canvas.rect(0, H - 1.1*cm, W, 1.1*cm, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(WH)
    canvas.drawString(2*cm, H - 0.72*cm, "NEXORA UNIVERSITY")
    canvas.setFillColor(GD)
    canvas.drawRightString(W - 2*cm, H - 0.72*cm, title[:80])
    canvas.setFillColor(MU)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(W/2, 0.65*cm,
        f"Nexora University  \u2022  Page {doc.page}  \u2022  AY 2026-2027  \u2022  Official Document")
    canvas.setStrokeColor(BD)
    canvas.line(2*cm, 1.05*cm, W - 2*cm, 1.05*cm)
    canvas.restoreState()

def build(filename, elements, title):
    path = KB / filename
    doc = SimpleDocTemplate(str(path), pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm, topMargin=2.2*cm, bottomMargin=2*cm,
        title=title, author="Nexora University")
    cb = lambda c, d: page_decor(c, d, title)
    doc.build(elements, onFirstPage=cb, onLaterPages=cb)
    kb = path.stat().st_size // 1024
    print(f"  \u2713 {filename}  [{kb} KB]")

# ── Helper flowables ─────────────────────────────────────────────────────────
def cover(title, subtitle, cat=""):
    return [
        Spacer(1, 1.8*cm),
        Paragraph("NEXORA UNIVERSITY", ST["cu"]),
        Spacer(1, 0.25*cm),
        HRFlowable(width="80%", thickness=1, color=GD, hAlign="CENTER"),
        Spacer(1, 0.5*cm),
        Paragraph(title.upper(), ST["ct"]),
        Spacer(1, 0.2*cm),
        Paragraph(subtitle, ST["cs"]),
        Spacer(1, 0.4*cm),
        HRFlowable(width="40%", thickness=0.5, color=GD, hAlign="CENTER"),
        Spacer(1, 0.3*cm),
        Paragraph(f"Academic Year 2026-2027  |  {cat}", ST["cv"]),
        Spacer(1, 0.2*cm),
        Paragraph("Innovation District, Hyderabad, Telangana 500032", ST["cv"]),
        Paragraph("www.nexorauniversity.edu  |  info@nexorauniversity.edu", ST["cv"]),
        PageBreak(),
    ]

def toc(sections):
    e = [Paragraph("TABLE OF CONTENTS", ST["h1"]),
         HRFlowable(width="100%", thickness=1, color=DG), Spacer(1, 0.3*cm)]
    for i, (n, t) in enumerate(sections, 1):
        e.append(Paragraph(f"{n}.  {t}", ST["to"]))
    e += [Spacer(1, 0.4*cm), PageBreak()]
    return e

def sec(title, sub=None):
    e = [Spacer(1, 0.25*cm), Paragraph(title, ST["h1"]),
         HRFlowable(width="100%", thickness=0.8, color=DG)]
    if sub: e.append(Paragraph(sub, ST["nt"]))
    e.append(Spacer(1, 0.15*cm))
    return e

def sub(title, paras):
    e = [Paragraph(title, ST["h2"])]
    for p in paras: e.append(Paragraph(p, ST["bd"]))
    return e

def bul(title, items):
    e = [Paragraph(title, ST["h3"])]
    for b in items: e.append(Paragraph(f"\u2022 {b}", ST["bl"]))
    e.append(Spacer(1, 0.1*cm))
    return e

def faq(pairs):
    fq = ParagraphStyle("fq", fontName="Helvetica-Bold", fontSize=10,
                         textColor=DG, spaceBefore=8)
    e = [Paragraph("Frequently Asked Questions (FAQ)", ST["h2"]), Spacer(1, 0.1*cm)]
    for q, a in pairs:
        e += [Paragraph(f"Q: {q}", fq), Paragraph(f"A: {a}", ST["bd"])]
    return e

def tbl(headers, rows, widths=None, alt=False):
    data = [[Paragraph(h, ST["th"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), ST["tl"] if i == 0 else ST["td"])
                     for i, c in enumerate(row)])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TS(alt))
    return t

def box(label, val):
    data = [[Paragraph(label, ST["th"]), Paragraph(val, ST["tl"])]]
    t = Table(data, colWidths=[4*cm, 12.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), MG), ("BACKGROUND", (1,0), (1,0), LG),
        ("TEXTCOLOR",  (0,0), (0,0), WH), ("GRID", (0,0), (-1,-1), 0.4, BD),
        ("FONTNAME",   (0,0), (0,0), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 9),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"), ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6), ("LEFTPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def PB(): return PageBreak()
def SP(h=0.3): return Spacer(1, h*cm)

# ═══════════════════════════════════════════════════════════════════════════
# PDF 1 – Admission Handbook 2026
# ═══════════════════════════════════════════════════════════════════════════
def pdf_01():
    e = cover("Admission Handbook 2026", "Undergraduate & Postgraduate Admissions Guide", "Admissions")
    e += toc([("1","About Nexora University"),("2","Programmes Offered"),("3","Eligibility Criteria"),
               ("4","Application Process"),("5","Entrance Examinations"),("6","Merit List & Counselling"),
               ("7","Documents Required"),("8","Fee Payment & Acceptance"),("9","International Students"),
               ("10","Frequently Asked Questions")])
    e += sec("1. About Nexora University","Established 2010 | NAAC A++ | NIRF Rank 18")
    e += sub("1.1 Overview", [
        "Nexora University is a premier autonomous institution located in Innovation District, Hyderabad, Telangana. Founded in 2010, the university has grown to become one of South India's most respected centres of higher education.",
        "Accredited NAAC A++ with a 3.87/4.0 CGPA, ranked 18th in NIRF 2025, Nexora offers over 60 undergraduate, postgraduate, and doctoral programmes across 14 departments.",
        "The 250-acre campus houses state-of-the-art labs, a central library with 2.5 lakh volumes, a 1,200-bed hostel, and a 300+ company placement cell."
    ])
    e += sub("1.2 Vision & Mission", [
        "Vision: To be a globally recognised centre of excellence in education, innovation, and research, shaping transformative leaders of tomorrow.",
        "Mission: Deliver world-class education through cutting-edge curricula, foster research and entrepreneurship, and build industry partnerships that translate into impactful careers.",
    ])
    e += bul("1.3 Key Accreditations & Rankings", [
        "NAAC A++ Grade | CGPA 3.87/4.00 (2025)",
        "NIRF Rank 18 – Engineering | Rank 24 – Overall (2025)",
        "NBA Accredited: CSE, ECE, ME, CE, AIDS departments",
        "ISO 9001:2015 Certified for Quality Management",
        "Affiliated to Jawaharlal Nehru Technological University (JNTU-H)",
        "UGC Recognised under Section 2(f) and 12(B)",
    ])
    e += [PB()]
    e += sec("2. Programmes Offered")
    e += sub("2.1 Undergraduate Programmes (B.Tech / BCA / BBA)", [
        "Nexora offers a comprehensive set of undergraduate programmes designed to provide both theoretical foundations and practical exposure through mandatory internships and industry projects.",
    ])
    cw = [5.5*cm, 3*cm, 3*cm, 5*cm]
    e += [tbl(["Programme","Duration","Intake","Eligibility"],
              [["B.Tech CSE","4 Years","240","PCM 60%+ / JEE"],
               ["B.Tech CSE (AI&DS)","4 Years","120","PCM 60%+ / JEE"],
               ["B.Tech ECE","4 Years","120","PCM 60%+ / JEE"],
               ["B.Tech Mechanical","4 Years","60","PCM 60%+ / JEE"],
               ["B.Tech Civil","4 Years","60","PCM 60%+ / JEE"],
               ["BCA","3 Years","120","10+2 Any Stream 50%"],
               ["BBA","3 Years","120","10+2 Any Stream 50%"],
               ["B.Sc Data Science","3 Years","60","10+2 Maths 55%"]], widths=cw), SP()]
    e += sub("2.2 Postgraduate Programmes", [
        "Postgraduate programmes at Nexora are designed for professionals seeking to deepen expertise and transition into research or senior industry roles.",
    ])
    e += [tbl(["Programme","Duration","Intake","Eligibility"],
              [["M.Tech CSE","2 Years","60","B.Tech CSE/IT GATE preferred"],
               ["M.Tech AI & ML","2 Years","60","B.Tech any branch GATE"],
               ["MBA","2 Years","120","Any degree 50%+ CAT/MAT/NEXMAT"],
               ["MCA","2 Years","60","BCA/BSc CS 55%+"],
               ["M.Sc Data Science","2 Years","60","BSc Maths/Stats/CS 55%+"]], widths=cw), SP()]
    e += [PB()]
    e += sec("3. Eligibility Criteria")
    e += sub("3.1 Undergraduate Eligibility", [
        "Applicants for B.Tech programmes must have passed Class 12 (10+2) or equivalent with Physics, Chemistry, and Mathematics as core subjects, securing a minimum aggregate of 60% marks (55% for reserved category candidates).",
        "Valid scores in JEE Main, TS EAMCET, AP EAMCET, or Nexora Entrance Examination (NEXET) are accepted. Foreign nationals with equivalent qualifications may apply through the international admissions window.",
    ])
    e += [tbl(["Category","Min Aggregate","Entrance Accepted"],
              [["General / OBC","60% in PCM","JEE / EAMCET / NEXET"],
               ["SC / ST / EWS","55% in PCM","JEE / EAMCET / NEXET"],
               ["NRI / OCI","60% in PCM","SAT / NEXET / Direct"],
               ["International","Equivalent","NEXET / Direct Interview"]], widths=[5*cm,5*cm,6.5*cm]), SP()]
    e += sub("3.2 Postgraduate Eligibility", [
        "M.Tech applicants must hold a B.Tech/B.E. degree in the relevant or related discipline with a minimum CGPA of 6.0/10 or 60% aggregate. GATE score is preferred but not mandatory for sponsored candidates.",
        "MBA applicants must hold any bachelor's degree with a minimum 50% aggregate and a valid CAT, MAT, XAT, or Nexora Management Aptitude Test (NEXMAT) score.",
    ])
    e += [PB()]
    e += sec("4. Application Process")
    e += sub("4.1 How to Apply – Step by Step", [
        "The entire admissions process is conducted online through the Nexora Admissions Portal at admissions.nexorauniversity.edu. Applicants must complete the process in the following sequence.",
    ])
    for step, desc in [
        ("Step 1: Register","Visit admissions.nexorauniversity.edu → Click 'New Applicant Registration' → Enter name, email, and mobile number → Verify OTP → Set password."),
        ("Step 2: Fill Application","Login → Select programme and specialisation → Fill academic history, entrance scores, and personal details → Upload photograph and signature."),
        ("Step 3: Pay Application Fee","Pay the non-refundable application fee of ₹1,200 online via UPI/Net Banking/Debit Card. Keep the payment receipt."),
        ("Step 4: Submit Application","Review all details → Click 'Final Submit' → Download application acknowledgement with unique Application ID."),
        ("Step 5: Admit Card","Download admit card 7 days before entrance/counselling from the portal."),
        ("Step 6: Entrance / Counselling","Appear for NEXET or submit EAMCET/JEE scores online → Wait for merit list publication."),
        ("Step 7: Allotment & Acceptance","Accept seat within 72 hours of allotment → Pay seat acceptance fee → Report for document verification."),
    ]:
        e += [box(step, desc), SP(0.15)]
    e += [PB()]
    e += sec("5. Entrance Examinations")
    e += sub("5.1 NEXET – Nexora Entrance Test", [
        "NEXET is Nexora's own entrance examination conducted twice yearly (January and May) for students who have not appeared in national exams or wish to improve their scores.",
        "NEXET Pattern: 90 minutes | 90 MCQ questions | Physics (30), Chemistry (30), Mathematics (30) | +4 for correct, -1 for wrong | Maximum score: 360.",
    ])
    e += [tbl(["Subject","Questions","Marks","Duration"],
              [["Physics","30","120","30 min"],["Chemistry","30","120","30 min"],["Mathematics","30","120","30 min"],["Total","90","360","90 min"]],
              widths=[5*cm,3.5*cm,3.5*cm,4.5*cm]), SP()]
    e += [PB()]
    e += sec("6. Documents Required for Admission")
    e += [tbl(["Document","Copies Required","Attestation"],
              [["Class 10 Marksheet & Certificate","2","Self-attested"],
               ["Class 12 Marksheet & Certificate","2","Self-attested"],
               ["Entrance Score Card (JEE/EAMCET/NEXET)","1","Original"],
               ["Transfer Certificate","1","Original from previous institution"],
               ["Character Certificate","1","From previous institution"],
               ["Caste Certificate (if applicable)","2","Gazette officer attested"],
               ["Aadhar Card","2","Self-attested"],
               ["Passport-size photographs","6","Recent (within 3 months)"],
               ["Income Certificate (EWS/Scholarship)","2","MRO/Tahsildar attested"],
               ["Migration Certificate (outside state)","1","Original"]], widths=[7*cm,3.5*cm,5.5*cm]), SP()]
    e += [PB()]
    e += sec("7. Fee Payment & Acceptance")
    e += sub("7.1 Seat Acceptance Fee", [
        "Upon allotment, candidates must pay a non-refundable seat acceptance fee of ₹25,000 within 72 hours to confirm their admission. This amount is adjusted against the first-semester tuition fee.",
        "Failure to pay within the stipulated time will result in automatic cancellation of the allotted seat, and the seat will be offered to the next eligible candidate on the waitlist.",
    ])
    e += [tbl(["Programme","Seat Acceptance Fee","Deadline"],
              [["B.Tech (All Branches)","₹25,000","72 hrs from allotment"],
               ["BCA / BBA","₹15,000","72 hrs from allotment"],
               ["M.Tech / MCA","₹20,000","72 hrs from allotment"],
               ["MBA","₹25,000","72 hrs from allotment"]], widths=[6*cm,5*cm,5.5*cm]), SP()]
    e += [PB()]
    e += sec("8. International Student Admissions")
    e += sub("8.1 International Admissions Window", [
        "Nexora University welcomes applications from international students from all SAARC, Middle Eastern, African, and South-East Asian countries. Applications are accepted year-round through the International Office.",
        "International students are required to submit equivalency certificates from the Association of Indian Universities (AIU), a valid passport, and IELTS 6.0 or TOEFL 80 score for English proficiency (applicable if medium of instruction was not English).",
    ])
    e += bul("8.2 Facilities for International Students", [
        "Dedicated International Student Cell with a full-time counsellor",
        "On-campus accommodation guaranteed for the first year",
        "Cultural orientation and language support programme",
        "Tuition fee in USD/AED also accepted via wire transfer",
        "Airport pickup assistance on request",
        "Visa assistance and police registration support",
    ])
    e += [PB()]
    e += sec("9. Merit List & Counselling Schedule")
    e += [tbl(["Round","Publication Date","Acceptance Deadline","Remarks"],
              [["Round 1 (EAMCET/JEE)","15 June 2026","18 June 2026","Main merit list"],
               ["Round 2 (NEXET May)","25 June 2026","28 June 2026","Remaining seats"],
               ["Spot Round","5 July 2026","Same day","Walk-in counselling"],
               ["PG Round 1","20 July 2026","23 July 2026","GATE + Direct"],
               ["PG Round 2","1 August 2026","4 August 2026","Remaining seats"]], widths=[3*cm,4*cm,4.5*cm,5*cm]), SP()]
    e += [PB()]
    e += sec("10. Frequently Asked Questions")
    e += faq([
        ("Can I apply to multiple programmes simultaneously?",
         "Yes. You may apply to a maximum of 3 programmes in a single application cycle by selecting them during registration. A separate application fee is charged per programme."),
        ("Is there a management quota for admissions?",
         "Yes. 15% of seats in each programme are reserved under the management quota. These seats are allotted on the basis of academic merit and personal interview. Contact the Admissions Office for details."),
        ("What is the refund policy if I withdraw after admission?",
         "Refunds are processed as per UGC guidelines. Withdrawal before the last date for admission entitles the student to a full refund of tuition fees minus the seat acceptance fee and processing charge."),
        ("Is there a lateral entry option for B.Tech?",
         "Yes. Diploma holders in Engineering (3-year polytechnic) with 60% aggregate may seek lateral entry into the second year of B.Tech through TS ECET / AP ECET scores."),
        ("When does the academic year begin?",
         "The academic year for all UG programmes begins the last week of August. PG programmes commence in September. Exact dates are published in the Academic Calendar available at www.nexorauniversity.edu."),
    ])
    build("Admission_Handbook_2026.pdf", e, "Admission Handbook 2026")

# ═══════════════════════════════════════════════════════════════════════════
# PDF 2 – Fee Structure 2026-27
# ═══════════════════════════════════════════════════════════════════════════
def pdf_02():
    e = cover("Fee Structure 2026-2027","Complete Tuition, Hostel & Miscellaneous Fee Schedule","Finance")
    e += toc([("1","Tuition Fee – UG Programmes"),("2","Tuition Fee – PG Programmes"),
               ("3","Hostel & Mess Fee"),("4","Miscellaneous Charges"),("5","Scholarship Deductions"),
               ("6","Payment Schedule"),("7","Refund Policy"),("8","Fee Concessions"),("9","FAQs")])
    e += sec("1. Tuition Fee – Undergraduate Programmes")
    e += sub("1.1 B.Tech Annual Tuition Fee (Per Year)", [
        "The following table lists the annual tuition fee for all B.Tech programmes for the academic year 2026-2027. Fees are payable in two equal installments per semester.",
    ])
    e += [tbl(["Programme","General / OBC (₹)","SC / ST (₹)","NRI (USD)"],
              [["B.Tech CSE","1,85,000","1,20,000","4,500"],
               ["B.Tech CSE (AI & Data Science)","2,00,000","1,30,000","4,800"],
               ["B.Tech ECE","1,75,000","1,15,000","4,200"],
               ["B.Tech Mechanical Engineering","1,65,000","1,10,000","4,000"],
               ["B.Tech Civil Engineering","1,60,000","1,05,000","3,800"],
               ["B.Tech AIDS (Lateral Entry)","1,80,000","1,15,000","4,300"],
               ["BCA (3-Year)","90,000","65,000","2,200"],
               ["BBA (3-Year)","85,000","60,000","2,000"],
               ["B.Sc Data Science","95,000","68,000","2,300"]], widths=[6.5*cm,4*cm,3.5*cm,2.5*cm]), SP()]
    e += sub("1.2 One-Time Admission Charges", [
        "In addition to annual tuition fees, the following one-time charges are payable at the time of admission only.",
    ])
    e += [tbl(["Charge","Amount (₹)","Remarks"],
              [["Registration / Admission Fee","5,000","Non-refundable"],
               ["Caution Deposit (Library)","3,000","Refundable on graduation"],
               ["Caution Deposit (Lab)","2,000","Refundable on graduation"],
               ["Student ID Card","300","One-time"],
               ["University Uniform (2 sets)","2,500","Mandatory first year"],
               ["Alumni Registration","500","One-time lifetime membership"]], widths=[6.5*cm,4*cm,6*cm]), SP()]
    e += [PB()]
    e += sec("2. Tuition Fee – Postgraduate Programmes")
    e += [tbl(["Programme","Annual Fee (₹)","GATE Scholarship","NRI (USD)"],
              [["M.Tech CSE","1,50,000","₹12,400/month (GATE score ≥ 650)","3,600"],
               ["M.Tech AI & ML","1,60,000","₹12,400/month (GATE score ≥ 650)","3,800"],
               ["MBA (2-Year)","2,20,000","Merit scholarship up to 50%","5,200"],
               ["MCA (2-Year)","1,10,000","Merit scholarship up to 30%","2,600"],
               ["M.Sc Data Science","1,05,000","Merit scholarship up to 30%","2,500"],
               ["Ph.D (per semester)","50,000","Stipend for funded scholars","–"]], widths=[5.5*cm,3.5*cm,5*cm,2.5*cm]), SP()]
    e += [PB()]
    e += sec("3. Hostel & Mess Fee (Annual)")
    e += sub("3.1 Hostel Accommodation", [
        "The university provides on-campus hostel facilities for both male and female students. All rooms are furnished with bed, mattress, study table, chair, cupboard, and Wi-Fi access.",
    ])
    e += [tbl(["Room Type","Occupancy","Annual Rent (₹)","Included"],
              [["Standard Room","4 per room","45,000","Wi-Fi, Hot water, Power backup"],
               ["Semi-Private Room","2 per room","65,000","Wi-Fi, Hot water, AC optional"],
               ["Private Room","1 per room","90,000","Wi-Fi, Hot water, AC included"],
               ["PG/MBA Block (AC)","2 per room","80,000","Wi-Fi, AC, Attached bath"]], widths=[4.5*cm,3*cm,4*cm,5*cm]), SP()]
    e += sub("3.2 Mess Fee", [
        "Mess fee is payable on an annual basis. The mess operates on a fixed meal plan providing breakfast, lunch, evening snacks, and dinner seven days a week.",
    ])
    e += [tbl(["Plan","Meals Included","Annual Fee (₹)"],
              [["Veg Thali Plan","All 4 meals/day","42,000"],
               ["Non-Veg Plan","All 4 meals/day (non-veg 4x/week)","48,000"],
               ["Flexible Plan","Lunch + Dinner only","32,000"],
               ["Jain / Special Diet","All 4 meals (customised)","50,000"]], widths=[5*cm,6*cm,5.5*cm]), SP()]
    e += [PB()]
    e += sec("4. Miscellaneous & Utility Charges")
    e += [tbl(["Item","Amount (₹)","Frequency"],
              [["Examination Fee (per semester)","1,500","Per semester"],
               ["Sports & Cultural Fee","2,500","Annual"],
               ["Student Union Fee","500","Annual"],
               ["Medical Insurance Premium","1,200","Annual"],
               ["Internet / Wi-Fi (Campus)","Included in tuition","–"],
               ["Lab Consumables (Engineering)","3,000","Annual"],
               ["Library Fine (per day overdue)","10","Per item"],
               ["Duplicate ID Card","200","Per instance"],
               ["Transcript Issuance","500","Per request"],
               ["Migration Certificate","500","One-time"]], widths=[6*cm,4*cm,6.5*cm]), SP()]
    e += [PB()]
    e += sec("5. Fee Payment Schedule")
    e += [tbl(["Semester","Instalment","Due Date","Late Fine"],
              [["Odd Sem (Jul–Nov)","1st Instalment (50%)","10 July 2026","₹100/day after 10 July"],
               ["Odd Sem (Jul–Nov)","2nd Instalment (50%)","10 September 2026","₹100/day after due date"],
               ["Even Sem (Jan–May)","1st Instalment (50%)","10 January 2027","₹100/day after due date"],
               ["Even Sem (Jan–May)","2nd Instalment (50%)","10 March 2027","₹100/day after due date"]], widths=[4.5*cm,4.5*cm,4.5*cm,3*cm]), SP()]
    e += sub("5.1 Payment Modes Accepted", [
        "Online payment via the student portal (UPI, Net Banking, Debit/Credit Card), NEFT/RTGS to university bank account, Demand Draft payable to 'Nexora University' at Hyderabad.",
    ])
    e += [PB()]
    e += sec("6. Scholarship Fee Deductions")
    e += [tbl(["Scholarship","Eligibility","Deduction"],
              [["Merit Scholarship Tier 1","CGPA ≥ 9.5 in previous year","50% tuition fee waiver"],
               ["Merit Scholarship Tier 2","CGPA 9.0–9.49","30% tuition fee waiver"],
               ["Merit Scholarship Tier 3","CGPA 8.5–8.99","15% tuition fee waiver"],
               ["GATE Scholarship (M.Tech)","GATE score ≥ 650","Full tuition + ₹12,400/month"],
               ["SC/ST Government Scholarship","As per state norms","Full fee reimbursement (post-matric)"],
               ["Sports Achievement Award","State/National level","25% tuition waiver"],
               ["EWS Scholarship","Annual income < ₹8 lakh","20% tuition waiver"]], widths=[5.5*cm,5.5*cm,5.5*cm]), SP()]
    e += [PB()]
    e += sec("7. Refund Policy")
    e += sub("7.1 Withdrawal Refund Schedule", [
        "As per UGC guidelines (Order F.No.25-3/2020-DEB-I), refunds are processed based on withdrawal date relative to the start of the academic session.",
    ])
    e += [tbl(["Withdrawal Timeline","% Refund","Processing Time"],
              [["Before last day of admission","100% of fees paid","7 working days"],
               ["Within 15 days after admission close","80% of fees paid","10 working days"],
               ["Between 16–30 days after admission close","50% of fees paid","10 working days"],
               ["After 30 days of admission close","No refund","–"]], widths=[7*cm,3.5*cm,5*cm]), SP()]
    e += sub("7.2 Caution Deposit Refund", [
        "Library and Lab caution deposits are refunded within 30 days of completion of programme upon return of all issued materials and clearance certificates from respective departments.",
    ])
    e += [PB()]
    e += sec("8. Frequently Asked Questions – Fees")
    e += faq([
        ("Can I pay fees in instalments?",
         "Yes. Fees are split across two instalments per semester. Additional instalment options up to 4 parts can be arranged via a written request to the Finance Office with a valid reason."),
        ("What happens if I miss the fee payment deadline?",
         "A late fine of ₹100 per day is charged from the due date. Access to examination hall tickets and portal is restricted until full outstanding amount including fine is cleared."),
        ("Is the hostel fee compulsory?",
         "No. Hostel fee is only applicable to students who opt for on-campus accommodation. Day scholars are exempt from hostel and mess charges."),
        ("Where do I get the fee payment receipt?",
         "Official fee receipts are auto-generated on the student portal immediately after successful payment. Physical receipts can be collected from the Finance Office within 3 working days."),
    ])
    build("Fee_Structure_2026.pdf", e, "Fee Structure 2026-27")

# ═══════════════════════════════════════════════════════════════════════════
# PDF 3 – Hostel & Accommodation Guide
# ═══════════════════════════════════════════════════════════════════════════
def pdf_03():
    e = cover("Hostel & Accommodation Guide","On-Campus Residential Life Handbook","Hostel")
    e += toc([("1","Hostel Facilities Overview"),("2","Room Types & Allotment"),("3","Mess & Dining"),
               ("4","Hostel Rules & Regulations"),("5","Visitor Policy"),("6","Security Arrangements"),
               ("7","Grievance & Maintenance"),("8","Hostel Fee Summary"),("9","FAQs")])
    e += sec("1. Hostel Facilities Overview","Nexora University provides fully managed residential facilities for students from outside Hyderabad.")
    e += sub("1.1 Hostel Blocks", [
        "The campus has 6 hostel blocks — 4 for male students (Blocks A, B, C, D) and 2 for female students (Blocks E, F). All blocks are equipped with 24/7 power backup, CCTV surveillance, and biometric entry.",
        "Total capacity: 1,200 beds. Occupancy is allocated on a first-come, first-served basis at the time of admission. PG students are housed in dedicated floors in Blocks C and F.",
    ])
    e += [tbl(["Block","For","Capacity","AC Rooms","Facilities"],
              [["Block A","Male UG","200 beds","No","Common room, TV lounge"],
               ["Block B","Male UG","200 beds","No","Gym, Study hall"],
               ["Block C","Male UG+PG","200 beds","Select floors","Quiet zone, high-speed Wi-Fi"],
               ["Block D","Male UG","160 beds","No","Sports area, common hall"],
               ["Block E","Female UG+PG","220 beds","Select floors","Beauty salon, recreation room"],
               ["Block F","Female UG","220 beds","No","Reading room, indoor games"]], widths=[2.5*cm,4*cm,3*cm,3*cm,4*cm]), SP()]
    e += sub("1.2 Common Amenities", [
        "All hostel blocks share the following common facilities: 24-hour water supply (hot + cold), coin-operated washing machines (20 units per block), ironing stations, common refrigerators, solar-heated water, purified drinking water dispensers every floor, and high-speed Wi-Fi (up to 100 Mbps per room).",
    ])
    e += [PB()]
    e += sec("2. Room Allotment Process")
    e += [tbl(["Step","Action","Mode","Deadline"],
              [["1","Fill hostel preference form","Online – Student Portal","Within 7 days of admission"],
               ["2","Room type selection and payment","Online payment","Within 72 hrs of allotment"],
               ["3","Room key and access card issue","Hostel Office","Reporting day"],
               ["4","Inventory verification","Physical – with warden","Move-in day"]],
              widths=[1.5*cm,6*cm,5*cm,4*cm]), SP()]
    e += sub("2.1 Room Type Details", [
        "Students may request room type preference, subject to availability. Room allotments are final and change requests are only entertained in the first 10 days of the semester.",
    ])
    e += [tbl(["Type","Occupancy","Size (sq.ft)","Monthly Rent (₹)","AC"],
              [["Standard","4-sharing","200","3,750","No"],
               ["Semi-Private","2-sharing","160","5,400","No"],
               ["Private","Single","120","7,500","No"],
               ["AC Semi-Private","2-sharing","160","6,800","Yes"],
               ["AC Private","Single","120","9,500","Yes"],
               ["PG Suite (MBA)","2-sharing","200","7,200","Yes"]], widths=[4*cm,3*cm,3.5*cm,3.5*cm,2.5*cm]), SP()]
    e += [PB()]
    e += sec("3. Mess & Dining Services")
    e += sub("3.1 Dining Hall Details", [
        "The university operates 3 mess halls — Mess 1 (Block A-B), Mess 2 (Block C-D), and Ladies Mess (Block E-F). All mess halls are managed by professional catering staff and supervised by a Mess Committee of student representatives.",
        "Menu is rotated weekly. Sampler menus are available on notice boards and the student portal. Special dietary requests (Jain, diabetic, gluten-free) must be registered at the Mess Office.",
    ])
    e += [tbl(["Meal","Time","Menu Highlights"],
              [["Breakfast","7:00 – 9:00 AM","Idli/Dosa/Paratha, Bread-Butter, Fruits, Tea/Coffee"],
               ["Lunch","12:00 – 2:00 PM","Rice, Dal, 2 Sabzis, Salad, Buttermilk, Curd"],
               ["Snacks","5:00 – 6:00 PM","Samosa/Bonda, Tea/Coffee, Biscuits"],
               ["Dinner","7:30 – 9:30 PM","Chapati, Rice, Dal, 2 Curries, Dessert (alternate days)"]], widths=[3*cm,4*cm,9.5*cm]), SP()]
    e += sub("3.2 Mess Committee", [
        "A Mess Committee comprising 2 student representatives per block meets monthly to review menu quality, hygiene, and vendor performance. Students may submit feedback via the QR code displayed in each dining hall.",
    ])
    e += [PB()]
    e += sec("4. Hostel Rules & Regulations")
    e += bul("4.1 General Conduct Rules", [
        "Ragging in any form — physical, verbal, cyber — is strictly prohibited and punishable under the Anti-Ragging Act. Zero tolerance policy enforced.",
        "Consumption of alcohol, tobacco, drugs, and psychotropic substances is completely prohibited within the hostel campus.",
        "All students must carry their university ID card at all times within the campus.",
        "Guests of the opposite gender are NOT permitted inside hostel rooms or floors.",
        "Playing loud music, use of electric cooking appliances, and keeping pets are strictly prohibited.",
        "Damage to hostel property will be recovered at full cost from the student.",
        "Silent study hours: 10:00 PM – 6:00 AM. All noise to be minimised.",
    ])
    e += bul("4.2 Gate Timings & Curfew", [
        "Male students: Hostel gate closes at 10:30 PM. Re-entry after 10:30 PM requires prior written permission from warden.",
        "Female students: Hostel gate closes at 9:30 PM. Late entry requires written permission from Chief Warden and parental consent.",
        "Night-out permission: A maximum of 2 night-outs per semester are allowed with duly filled permission form signed by parent/guardian.",
        "Continuous absence for more than 3 days without information to warden will be reported to parents and Dean of Students.",
    ])
    e += [PB()]
    e += sec("5. Visitor Policy")
    e += [tbl(["Visitor Type","Permission Level","Allowed Areas","Timings"],
              [["Parents / Guardians","Always permitted","Reception, Visitor Lounge","9 AM – 6 PM"],
               ["Siblings (same gender)","Always permitted","Common Room only","9 AM – 8 PM"],
               ["Friends (same gender)","Requires warden permission","Visitor Lounge only","10 AM – 5 PM"],
               ["Opposite gender (family)","Chief Warden permission","Visitor Lounge only","10 AM – 4 PM"],
               ["Vendors / Service","Hostel Office permission","Common areas only","9 AM – 12 PM"]], widths=[3.5*cm,4*cm,4*cm,4*cm]), SP()]
    e += [PB()]
    e += sec("6. Security & Safety")
    e += sub("6.1 Security Infrastructure", [
        "The hostel campus is secured by a 3-tier security system: biometric entry gates, CCTV (240 cameras covering all corridors, entries, and common areas), and 24/7 security guard patrol.",
        "An emergency panic button is installed in each room of the female hostel blocks and is directly connected to the campus security control room.",
    ])
    e += bul("6.2 Emergency Contacts", [
        "Campus Security (24/7): +91-40-4567-8901",
        "Female Hostel Warden: +91-40-4567-8912",
        "Male Hostel Chief Warden: +91-40-4567-8910",
        "Medical Centre: +91-40-4567-8920",
        "Police Control Room: 100 | Fire: 101 | Ambulance: 108",
        "Anti-Ragging Helpline: 1800-180-5522",
    ])
    e += [PB()]
    e += sec("7. Maintenance & Grievance")
    e += sub("7.1 Maintenance Requests", [
        "All maintenance requests (electrical, plumbing, furniture, Wi-Fi) must be raised through the Nexora Student Portal under 'Hostel Services → Raise Request'. Resolution SLA: Electrical 4 hours, Plumbing 6 hours, Furniture 24 hours.",
    ])
    e += faq([
        ("Can I stay in the hostel during semester break?",
         "Yes, with prior application and payment of a break stay charge of ₹150 per day. Applications must be submitted at least 5 days before semester end."),
        ("What do I do if I lose my room key or access card?",
         "Report to the Hostel Office immediately. A duplicate key/card is issued within 24 hours at a charge of ₹300 for key and ₹200 for access card."),
        ("Can I bring my own electrical appliances?",
         "Small appliances like laptops, phone chargers, and study lamps are permitted. High-wattage appliances like immersion heaters, electric kettles, and irons (personal) are prohibited due to fire safety regulations."),
        ("Is there a laundry service?",
         "Coin-operated washing machines are available in each block (₹30 per wash). A professional laundry service is also available on campus at additional cost."),
        ("What is the policy for hostel room change?",
         "Room change requests are considered only in the first 10 days of each semester. Changes require written approval from the Chief Warden and are granted only for medical or genuine compatibility reasons."),
    ])
    build("Hostel_Accommodation_Guide.pdf", e, "Hostel & Accommodation Guide")

# ═══════════════════════════════════════════════════════════════════════════
# PDF 4 – Placement & Career Development Guide
# ═══════════════════════════════════════════════════════════════════════════
def pdf_04():
    e = cover("Placement & Career Development Guide","2025-26 Placement Statistics & Preparation Roadmap","Placements")
    e += toc([("1","About the Career Development Centre"),("2","Placement Statistics 2025-26"),
               ("3","Top Recruiters"),("4","Placement Process"),("5","Eligibility & Criteria"),
               ("6","Internship Programme"),("7","Career Preparation Resources"),("8","Industry Connect"),("9","FAQs")])
    e += sec("1. About the Career Development Centre (CDC)")
    e += sub("1.1 Overview", [
        "The Career Development Centre (CDC) at Nexora University is a dedicated 24-member team of placement coordinators, industry liaisons, career counsellors, and technical training faculty who work year-round to connect students with top employers.",
        "CDC offers end-to-end placement support from first year through final placement — aptitude preparation, mock interviews, industry visits, resume workshops, and exclusive campus recruitment drives.",
    ])
    e += bul("1.2 Key CDC Services", [
        "Campus Recruitment Drives (on-campus and off-campus)",
        "1-on-1 Career Counselling sessions",
        "Resume and LinkedIn Profile building workshops",
        "Mock technical and HR interview panels (3 rounds per student/year)",
        "Aptitude and coding bootcamps (6-week intensive each semester)",
        "Industry guest lecture series: 40+ sessions per year",
        "GATE, CAT, GRE, IELTS coaching partnerships",
        "Startup incubation and entrepreneurship guidance",
    ])
    e += [PB()]
    e += sec("2. Placement Statistics 2025-26")
    e += sub("2.1 Overall Placement Summary", [
        "The academic year 2025-26 recorded Nexora's highest-ever placement rate of 94.3% for eligible final-year B.Tech students. A total of 312 companies visited the campus conducting 890 placement drives.",
    ])
    e += [tbl(["Metric","2025-26","2024-25","2023-24"],
              [["Total Students Eligible","1,180","1,050","940"],
               ["Students Placed","1,113 (94.3%)","962 (91.6%)","840 (89.4%)"],
               ["Companies Visited","312","278","240"],
               ["Highest Package (₹ LPA)","58.0","52.0","46.0"],
               ["Average Package (₹ LPA)","12.4","10.8","9.6"],
               ["Median Package (₹ LPA)","9.6","8.4","7.8"],
               ["International Offers","28","19","12"],
               ["PPO Conversions","187","142","118"]], widths=[7*cm,3*cm,3*cm,3.5*cm]), SP()]
    e += sub("2.2 Placement by Department", [
        "CSE continues to lead placements with a 98% placement rate. AI&DS department recorded the highest average package at ₹15.2 LPA in its second year.",
    ])
    e += [tbl(["Department","Eligible","Placed","% Placed","Avg CTC (LPA)","Highest CTC (LPA)"],
              [["CSE","340","333","98.0%","15.2","58.0"],
               ["CSE (AI&DS)","118","115","97.5%","17.8","52.0"],
               ["ECE","230","218","94.8%","9.6","24.0"],
               ["Mechanical","180","162","90.0%","7.2","18.0"],
               ["Civil","120","103","85.8%","6.8","14.0"],
               ["BCA","98","89","90.8%","5.6","12.0"],
               ["BBA","94","93","98.9%","6.2","16.0"]], widths=[3.5*cm,2.5*cm,2.5*cm,2.5*cm,3.5*cm,3.5*cm]), SP()]
    e += [PB()]
    e += sec("3. Top Recruiters 2025-26")
    e += [tbl(["Company","Sector","Roles Offered","Avg CTC (LPA)"],
              [["Google","Technology","SWE, ML Engineer","42.0+"],
               ["Microsoft","Technology","SDE, Product Analyst","38.0+"],
               ["Amazon","E-Commerce / Cloud","SDE, SDE-II, Data Engineer","28.0+"],
               ["Infosys","IT Services","Systems Engineer, DEx","6.5"],
               ["TCS","IT Services","Engineer, Business Analyst","7.0"],
               ["Wipro","IT Services","Project Engineer","6.5"],
               ["Hyundai Motor India","Automotive","Grad Engineer Trainee","6.8"],
               ["Capgemini","IT Consulting","Associate Consultant","8.0"],
               ["Deloitte","Consulting / Tech","Analyst, UST","9.5"],
               ["Goldman Sachs","Finance / Technology","Analyst","32.0+"],
               ["JP Morgan Chase","Finance / Technology","SWE Analyst","28.0+"],
               ["KPMG","Audit / Consulting","Associate","7.5"],
               ["Swiggy","Technology","SWE, Data Scientist","18.0"],
               ["Zomato","Technology","SWE, Analytics","16.0"],
               ["Freshworks","SaaS","SDE-I, Customer Success","14.0"]], widths=[4.5*cm,3.5*cm,4*cm,4.5*cm]), SP()]
    e += [PB()]
    e += sec("4. Campus Placement Process")
    e += [tbl(["Round","Description","Duration"],
              [["1 – Resume Shortlist","Company shortlists based on CGPA, skills, and resume","1-2 days"],
               ["2 – Online Test","Aptitude, Coding (2-3 problems, 90 min), Verbal","90 min"],
               ["3 – Technical Interview","DSA, OS, DBMS, OOPs, projects, internship discussion","45-60 min"],
               ["4 – HR Interview","Culture fit, communication, salary discussion","20-30 min"],
               ["5 – Final Offer","Offer letter issued within 7 working days","–"]], widths=[4.5*cm,7.5*cm,3.5*cm]), SP()]
    e += bul("4.1 Important Placement Policy", [
        "Students may accept a maximum of 1 placement offer. A student placed in a company with CTC ≥ ₹12 LPA is not eligible for further campus drives ('Dream Company' policy).",
        "Students may participate in unlimited drives until placed.",
        "CGPA below 6.0 makes a student ineligible for premium drives (CTC > ₹15 LPA).",
        "Minimum 75% attendance mandatory to participate in campus placements.",
        "Students must register for each drive separately via the CDC Portal 48 hours before the drive.",
    ])
    e += [PB()]
    e += sec("5. Internship Programme")
    e += sub("5.1 Summer Internship (2nd Year – 3rd Year Transition)", [
        "A mandatory 8-week summer internship is compulsory for all B.Tech students between 2nd and 3rd year (May–July). Students must secure their own internship or apply through CDC's internship database (400+ partner companies).",
    ])
    e += [tbl(["Internship Partner","Sector","Stipend Range","Duration"],
              [["IIT Hyderabad Research Lab","Research","₹10,000–₹15,000/month","8 weeks"],
               ["Microsoft Research","Technology","₹30,000–₹50,000/month","8 weeks"],
               ["Infosys InStep","IT Services","₹10,000–₹20,000/month","8 weeks"],
               ["Goldman Sachs (Summer)","Finance","₹60,000/month","10 weeks"],
               ["Government of Telangana","Public Sector","₹5,000/month","6 weeks"]], widths=[5*cm,3.5*cm,4.5*cm,3.5*cm]), SP()]
    e += [PB()]
    e += sec("6. FAQs – Placements")
    e += faq([
        ("What is the minimum CGPA required to sit for campus placements?",
         "A minimum CGPA of 5.0 is required to be eligible for campus placements. However, most premium companies (CTC > ₹10 LPA) require CGPA ≥ 7.0 or 8.0. Dream company drives require CGPA ≥ 8.5."),
        ("Can I get placed off-campus through CDC support?",
         "Yes. CDC conducts year-round off-campus placement drives, job fairs, and maintains a placement portal with live job postings from 500+ partner companies. Off-campus placements are counted in official placement records."),
        ("How many companies visit for MBA placements?",
         "Approximately 80 companies visit for MBA placements covering BFSI, Consulting, FMCG, IT, and E-Commerce sectors. Average CTC for MBA 2025-26 was ₹10.8 LPA with a highest of ₹28 LPA."),
        ("Is it mandatory to participate in campus placements?",
         "No. Participation is voluntary. Students pursuing higher education (GATE/CAT/GRE/UPSC) or starting their own venture may opt out by submitting a declaration to the CDC."),
    ])
    build("Placement_Report_2026.pdf", e, "Placement & Career Development Guide")

# ═══════════════════════════════════════════════════════════════════════════
# PDF 5 – Academic Regulations & Examination Rules
# ═══════════════════════════════════════════════════════════════════════════
def pdf_05():
    e = cover("Academic Regulations & Examination Rules","Grading, Attendance, Backlog & Academic Integrity Policies","Academics")
    e += toc([("1","Academic Calendar Overview"),("2","Credit System & Grading"),("3","Attendance Policy"),
               ("4","Internal Assessment"),("5","End-Semester Examinations"),("6","Revaluation & Challenges"),
               ("7","Backlog & Supplementary Exams"),("8","Promotion Rules"),("9","Academic Integrity"),("10","FAQs")])
    e += sec("1. Academic Calendar Overview")
    e += [tbl(["Event","Odd Semester (Jul–Nov)","Even Semester (Jan–May)"],
              [["Classes Begin","25 July 2026","2 January 2027"],
               ["Internal Assessment 1","3rd week of September","3rd week of February"],
               ["Mid-Semester Break","3rd week of October","2nd week of March"],
               ["Internal Assessment 2","2nd week of November","3rd week of April"],
               ["Last Working Day","21 November 2026","7 May 2027"],
               ["Practical Examinations","22–28 November","8–14 May"],
               ["End-Semester Theory Exams","29 November – 16 December","15–30 May"],
               ["Result Declaration","5 January 2027","20 June 2027"]], widths=[6*cm,5*cm,5.5*cm]), SP()]
    e += [PB()]
    e += sec("2. Credit System & Grading Policy")
    e += sub("2.1 Credit Distribution", [
        "Nexora follows a 10-point Cumulative Grade Point Average (CGPA) system aligned with AICTE guidelines. Each course carries a fixed number of credits based on contact hours per week.",
    ])
    e += [tbl(["Contact Hours/Week","Credits Assigned","Course Type"],
              [["3L + 0T + 0P","3","Theory only"],
               ["3L + 1T + 0P","4","Theory with tutorial"],
               ["3L + 0T + 3P","5","Theory + Lab"],
               ["0L + 0T + 3P","2","Lab only / Project"],
               ["0L + 0T + 6P","4","Full project / Seminar"]], widths=[4.5*cm,4*cm,8*cm]), SP()]
    e += sub("2.2 Grading Scale", [
        "Grades are awarded on a letter scale mapped to grade points. CGPA is calculated as the weighted average of grade points earned.",
    ])
    e += [tbl(["Marks Range (%)","Grade","Grade Point","Performance Level"],
              [["90–100","O","10","Outstanding"],
               ["80–89","A+","9","Excellent"],
               ["70–79","A","8","Very Good"],
               ["60–69","B+","7","Good"],
               ["50–59","B","6","Above Average"],
               ["40–49","C","5","Average"],
               ["< 40","F","0","Fail – Re-examination required"]], widths=[4.5*cm,2.5*cm,3*cm,6.5*cm]), SP()]
    e += [PB()]
    e += sec("3. Attendance Policy")
    e += sub("3.1 Minimum Attendance Requirement", [
        "A minimum of 75% attendance in each course is mandatory for eligibility to appear in End-Semester Examinations. Attendance below 75% in any course will result in detention from that course's examination.",
    ])
    e += [tbl(["Attendance %","Status","Action"],
              [["≥ 75%","Eligible","No action required"],
               ["65–74%","Conditional","Fine of ₹500 per subject; condonation by Principal"],
               ["50–64%","Detained","Not allowed to appear; repeat the course next year"],
               ["< 50%","Detained + Referred","Not allowed; referred to academic counsellor"]], widths=[4*cm,4*cm,8.5*cm]), SP()]
    e += bul("3.2 Valid Reasons for Attendance Condonation", [
        "Serious illness with medical certificate from a registered hospital",
        "Bereavement of immediate family member (with documentary proof)",
        "Representing university in sports/cultural/technical events (prior approval required)",
        "Natural calamities and declared public emergencies",
        "Maximum condonation: 10% of total working days (subject to HOD and Principal approval)",
    ])
    e += [PB()]
    e += sec("4. Internal Assessment Structure")
    e += [tbl(["Component","Marks","Weightage","Schedule"],
              [["Internal Assessment Test 1 (IA-1)","20","10%","3rd week, September/February"],
               ["Internal Assessment Test 2 (IA-2)","20","10%","2nd week, November/April"],
               ["Assignments & Quizzes","10","5%","Continuous throughout semester"],
               ["Seminar / Presentation","10","5%","4th month of semester"],
               ["Laboratory Practical","25","25%","Ongoing + End-sem Practical"],
               ["End-Semester Theory Exam","100","50%","End of semester"],
               ["Project Work (Final Year)","100","Replaces 2 theory courses","Viva-Voce + Report"]], widths=[5*cm,2.5*cm,3*cm,6*cm]), SP()]
    e += [PB()]
    e += sec("5. End-Semester Examinations")
    e += sub("5.1 Examination Rules", [
        "Students must carry their Hall Ticket (downloaded from portal) and University Photo ID to every examination. No student will be permitted entry without a valid Hall Ticket.",
        "Hall tickets are issued to students with ≥ 75% attendance (or condoned ≥ 65%) and with all fee dues cleared.",
    ])
    e += bul("5.2 Examination Conduct Rules", [
        "Mobile phones, smart watches, earphones, and Bluetooth devices are strictly prohibited in examination halls.",
        "Malpractice (copying, chits) → immediate cancellation + suspension for 1 semester. Repeat offence → rustication.",
        "Late entry permitted only within first 30 minutes. No student can leave the hall before 1 hour.",
        "Answer booklets must be written in blue/black pen only. Pencil allowed only for diagrams.",
        "Additional answer sheets available on request from invigilator.",
    ])
    e += [PB()]
    e += sec("6. Backlog, Revaluation & Supplementary Exams")
    e += [tbl(["Examination","When Conducted","Eligibility","Fee per Subject"],
              [["Supplementary Exam","After result of main exam","F grade in ≤ 4 subjects","₹800"],
               ["Arrear Exam (Backlog)","Odd/Even sem along with regular","Any F grade from previous years","₹800"],
               ["Revaluation Request","Within 10 days of result","Score of 25-39% only","₹500"],
               ["Photocopy of Answer Sheet","Within 5 days of result","Any student","₹200"],
               ["Grade Challenge","Post-revaluation","Difference of > 5 marks","₹1,000"]], widths=[4.5*cm,4*cm,4.5*cm,3.5*cm]), SP()]
    e += sub("6.1 Backlog Policy", [
        "Students with more than 6 active backlogs at the end of 4th semester will be placed on Academic Probation. A personalised Academic Recovery Plan (ARP) is prepared with the academic counsellor.",
    ])
    e += [PB()]
    e += sec("7. Academic Integrity & Plagiarism Policy")
    e += sub("7.1 Plagiarism Policy", [
        "All written assignments, project reports, dissertations, and research papers are checked via plagiarism detection tools. Acceptable similarity index: ≤ 15%.",
    ])
    e += [tbl(["Plagiarism Level","Similarity %","First Offence","Second Offence"],
              [["Minor","16–30%","Redo assignment","Grade reduction (–1 grade)"],
               ["Moderate","31–50%","Grade 'F' for assignment","F for entire course"],
               ["Severe","> 50%","F for entire course","Academic suspension 1 semester"],
               ["Fabrication","Any","F for course + report to committee","Rustication"]], widths=[3.5*cm,3.5*cm,5*cm,4.5*cm]), SP()]
    e += [PB()]
    e += sec("8. FAQs – Academics")
    e += faq([
        ("What is the minimum CGPA to maintain a scholarship?",
         "Merit scholarships require CGPA ≥ 8.5 (Tier 1), ≥ 9.0 (Tier 2), or ≥ 9.5 (Tier 3) at the end of each academic year. CGPA is reviewed annually and scholarships are renewed accordingly."),
        ("How is CGPA calculated?",
         "CGPA = Σ(Grade Points × Credits) / Σ(Credits). It is calculated at the end of each semester and updated cumulatively. All theory and lab courses are included."),
        ("Can I improve my grade after passing a course?",
         "Yes. Grade Improvement Examination is allowed once for up to 2 courses per programme. The higher of the two scores is considered. Grade improvement is not allowed for final-year project or viva."),
        ("What happens if I fail the project viva?",
         "Students failing the final-year project viva may resubmit within the same semester or appear in the supplementary viva conducted within 30 days. A maximum of 2 viva attempts are permitted."),
    ])
    build("Academic_Regulations_2026.pdf", e, "Academic Regulations & Examination Rules")

# ═══════════════════════════════════════════════════════════════════════════
# PDF 6 – Scholarships & Financial Aid Handbook
# ═══════════════════════════════════════════════════════════════════════════
def pdf_06():
    e = cover("Scholarships & Financial Aid Handbook","Merit, Need-Based, Government & External Scholarships","Scholarships")
    e += toc([("1","University Merit Scholarships"),("2","Need-Based Financial Aid"),("3","Government Scholarships"),
               ("4","External & Corporate Scholarships"),("5","GATE Fellowship"),("6","Sports & Arts Scholarships"),
               ("7","Application Process"),("8","Scholarship Calendar"),("9","FAQs")])
    e += sec("1. University Merit Scholarships")
    e += sub("1.1 Annual Merit Scholarship Tiers", [
        "Nexora University awards Merit Scholarships at the end of each academic year based on CGPA performance. Scholarships are credited directly to the student's fee account for the next academic year.",
    ])
    e += [tbl(["Scholarship","CGPA Requirement","Annual Award","Eligible Programmes"],
              [["Chancellor's Gold Award","CGPA ≥ 9.5","100% Tuition Fee Waiver","All programmes"],
               ["Vice-Chancellor's Silver Award","CGPA 9.0–9.49","50% Tuition Fee Waiver","All programmes"],
               ["Dean's Merit Award","CGPA 8.5–8.99","25% Tuition Fee Waiver","All programmes"],
               ["Department Topper Award","Rank 1 in department","₹50,000 cash prize","Per department"],
               ["Academic Excellence Award","Top 5% of class","₹25,000 cash prize","All programmes"]], widths=[5*cm,4.5*cm,4*cm,3*cm]), SP()]
    e += sub("1.2 First-Year Admission Scholarship", [
        "Students with exceptional entrance exam scores receive the following one-time scholarships at the time of admission, credited in the first semester fee.",
    ])
    e += [tbl(["Entrance Score","Scholarship Amount","Programme"],
              [["JEE Main ≥ 99 percentile","₹1,00,000","B.Tech"],
               ["JEE Main 95–98.99 percentile","₹50,000","B.Tech"],
               ["JEE Main 90–94.99 percentile","₹25,000","B.Tech"],
               ["NEXET ≥ 310/360 (Top 1%)","₹75,000","B.Tech / BCA"],
               ["GATE Score ≥ 700","Full fee waiver + stipend","M.Tech"]], widths=[6*cm,4.5*cm,6*cm]), SP()]
    e += [PB()]
    e += sec("2. Need-Based Financial Aid")
    e += sub("2.1 Economic Hardship Scholarship", [
        "Students from economically disadvantaged backgrounds whose family income falls below certain thresholds are eligible for partial fee waivers. Applications are reviewed by the Financial Aid Committee annually.",
    ])
    e += [tbl(["Annual Family Income","Aid Percentage","Maximum Aid (₹/year)"],
              [["Below ₹3 lakh","50% tuition fee waiver","₹92,500"],
               ["₹3 lakh – ₹5 lakh","35% tuition fee waiver","₹64,750"],
               ["₹5 lakh – ₹8 lakh","20% tuition fee waiver","₹37,000"],
               ["₹8 lakh – ₹12 lakh (EWS)","15% tuition fee waiver","₹27,750"]], widths=[5.5*cm,4.5*cm,6.5*cm]), SP()]
    e += sub("2.2 Emergency Financial Assistance", [
        "Students facing sudden financial crises (death of parent, natural disaster, medical emergency) may apply for emergency financial assistance of up to ₹50,000 as an interest-free loan, repayable over 12 months post-graduation.",
    ])
    e += [PB()]
    e += sec("3. Government Scholarships")
    e += sub("3.1 State Government Scholarships (Telangana)", [
        "Multiple state government scholarship schemes are available for students from Telangana. The university's Scholarship Cell assists students in applying, verifying documents, and tracking disbursements.",
    ])
    e += [tbl(["Scheme Name","Eligibility","Annual Amount","Portal"],
              [["TS Post-Matric Scholarship","SC/ST students TS domicile","Full fee + maintenance","epass.telangana.gov.in"],
               ["EBC Scholarship","OBC/EBC students","Partial fee reimbursement","epass.telangana.gov.in"],
               ["Kalyani Scholarship","Unmarried girls TS domicile","₹30,000/year","TS Women Welfare"],
               ["Aarohi Scheme","Girls in STEM fields","₹20,000/year","TS DOST portal"],
               ["Minorities Scholarship","Muslim/Christian/Sikh minority","₹25,000/year","Minority Welfare Dept"]], widths=[4.5*cm,4*cm,3.5*cm,4.5*cm]), SP()]
    e += sub("3.2 National Scholarships", [
        "Central Government scholarship schemes applicable to Nexora students include the National Scholarship Portal (NSP) schemes and the AICTE scholarships for technical education students.",
    ])
    e += [tbl(["Scheme","Eligibility","Amount","Portal"],
              [["NSP Post-Matric (Central)","SC/ST all states","Full fee reimbursement","scholarships.gov.in"],
               ["AICTE Pragati Scholarship","Girl students in AICTE programmes","₹50,000/year","scholarships.gov.in"],
               ["AICTE Saksham Scholarship","Differently-abled students","₹50,000/year","scholarships.gov.in"],
               ["PM Scholarship (WARB)","Wards of defence/police personnel","₹25,000/year","ksb.gov.in"],
               ["Inspire Scholarship (DST)","Top 1% in Class 12","₹80,000/year + mentorship","online-inspire.gov.in"]], widths=[4.5*cm,4*cm,3.5*cm,4.5*cm]), SP()]
    e += [PB()]
    e += sec("4. Corporate & External Scholarships")
    e += [tbl(["Company/Foundation","Programme Name","Amount","Target Group"],
              [["Tata Trusts","Tata Scholar Programme","Up to ₹2 lakh/year","Meritorious needy students"],
               ["Infosys Foundation","Infosys Scholarship","₹1.5 lakh/year","Women in STEM"],
               ["Google India","Generation Google Scholarship","₹75,000 (one-time)","CS/IT women"],
               ["Microsoft India","Microsoft Scholarship","₹60,000 (one-time)","Engineering students"],
               ["Reliance Foundation","Reliance Scholarship","₹4 lakh/year","Top technical students"]], widths=[4.5*cm,4*cm,3.5*cm,4.5*cm]), SP()]
    e += [PB()]
    e += sec("5. Scholarship Application Process")
    e += [tbl(["Step","Action","Deadline","Mode"],
              [["1","Download application from portal or Scholarship Cell","1 August 2026","Online/Physical"],
               ["2","Collect required documents (income cert, marksheets)","15 August 2026","Physical"],
               ["3","Submit to Scholarship Cell with HOD recommendation","31 August 2026","Physical"],
               ["4","Verification and interview (if required)","September 2026","Campus"],
               ["5","Award notification","1 October 2026","Portal + Email"],
               ["6","Scholarship credit to fee account","15 October 2026","Automatic"]], widths=[1.5*cm,5.5*cm,4*cm,5.5*cm]), SP()]
    e += [PB()]
    e += sec("6. FAQs – Scholarships")
    e += faq([
        ("Can I receive multiple scholarships simultaneously?",
         "You may receive one university scholarship AND one government scholarship simultaneously. However, no two university merit scholarships can be combined. External corporate scholarships can be added regardless."),
        ("Is there a bond attached to scholarship recipients?",
         "No bond is required for merit or need-based scholarships. However, students receiving the Chancellor's Gold Award are expected to maintain CGPA ≥ 9.5 and serve as peer mentors for 2 hours per week."),
        ("What documents are needed for government scholarship renewal?",
         "Annual renewal requires: Marksheet of previous year, Income certificate (current year), Bonafide certificate, Bank passbook copy, Aadhaar card, and Caste certificate (one-time)."),
        ("Can a student apply for scholarship mid-semester?",
         "Government scholarships may accept applications up to 60 days after semester start as per NSP guidelines. University scholarships are processed once per year in August."),
    ])
    build("Scholarships_Financial_Aid_2026.pdf", e, "Scholarships & Financial Aid")

# ═══════════════════════════════════════════════════════════════════════════
# PDF 7 – Course Catalog & Programmes
# ═══════════════════════════════════════════════════════════════════════════
def pdf_07():
    e = cover("Course Catalog & Programme Guide","Detailed Curriculum for All Programmes 2026-27","Academics")
    e += toc([("1","B.Tech CSE Programme"),("2","B.Tech AI & Data Science"),("3","B.Tech ECE"),
               ("4","MBA Programme"),("5","M.Tech CSE / AI&ML"),("6","BCA / BBA"),("7","Elective Catalogue"),("8","FAQs")])
    e += sec("1. B.Tech Computer Science Engineering (CSE)")
    e += sub("1.1 Programme Overview", [
        "The B.Tech CSE programme is a 4-year, 8-semester degree programme with 160 credits. The curriculum is designed by an Academic Advisory Board comprising faculty from IIT, industry leaders from Google, Microsoft, and Amazon, and AICTE-nominated members.",
        "The programme emphasises: strong foundations in algorithms and systems, project-based learning from semester 2, mandatory industry internship, and specialisation electives in AI/ML, cybersecurity, cloud computing, and full-stack development.",
    ])
    e += sub("1.2 Semester-Wise Credit Distribution", [])
    e += [tbl(["Semester","Theory Courses","Lab","Credits","Key Subjects"],
              [["I","4","2","22","Mathematics I, Programming in C, Digital Logic, Physics"],
               ["II","4","2","22","Mathematics II, Data Structures, OOP in C++, Basic Electronics"],
               ["III","4","2","22","Algorithms, DBMS, Computer Organisation, Discrete Maths"],
               ["IV","4","2","22","OS, Computer Networks, Software Engineering, Probability"],
               ["V","3+2E","2","22","Compiler Design, ML Basics, Web Dev, Elective I & II"],
               ["VI","2+3E","2","22","Cloud Computing, Big Data, Elective III, IV, V"],
               ["VII","1+3E","Project","20","Internship (8 weeks), Elective VI, Project Phase I"],
               ["VIII","–","Project","8","Project Phase II, Seminar, Viva"]], widths=[2*cm,4*cm,2.5*cm,2.5*cm,5.5*cm]), SP()]
    e += [PB()]
    e += sec("2. B.Tech CSE (Artificial Intelligence & Data Science)")
    e += sub("2.1 Programme Overview", [
        "AI&DS is a specialised B.Tech programme launched in 2023, designed in collaboration with NVIDIA, Intel, and the IIIT Hyderabad AI Lab. The curriculum focuses on machine learning, deep learning, NLP, computer vision, and big data analytics.",
    ])
    e += [tbl(["Semester","Key Focus Areas","Notable Courses"],
              [["I-II","Foundations","Linear Algebra, Statistics, Python for AI, Introduction to ML"],
               ["III-IV","Core ML","Supervised/Unsupervised Learning, Neural Networks, Feature Engineering"],
               ["V-VI","Deep Learning","CNNs, RNNs, Transformers, NLP, Computer Vision"],
               ["VII-VIII","Applied AI","MLOps, LLMs, Generative AI, Capstone Project"]], widths=[2.5*cm,4.5*cm,9.5*cm]), SP()]
    e += [PB()]
    e += sec("3. B.Tech Electronics & Communication Engineering (ECE)")
    e += sub("3.1 Programme Overview", [
        "The ECE programme covers analog and digital electronics, VLSI design, signal processing, embedded systems, communication systems, and IoT. Students have access to the Nexora Embedded Systems Lab and the RF Communications Lab.",
    ])
    e += [tbl(["Year","Key Subjects","Labs"],
              [["1st Year","Engineering Maths, Basic Electronics, Circuit Theory","Basic Electronics Lab, Programming Lab"],
               ["2nd Year","Analog/Digital Electronics, Signals & Systems, Microprocessors","Analog Circuits Lab, Digital Lab"],
               ["3rd Year","VLSI Design, Communication Systems, Embedded Systems","VLSI Lab, DSP Lab, Embedded Lab"],
               ["4th Year","5G/IoT, Advanced DSP, Electives, Capstone Project","Research Lab, Project Lab"]], widths=[2.5*cm,7*cm,7*cm]), SP()]
    e += [PB()]
    e += sec("4. MBA Programme Overview")
    e += sub("4.1 MBA Specialisations", [
        "The MBA programme at Nexora Business School offers 4 dual specialisations. Students choose 2 specialisations in Semester 3 based on merit and interest.",
    ])
    e += [tbl(["Specialisation","Core Areas","Industry Partners","Avg Placement CTC"],
              [["Finance & Banking","Investment, Risk, Corporate Finance","ICICI, HDFC, Kotak","₹12.5 LPA"],
               ["Marketing & Brand","Digital Marketing, Consumer Behaviour, Analytics","HUL, ITC, Zomato","₹10.8 LPA"],
               ["Operations & SCM","Supply Chain, Lean, ERP, Logistics","Amazon, DHL, TCS","₹11.2 LPA"],
               ["Human Resources","Talent Management, OB, Labour Laws, HRTech","Deloitte, ADP, SAP","₹10.5 LPA"],
               ["Business Analytics","Data Analysis, Tableau, Python, Business Intelligence","TCS, Mu Sigma","₹14.0 LPA"]], widths=[4*cm,5*cm,4*cm,3.5*cm]), SP()]
    e += sub("4.2 MBA Programme Structure", [
        "Semester 1-2: Core management courses (Marketing, Finance, HR, Operations, Statistics, IT). Semester 3-4: Specialisation courses + industry projects + live consulting assignments. Summer Internship: Between Semester 2 and 3 (8-10 weeks, mandatory).",
    ])
    e += [PB()]
    e += sec("5. Available Elective Catalogue")
    e += [tbl(["Elective Course","Programme","Credits","Prerequisites"],
              [["Deep Learning & Neural Networks","B.Tech CSE/AI&DS","3","Machine Learning"],
               ["Cybersecurity & Ethical Hacking","B.Tech CSE","3","Computer Networks, OS"],
               ["Cloud Architecture (AWS/Azure)","B.Tech CSE","3","Networking Basics"],
               ["Blockchain Technology","B.Tech CSE/MBA","3","Distributed Systems"],
               ["Natural Language Processing","B.Tech AI&DS","3","ML, Python"],
               ["IoT & Smart Systems","B.Tech ECE/CSE","3","Embedded Systems"],
               ["Quantum Computing Basics","B.Tech CSE (Optional)","2","Linear Algebra, Algorithms"],
               ["Business Analytics with Python","MBA","3","Statistics, Python Basics"],
               ["Competitive Programming","B.Tech CSE","2","Algorithms (Grade B+)"],
               ["Research Methodology & Writing","All PG","2","None"]], widths=[5.5*cm,4*cm,2.5*cm,5*cm]), SP()]
    e += [PB()]
    e += sec("6. FAQs – Courses & Curriculum")
    e += faq([
        ("Can I take electives from other departments?",
         "Yes. Inter-departmental electives are permitted for up to 2 elective slots per semester, subject to seat availability and HOD approval. Cross-department electives carry the same credits."),
        ("Is there an honours programme?",
         "Yes. Students with CGPA ≥ 8.0 may opt for an Honours programme by completing 20 additional credits in advanced electives and an independent research project. The degree will carry a 'with Honours' distinction."),
        ("When is the specialisation selection for MBA?",
         "MBA students choose specialisations during an Elective Declaration process conducted in the 3rd week of Semester 2. Career counselling sessions are arranged prior to selection."),
    ])
    build("Course_Catalog_and_Programs.pdf", e, "Course Catalog & Programmes 2026-27")


# ═══════════════════════════════════════════════════════════════════════════
# PDF 8 – Academic Calendar 2026
# ═══════════════════════════════════════════════════════════════════════════
def pdf_08():
    e = cover("Academic Calendar 2026-2027","Official Schedule: Classes, Exams, Holidays & Events","Academics")
    e += toc([("1","Odd Semester Calendar (Jul–Dec 2026)"),("2","Even Semester Calendar (Jan–May 2027)"),
               ("3","Public Holidays"),("4","Important Deadlines"),("5","Annual Events Calendar")])
    e += sec("1. Odd Semester 2026 (July – December)")
    e += [tbl(["Date","Event","Category"],
              [["25 July 2026","Classes commence – Odd Semester 2026","Academic"],
               ["1 August 2026","Last date for admission / lateral entry","Admissions"],
               ["15 August 2026","Independence Day – Holiday","Holiday"],
               ["31 August 2026","Last date for course add/drop requests","Academic"],
               ["2 September 2026","Onam (Telangana gazetted holiday)","Holiday"],
               ["14 September 2026","Internal Assessment 1 – All Programmes","Examinations"],
               ["2 October 2026","Gandhi Jayanti – Holiday","Holiday"],
               ["10–20 October 2026","Cultural & Technical Fest 'NEXFEST 2026'","Events"],
               ["24 October 2026","Dussehra – Holiday","Holiday"],
               ["1 November 2026","Telangana Formation Day – Holiday","Holiday"],
               ["8 November 2026","Internal Assessment 2 – All Programmes","Examinations"],
               ["12 November 2026","Diwali – Holiday (2 days)","Holiday"],
               ["21 November 2026","Last Teaching Day – Odd Semester","Academic"],
               ["22–28 November 2026","Practical / Lab Examinations","Examinations"],
               ["29 November – 16 Dec 2026","End-Semester Theory Examinations","Examinations"],
               ["25 December 2026","Christmas – Holiday","Holiday"],
               ["5 January 2027","Odd Semester Results Published","Academic"]], widths=[4*cm,9*cm,3.5*cm]), SP()]
    e += [PB()]
    e += sec("2. Even Semester 2027 (January – May)")
    e += [tbl(["Date","Event","Category"],
              [["2 January 2027","Classes commence – Even Semester 2027","Academic"],
               ["14 January 2027","Sankranti – Holiday (2 days)","Holiday"],
               ["26 January 2027","Republic Day – Holiday","Holiday"],
               ["12 February 2027","Last date for supplementary exam registration","Academic"],
               ["18 February 2027","Internal Assessment 1 – Even Semester","Examinations"],
               ["10 March 2027","Holi – Holiday","Holiday"],
               ["14 April 2027","Dr Ambedkar Jayanti / Ugadi – Holiday","Holiday"],
               ["14 April 2027","Internal Assessment 2 – Even Semester","Examinations"],
               ["1 May 2027","Labour Day / Maharashtra Day – Holiday","Holiday"],
               ["7 May 2027","Last Teaching Day – Even Semester","Academic"],
               ["8–14 May 2027","Practical / Lab Examinations","Examinations"],
               ["15–30 May 2027","End-Semester Theory Examinations","Examinations"],
               ["20 June 2027","Even Semester Results Published","Academic"],
               ["20–30 June 2027","Convocation 2027 (Tentative)","Events"]], widths=[4*cm,9*cm,3.5*cm]), SP()]
    e += [PB()]
    e += sec("3. Annual Events Calendar")
    e += [tbl(["Event","Month","Description"],
              [["NEXFEST – Annual Fest","October","3-day cultural, technical, and startup fest. 10,000+ participants"],
               ["Sports Week","February","Inter-department sports tournament: cricket, football, badminton, chess"],
               ["Industry-Academia Summit","November","2-day summit with 50+ industry leaders as speakers"],
               ["Hackathon 2026 (36-hr)","September","Pan-India hackathon. Prizes worth ₹10 lakh"],
               ["Alumni Meet","March","Annual gathering of 5,000+ alumni. Placement networking"],
               ["Research Symposium","April","Student research paper presentations. Best paper awards"],
               ["Farewell & Convocation","June","Graduation ceremony for final year students"]], widths=[4.5*cm,3*cm,9*cm]), SP()]
    e += [PB()]
    e += sec("4. Important Deadlines Summary")
    e += [tbl(["Activity","Deadline","Mode"],
              [["Fee Payment – 1st Instalment","10 July 2026","Online"],
               ["Hostel Allotment Request","15 July 2026","Online portal"],
               ["Scholarship Application","31 August 2026","Physical / Online"],
               ["Internship Report Submission","10 August 2026","Portal"],
               ["Project Topic Registration (7th Sem)","15 August 2026","HOD approval"],
               ["Leave of Absence Application","7 days before absence","Warden + HOD"],
               ["Examination Form Submission","15 days before exam","Online"],
               ["Revaluation Request","10 days after result","Online + Fee"]], widths=[6*cm,4*cm,6.5*cm]), SP()]
    build("Academic_Calendar_2026.pdf", e, "Academic Calendar 2026-2027")

# ═══════════════════════════════════════════════════════════════════════════
# PDF 9 – Library Guide 2026
# ═══════════════════════════════════════════════════════════════════════════
def pdf_09():
    e = cover("Library Guide 2026","Central Library Services, Resources & Usage Policies","Library")
    e += toc([("1","Library Overview"),("2","Collections & Holdings"),("3","Library Timings"),
               ("4","Borrowing Rules"),("5","Digital Resources"),("6","Study Spaces"),
               ("7","Research Support"),("8","Fines & Penalties"),("9","FAQs")])
    e += sec("1. Library Overview","Nexora University Central Library – 2.5 Lakh volumes across 4 floors")
    e += sub("1.1 About the Library", [
        "The Nexora Central Library, spread across 25,000 sq.ft on 4 floors of the Academic Block, houses over 2.5 lakh books, 450+ national and international journal subscriptions, 80,000+ e-books, and 15 years of digital thesis and dissertation archives.",
        "The library is managed by a team of 18 qualified librarians and 12 support staff. It is a member of DELNET, INFLIBNET N-LIST, and IEEE Xplore Digital Library.",
    ])
    e += [tbl(["Floor","Section","Seating Capacity"],
              [["Ground Floor","Circulation Desk, New Arrivals, Newspapers & Magazines, General Reference","120 seats"],
               ["First Floor","Engineering & Technology, Science & Maths, Project Archives","200 seats"],
               ["Second Floor","Management, Humanities, Language Lab, Group Study Rooms","180 seats"],
               ["Third Floor","Digital Resource Centre, Thesis Repository, Research Lab, OPAC Terminals","100 seats"]], widths=[2.5*cm,10*cm,3.5*cm]), SP()]
    e += [PB()]
    e += sec("2. Library Timings")
    e += [tbl(["Day","Timings","Remarks"],
              [["Monday – Friday","7:30 AM – 10:00 PM","Full services available"],
               ["Saturday","8:00 AM – 6:00 PM","Issue/Return only till 4 PM"],
               ["Sunday","10:00 AM – 4:00 PM","Reading room only"],
               ["Public Holidays","Closed","Emergency reading room access on request"],
               ["Exam Period (Theory)","7:30 AM – 11:30 PM","Extended hours"],
               ["Summer / Semester Break","9:00 AM – 5:00 PM","Limited staff"]], widths=[4.5*cm,5*cm,7*cm]), SP()]
    e += [PB()]
    e += sec("3. Borrowing Privileges")
    e += [tbl(["Category","Books Allowed","Loan Period","Renewal"],
              [["UG Student","4 books","14 days","1 renewal × 14 days"],
               ["PG Student","6 books","21 days","2 renewals × 14 days each"],
               ["Ph.D Scholar","8 books","30 days","3 renewals × 30 days each"],
               ["Faculty","12 books","90 days","3 renewals × 30 days each"],
               ["Visiting Faculty","4 books","14 days","1 renewal"],
               ["Staff","3 books","14 days","1 renewal"]], widths=[4*cm,3.5*cm,3.5*cm,5.5*cm]), SP()]
    e += sub("3.1 Borrowing Rules", [
        "Books must be borrowed by physically presenting the University ID card at the Circulation Desk. Online reservations may be placed through the OPAC portal (library.nexorauniversity.edu) 24 hours in advance.",
        "Reference books, rare documents, dissertations, and current journals are 'Read Only' and cannot be borrowed.",
        "Lost books must be reported to the Circulation Desk immediately. The borrower is responsible for paying the current market price of the book plus a ₹200 processing charge.",
    ])
    e += [PB()]
    e += sec("4. Digital Library Resources")
    e += [tbl(["Database / Resource","Coverage","Access Mode"],
              [["IEEE Xplore","500,000+ engineering papers","On-campus + VPN (off-campus)"],
               ["EBSCO Business Source","Management & Finance journals","On-campus + VPN"],
               ["Springer Link","Science, Tech, Med journals","On-campus + VPN"],
               ["JSTOR","Humanities & Social Sciences archive","On-campus only"],
               ["INFLIBNET N-LIST","6,000+ e-journals, 300,000+ e-books","Student credentials"],
               ["ACM Digital Library","Computer Science research","On-campus + VPN"],
               ["ScienceDirect (Elsevier)","Engineering & Science","On-campus + VPN"],
               ["Nexora Thesis Repository","All Nexora theses 2010–present","Open access (internal)"]], widths=[4.5*cm,5*cm,6.5*cm]), SP()]
    e += sub("4.1 Remote Access", [
        "Students and faculty may access all licensed databases off-campus via the Nexora VPN. VPN credentials are issued by the IT Department. Contact it.helpdesk@nexorauniversity.edu for VPN setup instructions.",
    ])
    e += [PB()]
    e += sec("5. Study Spaces & Facilities")
    e += bul("5.1 Available Study Areas", [
        "Silent Reading Rooms: 3 dedicated silent zones with 200-seat capacity each",
        "Group Study Rooms: 8 air-conditioned rooms (6 seats each), bookable online up to 24 hours in advance",
        "Research Workstations: 30 dedicated PC workstations with MS Office, MATLAB, Python, and statistical software",
        "Discussion Booths: 12 semi-enclosed pods for group discussions",
        "Thesis Writing Centre: 20-seat room with specialised academic writing software and dissertation templates",
        "Newspaper & Magazine Reading Corner: 80+ national and state dailies, 60+ popular magazines",
    ])
    e += [PB()]
    e += sec("6. Fines & Penalty Chart")
    e += [tbl(["Offence","Fine"],
              [["Overdue book return","₹10 per day per book (from due date)"],
               ["Damage to book (minor – torn page, mark)","₹200 flat + cost of repair"],
               ["Damage to book (severe – missing pages)","Full replacement cost + ₹200"],
               ["Loss of book","Replacement cost at current market price + ₹200"],
               ["Loss of library ID card","₹200 for duplicate"],
               ["Unauthorised removal of library material","₹1,000 + academic warning"],
               ["Using mobile/eating in silent zone","₹100 per incident"],
               ["Non-return of borrowed items at semester end","Library clearance withheld"]], widths=[7*cm,9.5*cm]), SP()]
    e += [PB()]
    e += sec("7. FAQs – Library")
    e += faq([
        ("How do I access the library portal?","Visit library.nexorauniversity.edu. Login with your student roll number and password (default: date of birth in DDMMYYYY format). First-time users must change the default password."),
        ("Can I extend the borrowing period online?","Yes. Books can be renewed online via the library portal up to 24 hours before the due date, provided no reservation request has been placed by another user."),
        ("Is inter-library loan available?","Yes. Through DELNET membership, Nexora students can request books and articles from partner institutions across India. Delivery takes 5-7 working days. Submit requests at the Reference Desk."),
        ("What is the printing/scanning policy?","Black-and-white printing costs ₹2 per page. Colour printing: ₹10 per page. Scanning is free. A prepaid printing card of ₹100 minimum is required."),
    ])
    build("Library_Guide_2026.pdf", e, "Library Guide 2026")

# ═══════════════════════════════════════════════════════════════════════════
# PDF 10 – Transport & Commute Guide
# ═══════════════════════════════════════════════════════════════════════════
def pdf_10():
    e = cover("Transport & Commute Guide","University Bus Routes, Timings & Travel Policies","Transport")
    e += toc([("1","Transport Overview"),("2","Bus Routes & Timings"),("3","Fee Schedule"),
               ("4","Student Transport Card"),("5","Rules & Conduct"),("6","Special Services"),("7","FAQs")])
    e += sec("1. Transport Overview")
    e += sub("1.1 Fleet Details", [
        "Nexora University operates a fleet of 42 AC and non-AC buses covering 28 routes across Greater Hyderabad, Secunderabad, Cyberabad, and surrounding districts. All buses are GPS-tracked and monitored via the Nexora Transport Management System.",
        "The transport office is located at the Main Gate and operates from 7:00 AM to 8:00 PM. Online queries: transport@nexorauniversity.edu | Helpline: +91-40-4567-8930",
    ])
    e += [tbl(["Fleet Category","Count","Capacity","AC"],
              [["Full-Size Bus (Volvo/Tata)","28","52 seats","Yes (18 buses)"],
               ["Mini Bus","10","35 seats","Yes (4 buses)"],
               ["Staff Shuttle","4","20 seats","Yes"]], widths=[5.5*cm,2.5*cm,3.5*cm,5*cm]), SP()]
    e += [PB()]
    e += sec("2. Bus Routes & Timings")
    e += sub("2.1 Major Bus Routes – Pickup & Drop Timings", [
        "All routes operate 6 days a week (Monday to Saturday). Sunday service is available only on exam days with advance booking.",
    ])
    e += [tbl(["Route No.","Origin – Destination","Key Stops","Morning Pickup","Evening Drop"],
              [["R01","Secunderabad Rly Stn – Campus","Paradise, Begumpet, ECIL","7:00 AM","6:15 PM"],
               ["R02","Kukatpally – Campus","KPHB, Miyapur, Chandanagar","7:10 AM","6:20 PM"],
               ["R03","Dilsukhnagar – Campus","LB Nagar, Nagole, Uppal","7:05 AM","6:10 PM"],
               ["R04","Madinaguda – Campus","Patancheru, Tellapur, Biodiversity","7:15 AM","6:25 PM"],
               ["R05","Ameerpet – Campus","SR Nagar, Balanagar, Moosapet","7:08 AM","6:18 PM"],
               ["R06","Shamshabad – Campus","Rajendranagar, Attapur, Mehdipatnam","7:20 AM","6:30 PM"],
               ["R07","Quthbullapur – Campus","Jeedimetla, Balanagar","7:05 AM","6:15 PM"],
               ["R08","Malkajgiri – Campus","ECIL X Road, Sainikpuri","7:00 AM","6:10 PM"],
               ["R09","Kompally – Campus","Gundlapochampally, Medchal Road","7:25 AM","6:35 PM"],
               ["R10","LB Nagar – Campus","Vanasthalipuram, Nacharam","7:03 AM","6:13 PM"]], widths=[2*cm,5*cm,5*cm,2.5*cm,2.5*cm]), SP()]
    e += [PB()]
    e += sec("3. Transport Fee Schedule 2026-27")
    e += [tbl(["Distance from Campus","Annual Fee (Non-AC)","Annual Fee (AC)","Semester Fee"],
              [["0–15 km","₹18,000","₹24,000","50% per semester"],
               ["15–25 km","₹22,000","₹29,000","50% per semester"],
               ["25–35 km","₹26,000","₹34,000","50% per semester"],
               ["35–50 km","₹30,000","₹38,000","50% per semester"],
               ["> 50 km","₹35,000","₹44,000","50% per semester"]], widths=[4.5*cm,4*cm,4*cm,4*cm]), SP()]
    e += sub("3.1 Fee Payment & Refund", [
        "Transport fees are payable at the beginning of each semester. Fee once paid is non-refundable except in cases of discontinuation of the bus route by the university, in which case a proportional refund is issued.",
        "Students who vacate hostel mid-semester and require transport may register at the Transport Office by paying a prorated fee.",
    ])
    e += [PB()]
    e += sec("4. Student Transport Card")
    e += sub("4.1 Transport Pass", [
        "All registered bus users are issued a University Transport Card (UTC) with RFID chip. The UTC must be scanned at the bus entry point. Entry without a valid UTC may result in denial of service.",
        "Lost UTC must be reported within 24 hours. Replacement card issued at ₹150 within 3 working days.",
    ])
    e += bul("4.2 Card Features", [
        "RFID-based automated attendance tracking for bus usage",
        "Emergency contact stored on card for accident/medical situations",
        "Linked to parent notification system — SMS alert on boarding/alighting",
        "Valid for one academic year; renewed free of cost upon fee payment",
    ])
    e += [PB()]
    e += sec("5. Rules & Code of Conduct")
    e += bul("5.1 Student Conduct in University Bus", [
        "Students must carry their Transport Card and University ID at all times while commuting.",
        "Seats are not reserved. No student may 'block' seats with bags.",
        "No loud music, video calls on speakerphone, or consumption of food items in buses.",
        "Smoking, alcohol, and chewing tobacco are strictly prohibited.",
        "In case of bus breakdown, students must wait at the nearest designated stop. Alternate arrangements are communicated via WhatsApp transport group.",
        "Eve-teasing, ragging, or misconduct in buses will result in immediate suspension of transport privileges and disciplinary action.",
    ])
    e += [PB()]
    e += sec("6. Special & Emergency Services")
    e += [tbl(["Service","Availability","Booking","Cost"],
              [["Examination Day Special Bus","All exam days including Sunday","Transport portal or office","Included in transport pass"],
               ["Night Return (after events/fests)","Event days – up to 11:30 PM","Transport office 48 hrs prior","₹150 per trip"],
               ["Medical Emergency Pickup","24/7","Security + Transport Helpline","Free (emergency)"],
               ["Outstation Day Trip (educational)","On request","5 days advance, HOD approval","Actuals collected"]], widths=[4.5*cm,4*cm,4*cm,4*cm]), SP()]
    e += faq([
        ("What if I miss my bus?","Contact the Transport Helpline. If you have missed your bus by less than 30 minutes, request the next available route. Nexora is not liable for individual delays caused by traffic or personal reasons."),
        ("Can I board from any stop on the route?","Yes, you may board from any stop listed on your registered route. Boarding from a different route requires a temporary route change request at the Transport Office."),
        ("What is the procedure for annual renewal of the transport pass?","Pay the transport fee for the new academic year via the student portal. The UTC is automatically activated for the new year. Physically visit the Transport Office only if you need a new card."),
    ])
    build("Transport_Guide_2026.pdf", e, "Transport & Commute Guide 2026")


# ═══════════════════════════════════════════════════════════════════════════
# PDF 11 – Research & Innovation Handbook
# ═══════════════════════════════════════════════════════════════════════════
def pdf_11():
    e = cover("Research & Innovation Handbook","PhD, Research Projects, Patents & Startup Incubation","Research")
    e += toc([("1","Research Overview"),("2","PhD Programme"),("3","Research Centres"),
               ("4","Funded Projects"),("5","Patent & Publication Policy"),("6","Startup Incubation"),("7","FAQs")])
    e += sec("1. Research Overview", "9 research centres | ₹48 crore funded projects | 312 patents filed")
    e += sub("1.1 Research Highlights 2025-26", [
        "Nexora University has established itself as a research-intensive institution with 9 dedicated research centres, ₹48 crore in active funded projects from DST, DRDO, AICTE, and industry partners.",
        "In 2025-26, Nexora faculty published 420+ research papers in Scopus-indexed journals, filed 38 new patents (22 granted), and launched 3 spin-off startups through the NEXHUB incubator.",
    ])
    e += [tbl(["Metric","2025-26","2024-25"],
              [["Scopus Publications","420","380"],
               ["Patents Filed","38","29"],
               ["Patents Granted","22","18"],
               ["Funded Projects (Active)","62","54"],
               ["Total Research Funding (₹ Crore)","48.2","39.6"],
               ["PhD Scholars Enrolled","312","284"],
               ["PhD Degrees Awarded","78","62"]], widths=[6*cm,3.5*cm,3.5*cm]), SP()]
    e += [PB()]
    e += sec("2. PhD Programme")
    e += sub("2.1 Eligibility & Admission", [
        "PhD admission is conducted twice a year (August and February intake). Eligible candidates: M.Tech/M.E. with 55% or M.Sc/MBA/MCA with 55% + valid GATE/UGC-NET/Nexora Research Aptitude Test (NEXRAT) score.",
    ])
    e += [tbl(["Programme","Duration","Stipend","Eligibility"],
              [["Ph.D (Funded JRF)","Min 3, Max 6 years","₹31,000–₹35,000/month","GATE/NET + Interview"],
               ["Ph.D (Self-Funded)","Min 3, Max 7 years","None","55%+ PG + NEXRAT"],
               ["Ph.D (Part-Time / Industry)","Min 4, Max 8 years","None","Industry experience 2+ years"],
               ["Ph.D (Collaborative – IIT/NIT)","Min 3, Max 6 years","₹31,000/month","Supervisor approval"]], widths=[4.5*cm,3*cm,4*cm,5*cm]), SP()]
    e += [PB()]
    e += sec("3. Research Centres")
    e += [tbl(["Centre","Focus Area","Faculty Strength","Active Projects"],
              [["Centre for AI & Machine Learning (CAML)","Deep Learning, NLP, Computer Vision","12 faculty","18 projects"],
               ["Nexora Cybersecurity Lab (NCL)","Network Security, Blockchain, Cryptography","8 faculty","9 projects"],
               ["Advanced Materials Research Centre","Nanomaterials, Composites, Smart Materials","10 faculty","12 projects"],
               ["IoT & Embedded Systems Lab","Smart Cities, Agriculture IoT, Industrial IoT","7 faculty","8 projects"],
               ["Centre for Data Science (CDS)","Big Data, Analytics, Bioinformatics","9 faculty","11 projects"],
               ["Green Energy Research Lab","Solar, Wind, EV Battery Tech","6 faculty","7 projects"],
               ["Business Innovation Lab (BIL)","FinTech, Supply Chain Innovation, Digital Commerce","8 faculty","6 projects"],
               ["Health Informatics Centre","Medical AI, Drug Discovery, Remote Health","5 faculty","5 projects"],
               ["VLSI & Semiconductor Lab","Chip Design, RF Circuits, Photonics","7 faculty","6 projects"]], widths=[5*cm,5.5*cm,3*cm,2.5*cm]), SP()]
    e += [PB()]
    e += sec("4. Patent & Publication Policy")
    e += sub("4.1 University Patent Policy", [
        "Any invention arising from research conducted using university resources, facilities, or funding is jointly owned by the inventor(s) and Nexora University. Revenue from commercialised patents is shared as: 60% inventor(s), 25% department, 15% university.",
    ])
    e += [tbl(["Stage","Nexora Role","Inventor Share","Timeline"],
              [["Invention Disclosure","University evaluates IP potential","Full rights to inventor initially","Within 30 days of disclosure"],
               ["Patent Filing","University funds Indian patent filing","60% inventor, 40% university","6–12 months"],
               ["International Patent","University + DST/BIRAC funding","60% inventor, 40% university","12–24 months after Indian"],
               ["Commercialisation","Technology Transfer Office handles licensing","60% inventor, 40% university","Post-grant"]], widths=[3*cm,5*cm,4*cm,4.5*cm]), SP()]
    e += [PB()]
    e += sec("5. NEXHUB – Startup Incubation Centre")
    e += sub("5.1 About NEXHUB", [
        "NEXHUB is Nexora's flagship entrepreneurship incubation centre established in 2019 with MSME and DPIIT recognition. It has incubated 47 startups, of which 12 are funded (total funding raised: ₹38 crore).",
    ])
    e += bul("5.2 NEXHUB Support Services", [
        "Free workspace (desks, meeting rooms, high-speed internet) for 12 months",
        "Seed funding of up to ₹5 lakh from NEXHUB Innovation Fund",
        "Access to ₹50 lakh MSME grant linkages and DST NIDHI scheme",
        "Mentorship from 80+ active entrepreneurs, VCs, and CXOs",
        "Legal, IP, accounting, and incorporation support",
        "Industry connections, pilot programme facilitation",
        "Annual NEXHUB Demo Day: pitch to 100+ investors",
    ])
    e += faq([
        ("Can undergraduate students apply for NEXHUB incubation?","Yes, students from 2nd year onwards are eligible. A faculty mentor must co-sign the application. Selected teams get a 6-month pre-incubation track before full incubation."),
        ("Is the research stipend taxable?","JRF/SRF stipends are exempt from income tax as per CBDT circular. However, industry-sponsored fellowships above ₹7 lakh/year may be taxable. Students are advised to consult the Finance Office."),
    ])
    build("Research_Innovation_Handbook.pdf", e, "Research & Innovation Handbook")

# ═══════════════════════════════════════════════════════════════════════════
# PDF 12 – Department Handbook: CSE
# ═══════════════════════════════════════════════════════════════════════════
def pdf_12():
    e = cover("Department of Computer Science & Engineering","Faculty, Labs, Research Areas & Student Opportunities","Departments")
    e += toc([("1","Department Overview"),("2","Faculty Directory"),("3","Labs & Infrastructure"),
               ("4","Research Groups"),("5","Student Clubs"),("6","Industry Collaborations"),("7","FAQs")])
    e += sec("1. Department Overview", "Established 1999 | NBA Accredited | 60+ Faculty | 1,200 Students")
    e += sub("1.1 About the Department", [
        "The Department of Computer Science & Engineering (CSE) at Nexora University is one of the largest and most sought-after departments with an annual intake of 240 UG students and 120 PG students.",
        "The department has been consistently ranked among the top 20 CSE departments in India (NIRF 2025) and is NBA-accredited. It houses 14 state-of-the-art laboratories, 4 active research centres, and has placed students at Google, Microsoft, Amazon, and 300+ other companies.",
    ])
    e += [PB()]
    e += sec("2. Faculty Directory")
    e += sub("2.1 Department Administration", [])
    e += [tbl(["Position","Name","Qualification","Email","Office"],
              [["Head of Department","Prof. Dr. Rajesh Kumar","Ph.D (IIT Delhi), B.Tech (NIT Warangal)","hod.cse@nexorauniversity.edu","Room 101, CSE Block"],
               ["Associate HOD","Dr. Priya Sharma","Ph.D (IIIT-H), M.Tech (NIT Trichy)","assoc.hod.cse@nexorauniversity.edu","Room 102, CSE Block"],
               ["Programme Coordinator (B.Tech)","Dr. Anil Verma","Ph.D (BITS Pilani)","coord.btech.cse@nexorauniversity.edu","Room 103"],
               ["Programme Coordinator (M.Tech)","Dr. Kavita Rao","Ph.D (IISc Bangalore)","coord.mtech.cse@nexorauniversity.edu","Room 104"]], widths=[3.5*cm,3.5*cm,4.5*cm,4.5*cm,3*cm]), SP()]
    e += sub("2.2 Senior Faculty", [])
    e += [tbl(["Name","Specialisation","Qualification","Office Hours","Cabin"],
              [["Dr. Srinivas Reddy","Machine Learning, NLP","Ph.D IIT Madras","Mon-Wed 2-4 PM","CSE-201"],
               ["Dr. Meena Iyer","Algorithms, Competitive Programming","Ph.D CMU (USA)","Tue-Thu 11 AM-1 PM","CSE-202"],
               ["Dr. Aakash Patel","Cybersecurity, Cryptography","Ph.D IIT Bombay","Mon-Fri 10-11 AM","CSE-203"],
               ["Dr. Lalitha Murthy","Cloud Computing, Distributed Systems","Ph.D IISC","Wed-Fri 3-5 PM","CSE-204"],
               ["Dr. Ranjit Singh","Computer Vision, Deep Learning","Ph.D Stanford (USA)","Mon-Fri 11 AM-12 PM","CSE-205"],
               ["Prof. Deepika Joshi","Database Systems, Data Warehousing","M.Tech (Gold Medal) IIT Delhi","Tue-Thu 2-4 PM","CSE-206"],
               ["Dr. Harish Gupta","Compiler Design, Programming Languages","Ph.D IIT Kanpur","Mon-Wed 3-4 PM","CSE-207"],
               ["Dr. Sunita Kaur","Software Engineering, Agile Methods","Ph.D BITS Pilani","Tue-Fri 10-11 AM","CSE-208"]], widths=[4*cm,4.5*cm,4*cm,3.5*cm,1.5*cm]), SP()]
    e += [PB()]
    e += sec("3. Labs & Infrastructure")
    e += [tbl(["Lab Name","Capacity","Key Equipment / Software","Location"],
              [["Advanced Programming Lab","80 PCs","C, C++, Python, Java, VS Code, PyCharm","CSE Block, Floor 1"],
               ["AI & Machine Learning Lab","60 PCs + 8 GPUs","TensorFlow, PyTorch, Keras, Jupyter","CSE Block, Floor 2"],
               ["Cybersecurity Lab","40 PCs (isolated network)","Kali Linux, Wireshark, Metasploit, Snort","CSE Block, Floor 2"],
               ["Data Science Lab","60 PCs","Python, R, Tableau, Power BI, Spark","CSE Block, Floor 1"],
               ["Cloud & DevOps Lab","40 PCs","AWS Academy, Azure DevOps, Docker, Kubernetes","CSE Block, Floor 3"],
               ["Software Testing Lab","40 PCs","Selenium, JUnit, JIRA, Jenkins, Git","CSE Block, Floor 3"],
               ["DBMS Lab","50 PCs","Oracle 19c, MySQL, PostgreSQL, MongoDB","CSE Block, Floor 1"],
               ["Web Development Lab","60 PCs","HTML/CSS, React, Node.js, Django, Figma","CSE Block, Floor 2"],
               ["High-Performance Computing Lab","16-node cluster","MPI, OpenMP, CUDA","CSE Block, Floor 4"],
               ["NLP & Generative AI Lab","40 PCs + 4 GPUs (A100)","HuggingFace, LangChain, GPT APIs","CSE Block, Floor 4"]], widths=[4.5*cm,3.5*cm,5.5*cm,3*cm]), SP()]
    e += [PB()]
    e += sec("4. Student Clubs & Associations")
    e += [tbl(["Club Name","Focus","Key Activities","Contact"],
              [["CodeNexora","Competitive Programming","LeetCode contests, ICPC prep, weekly contests","codenexora@nexorauniversity.edu"],
               ["AI Society","AI/ML Research & Projects","Paper reading clubs, project showcases, Kaggle","aisociety@nexorauniversity.edu"],
               ["CyberCell","Cybersecurity & Ethical Hacking","CTF competitions, workshops, Bug Bounty guidance","cybercell@nexorauniversity.edu"],
               ["OpenSource Club","Open Source Contribution","Hacktoberfest, GSoC guidance, GitHub projects","opensource@nexorauniversity.edu"],
               ["Web Dev Society","Full Stack Development","Build-a-thons, portfolio reviews, freelancing","webdev@nexorauniversity.edu"]], widths=[3.5*cm,4*cm,5.5*cm,4*cm]), SP()]
    e += faq([
        ("How do I get a project guide in CSE?","Students in the 7th semester submit project topics to the programme coordinator by 15 August. Guides are assigned based on research area preference and faculty availability."),
        ("What is the procedure for external projects?","Students may pursue final-year projects at industry partner companies (Google, Microsoft, Infosys, etc.) with prior approval from the HOD and programme coordinator. A co-guide from the company is mandatory."),
        ("How can I contact the HOD?","Visit Room 101, CSE Block, or email hod.cse@nexorauniversity.edu. Walk-in office hours: Monday to Friday, 2:00 PM – 4:00 PM."),
    ])
    build("Department_Handbook_CSE.pdf", e, "Department Handbook: CSE")

# ═══════════════════════════════════════════════════════════════════════════
# PDF 13 – Student Handbook & Code of Conduct
# ═══════════════════════════════════════════════════════════════════════════
def pdf_13():
    e = cover("Student Handbook & Code of Conduct","Rights, Responsibilities, Disciplinary Policies & Student Life","General")
    e += toc([("1","Welcome Message"),("2","Student Rights & Responsibilities"),("3","Code of Conduct"),
               ("4","Anti-Ragging Policy"),("5","Sexual Harassment Policy (POSH)"),("6","Grievance Redressal"),
               ("7","Health & Wellness Services"),("8","Student Clubs & Activities"),("9","FAQs")])
    e += sec("1. Welcome Message from the Vice-Chancellor")
    e += [Paragraph(
        "Welcome to Nexora University. You have joined an institution that believes education is not just about acquiring knowledge — it is about building character, developing critical thinking, and preparing to contribute meaningfully to society. "
        "This handbook outlines the standards of behaviour, rights, and responsibilities that every Nexora student must be familiar with. We expect you to uphold the values of integrity, respect, and excellence in everything you do on campus.",
        ST["bd"]), SP()]
    e += [Paragraph("— Prof. Dr. Arjun Mehta, Vice-Chancellor, Nexora University", ST["nt"])]
    e += [PB()]
    e += sec("2. Student Rights & Responsibilities")
    e += bul("2.1 Every Student Has the Right To:", [
        "Quality education delivered by qualified faculty without discrimination",
        "Access all campus facilities — library, labs, sports, hostels — as per eligibility",
        "A safe, inclusive, and discrimination-free campus environment",
        "Voice concerns and grievances through proper channels without fear of retaliation",
        "Participate in student union elections, cultural activities, and events",
        "Receive timely academic feedback, marks, and result information",
        "Privacy of personal information as per university data protection policy",
    ])
    e += bul("2.2 Every Student Has the Responsibility To:", [
        "Maintain minimum 75% attendance in all courses",
        "Submit assignments, projects, and reports by stipulated deadlines",
        "Respect all faculty, staff, fellow students, and campus visitors",
        "Protect and maintain all university property, equipment, and facilities",
        "Follow all rules in the academic and examination regulations handbook",
        "Report incidents of ragging, sexual harassment, or misconduct immediately",
        "Maintain the dignity and reputation of the institution in public and online spaces",
    ])
    e += [PB()]
    e += sec("3. Code of Conduct – Campus Behaviour")
    e += [tbl(["Category","Behaviour","Classification","Action"],
              [["Dress Code","University uniform on campus (Mon–Fri)","Minor","Reminder → Fine ₹200"],
               ["ID Card","Carry university ID at all times","Minor","Fine ₹100"],
               ["Campus Cleanliness","Littering, spitting on campus","Minor","Fine ₹200"],
               ["Property Damage","Breaking chairs, boards, fittings","Moderate","Full cost + written apology"],
               ["Substance Use","Smoking, alcohol, drugs on campus","Severe","Suspension 1–3 semesters"],
               ["Fake Documents","Forging transcripts, ID, certificates","Severe","Rustication + FIR"],
               ["Cyber Misconduct","Hacking university systems, cyberbullying","Severe","Suspension + police report"]], widths=[3.5*cm,5*cm,2.5*cm,5.5*cm]), SP()]
    e += [PB()]
    e += sec("4. Anti-Ragging Policy")
    e += sub("4.1 Definition & Zero-Tolerance Stance", [
        "Ragging is defined as any act, whether physical, verbal, written, or electronic/cyber, that causes physical or psychological harm, discomfort, fear, embarrassment, or humiliation to a student. Nexora University has a ZERO TOLERANCE policy on ragging.",
        "Any form of ragging — including seniors asking juniors to introduce themselves in a demeaning manner, demanding tasks, or any initiation ritual — is treated as a criminal offence under UGC Anti-Ragging Regulations 2009.",
    ])
    e += [tbl(["Offence Level","Examples","Punishment"],
              [["Level 1 – Minor","Verbal teasing, mocking junior","Written warning + community service 20 hrs"],
               ["Level 2 – Moderate","Forcing actions, abusive language","Suspension 1 semester + ₹5,000 fine"],
               ["Level 3 – Severe","Physical harm, group ragging","Rustication + police FIR under IPC 304 A"],
               ["Level 4 – Sexual Ragging","Any sexually offensive act","Permanent expulsion + criminal case"]], widths=[3.5*cm,5.5*cm,7.5*cm]), SP()]
    e += bul("4.2 Anti-Ragging Helplines", [
        "National Anti-Ragging Helpline: 1800-180-5522 (24/7, toll-free)",
        "UGC Anti-Ragging Portal: www.antiragging.in",
        "Nexora Anti-Ragging Cell: antiragging@nexorauniversity.edu | +91-40-4567-8905",
        "Anonymous tip: Drop a note in the Anti-Ragging suggestion boxes placed at all block entrances",
    ])
    e += [PB()]
    e += sec("5. Sexual Harassment Policy (POSH Act)")
    e += sub("5.1 Policy Statement", [
        "Nexora University is committed to providing a workplace and campus that is free from sexual harassment. The Internal Complaints Committee (ICC) is constituted as per the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013.",
        "All complaints are treated with strict confidentiality. No retaliatory action against the complainant is tolerated.",
    ])
    e += [tbl(["ICC Member","Designation","Role"],
              [["Dr. Nithya Prasad","Senior Faculty, Humanities","Presiding Officer (ICC Chairperson)"],
               ["Dr. Rashmi Bhat","Associate Professor, CSE","ICC Member"],
               ["Ms. Anupama Reddy","HR Manager, Admin","ICC Member"],
               ["Mr. Ravi Kumar","Student Union President","External Member"],
               ["Ms. Fatima Khan","NGO Representative (Anvaya Foundation)","External Member"]], widths=[4.5*cm,4.5*cm,7.5*cm]), SP()]
    e += [PB()]
    e += sec("6. Health & Wellness Services")
    e += sub("6.1 Campus Medical Centre", [
        "A fully equipped campus medical centre operates 24/7 with 2 MBBS doctors, 3 nurses, and a visiting specialist (gynaecologist on Tuesdays, psychiatrist/counsellor on Thursdays).",
        "Services: First aid, OPD consultations, basic diagnostics (BP, blood sugar, ECG), emergency stabilisation, ambulance arrangements, and referrals to partner hospitals.",
    ])
    e += [tbl(["Service","Days","Timings","Contact"],
              [["OPD (General)","Mon–Sun","8 AM – 8 PM","+91-40-4567-8920"],
               ["Emergency","Mon–Sun","24 hours","Campus Security: 8901"],
               ["Counsellor / Psychologist","Mon, Wed, Fri","10 AM – 4 PM","counselling@nexorauniversity.edu"],
               ["Dental Clinic (Visiting)","Tuesday","10 AM – 2 PM","Book via portal"],
               ["Gynaecologist (Visiting)","Wednesday","10 AM – 1 PM","Book via portal"]], widths=[4*cm,3*cm,3.5*cm,6*cm]), SP()]
    e += faq([
        ("How do I raise a formal grievance against a faculty member?","Submit a written complaint to the Student Grievance Redressal Committee (SGRC) via the Nexora Student Portal under 'Grievances'. Anonymous complaints are also accepted. Resolution timeline: 15 working days."),
        ("What support is available for students with mental health concerns?","Free confidential counselling is available at the Student Wellness Centre. Students may book appointments online or walk in during counselling hours. A peer support group 'MindSpace' also meets every Friday at 5 PM."),
    ])
    build("Student_Handbook_Code_of_Conduct.pdf", e, "Student Handbook & Code of Conduct")


# ═══════════════════════════════════════════════════════════════════════════
# PDF 14 – Campus Facilities & Infrastructure Guide
# ═══════════════════════════════════════════════════════════════════════════
def pdf_14():
    e = cover("Campus Facilities & Infrastructure Guide","Sports, Cafeteria, Labs, Health Centre & More","Campus")
    e += toc([("1","Campus Map Overview"),("2","Sports Facilities"),("3","Cafeteria & Food Courts"),
               ("4","IT Infrastructure"),("5","Health Centre"),("6","Banking & ATM"),("7","Other Facilities"),("8","FAQs")])
    e += sec("1. Campus Overview", "250-acre campus | 48 academic buildings | 6 hostel blocks | 2 sports complexes")
    e += [tbl(["Facility","Location","Timings","Access"],
              [["Main Library","Academic Block, Central","7:30 AM – 10 PM (Mon-Fri)","All students"],
               ["Sports Complex 1 (Indoor)","Sports Zone A","6 AM – 9 PM (all days)","All students"],
               ["Sports Complex 2 (Outdoor)","Sports Zone B","6 AM – 8 PM (all days)","All students"],
               ["Central Cafeteria","Main Plaza","7 AM – 10 PM","All"],
               ["Medical Centre","Block G, Ground Floor","24/7","All"],
               ["Bank Branch (SBI)","Admin Block","9:30 AM – 3:30 PM (Mon-Fri)","All"],
               ["ATM (SBI + HDFC)","Near Main Gate","24/7","All"],
               ["Post Office (sub-branch)","Admin Block","10 AM – 4 PM (Mon-Fri)","All"],
               ["Stationery & Book Store","Near Library","9 AM – 6 PM (Mon-Sat)","All"]], widths=[4*cm,4*cm,4*cm,3.5*cm]), SP()]
    e += [PB()]
    e += sec("2. Sports Facilities")
    e += [tbl(["Sport","Facility","Capacity","Coach Available"],
              [["Cricket","Full-size turf ground + practice nets","Playing XI + net practice simultaneous","Yes – Level 2 NCA coach"],
               ["Football","FIFA-standard grass field","22 players + substitutes","Yes – National B License"],
               ["Basketball","2 NBA-spec courts (indoor)","5v5 per court","Yes – State-level coach"],
               ["Badminton","6 synthetic courts (indoor, shuttled)","6 simultaneous games","Yes – District-level coach"],
               ["Table Tennis","8 TT tables (indoor)","8 simultaneous games","Yes"],
               ["Chess","Dedicated club room (20 boards)","20 simultaneous games","Yes – FIDE-rated trainer"],
               ["Gym (Fitness Centre)","220+ equipment, 3,000 sq.ft","150 simultaneous users","Yes – Certified fitness trainer"],
               ["Swimming Pool","Olympic-size 50m, 8 lanes","Lap + coaching sessions","Yes – State-level swimmer"],
               ["Volleyball","2 sand courts (outdoor)","2 simultaneous games","Yes"],
               ["Athletics Track","400m synthetic track + field events","Training + events","Yes"]], widths=[3*cm,5*cm,4.5*cm,4*cm]), SP()]
    e += sub("2.1 Annual Sports Events", [
        "NEXSPORTS — Annual Inter-Department Sports Championship (February). 22 sports disciplines, 2,000+ participants. Winners receive trophies, medals, and sports excellence certificates recognising achievements for placement portfolios.",
    ])
    e += [PB()]
    e += sec("3. Cafeteria & Food Courts")
    e += [tbl(["Outlet","Location","Specialty","Timings"],
              [["Central Mess Hall","Near Hostel A-B","Wholesome veg & non-veg thali","7 AM – 9:30 PM"],
               ["The Brew Café","Main Plaza","Coffee, Sandwiches, Snacks","8 AM – 10 PM"],
               ["South Indian Corner","Academic Block Ground Floor","Idli, Dosa, Upma, Filter Coffee","7:30 AM – 3 PM"],
               ["Mughal Bites","Student Activity Centre","Biryani, Kebabs, Rolls","12 PM – 9 PM"],
               ["Green Leaf Salad Bar","Sports Complex Entrance","Salads, Juices, Smoothies","8 AM – 6 PM"],
               ["Bakery & Confectionery","Near Main Gate","Cakes, Pastries, Bread","8:30 AM – 8 PM"],
               ["24-Hour Vending Zone","Near Hostels C & F","Packed snacks, beverages, instant meals","24/7 (automated)"]], widths=[4*cm,4*cm,4.5*cm,4*cm]), SP()]
    e += [PB()]
    e += sec("4. IT Infrastructure")
    e += sub("4.1 Campus Wi-Fi & Network", [
        "The entire 250-acre campus is covered by 1,400+ Wi-Fi 6 access points, providing 100 Mbps dedicated speed per connected device. The backbone network runs at 10 Gbps. Students receive 100 GB monthly data quota on the campus network.",
        "Guest Wi-Fi is available for visitors in public areas. All academic activities are prioritised over entertainment traffic using QoS policies.",
    ])
    e += bul("4.2 IT Services Available to Students", [
        "Microsoft 365 Education licence (Word, Excel, PowerPoint, Teams, OneDrive 1TB) — free for all enrolled students",
        "MATLAB student licence — free access on campus and via VPN",
        "Adobe Creative Cloud — free access in Design and Architecture labs",
        "GitHub Student Developer Pack (free via student email)",
        "24/7 IT Helpdesk: it.helpdesk@nexorauniversity.edu | +91-40-4567-8940",
    ])
    e += faq([
        ("Where can I get a duplicate student ID card?","Visit the Administrative Office (Block A, Room 005) with your admission letter and a passport-size photograph. Fee: ₹200. ID issued within 2 working days."),
        ("Can I use the sports facilities as a day scholar?","Yes, all sports facilities are open to both hostel residents and day scholars during designated hours. Gym membership includes unlimited access with a one-time annual registration of ₹500."),
    ])
    build("Campus_Facilities_Guide.pdf", e, "Campus Facilities & Infrastructure Guide")

# ═══════════════════════════════════════════════════════════════════════════
# PDFs 15, 16, 17 – Reserved for Manual Admin Testing
# These three are generated with a clear "Reserved for Admin Upload" label
# so they appear in knowledge_base/ but are NOT to be auto-indexed.
# ═══════════════════════════════════════════════════════════════════════════
def pdf_15():
    e = cover("International Exchange & Study Abroad Programme",
              "Partner Universities, Application Process & Scholarships","International")
    e += toc([("1","Programme Overview"),("2","Partner Universities"),("3","Application Process"),
               ("4","Scholarships for Exchange Students"),("5","FAQs")])
    e += sec("1. International Exchange Programme Overview")
    e += sub("1.1 About the Programme", [
        "Nexora University maintains academic exchange agreements with 38 partner universities across 18 countries. Students may participate in semester exchange, summer school, dual degree, and research internship programmes.",
        "Exchange programmes typically cover 1 or 2 semesters. Credits earned abroad are transferred and counted toward the Nexora degree (subject to equivalency approval).",
    ])
    e += [tbl(["Country","Partner University","Programme","Duration"],
              [["USA","University of Illinois Urbana-Champaign","Research Internship / Semester Exchange","1–2 semesters"],
               ["USA","Carnegie Mellon University","Summer School – AI & Systems","6 weeks"],
               ["Germany","Technical University of Munich (TUM)","Semester Exchange","1 semester"],
               ["Singapore","Nanyang Technological University (NTU)","Semester Exchange / Dual Degree","1–2 semesters"],
               ["UK","University of Edinburgh","Semester Exchange","1 semester"],
               ["Japan","Tokyo Institute of Technology","Research Internship","3 months"],
               ["Australia","UNSW Sydney","Semester Exchange","1 semester"],
               ["Canada","University of Toronto","Summer School / Research","6 weeks"],
               ["Netherlands","Delft University of Technology (TU Delft)","Semester Exchange","1 semester"],
               ["South Korea","KAIST","Research & Exchange","1 semester"]], widths=[2.5*cm,5.5*cm,5.5*cm,3*cm]), SP()]
    e += [PB()]
    e += sec("2. Eligibility & Application Process")
    e += [tbl(["Step","Action","Deadline","Remarks"],
              [["1","Submit Expression of Interest (EOI) on International Office portal","31 October (for Spring) / 31 March (for Fall)","Shortlisting based on CGPA + SoP"],
               ["2","Receive provisional acceptance letter from partner university","4–6 weeks after EOI","Subject to partner university screening"],
               ["3","Apply for scholarship (if available)","Simultaneous with Step 2","Multiple scholarships available"],
               ["4","Obtain NOC from HOD and Dean Academic","After provisional acceptance","Mandatory for credit transfer approval"],
               ["5","Apply for student visa","8–12 weeks before departure","Nexora International Office assists"],
               ["6","Pre-departure orientation","2 weeks before departure","Mandatory attendance"]], widths=[1.5*cm,6*cm,4*cm,5*cm]), SP()]
    e += [PB()]
    e += sec("3. Financial Support for Exchange Students")
    e += [tbl(["Scholarship / Grant","Amount","Eligibility","Source"],
              [["Nexora Global Merit Scholarship","₹2–5 lakh","CGPA ≥ 8.5, top 10 per year","University funded"],
               ["ASEM-DUO India Fellowship","₹3.5 lakh","India-EU exchanges","ASEM Education Secretariat"],
               ["ICCR Cultural Scholarship","Varies","Arts, Media, Performance","Indian Govt. (ICCR)"],
               ["DAAD India Scholarship","€750/month","Germany exchanges","DAAD Germany"],
               ["Singapore International Award","SGD 10,000","NTU/NUS partners","Singapore Govt."],
               ["Erasmus+ (Europe)","€700–1,200/month","EU partner universities","European Commission"]], widths=[5*cm,3*cm,4.5*cm,4*cm]), SP()]
    e += faq([
        ("Will my credits be recognised when I return?","Yes, provided you submit the credit transfer approval form signed by your HOD before departure. Up to 20 credits per semester can be transferred. All transferred courses appear on your Nexora transcript."),
        ("Can I extend my stay abroad beyond the approved period?","Extensions require fresh approval from Dean Academic and partner university. Maximum extension: 1 additional semester. Students on extension must continue paying Nexora tuition fees at 30% rate."),
    ])
    e += [PB()]
    e += [Paragraph("⚠  RESERVED FOR MANUAL ADMIN TESTING  ⚠", ParagraphStyle("res", fontName="Helvetica-Bold", fontSize=14, textColor=colors.red, alignment=TA_CENTER))]
    e += [Paragraph("This PDF (PDF 15) is intentionally reserved and should be uploaded manually through the Admin Portal for testing the document upload and indexing pipeline.", ST["bd"])]
    build("International_Exchange_Programme.pdf", e, "International Exchange & Study Abroad")

def pdf_16():
    e = cover("Industry Interface & MoU Directory","Corporate Partners, MoUs & Industry Collaboration Handbook","Industry")
    e += toc([("1","Industry Partnership Framework"),("2","Active MoUs"),("3","Industry-Sponsored Chairs"),
               ("4","Centre of Excellence Partners"),("5","Industry Projects & Funding"),("6","FAQs")])
    e += sec("1. Industry Partnership Framework")
    e += sub("1.1 About the Industry Interface Cell (IIC)", [
        "The Industry Interface Cell (IIC) at Nexora University is the nodal agency for managing all corporate partnerships, Memoranda of Understanding (MoUs), Centre of Excellence (CoE) agreements, and research collaboration contracts.",
        "As of June 2026, Nexora has 87 active MoUs with leading companies in IT, manufacturing, healthcare, finance, and public sector organisations. These partnerships generate ₹18 crore annually in research grants, sponsored projects, and equipment donations.",
    ])
    e += [tbl(["Sector","Number of MoUs","Key Partners"],
              [["Information Technology","28","Google, Microsoft, Amazon, TCS, Infosys, Wipro, Zoho"],
               ["Manufacturing & Auto","14","Hyundai, Bosch, Mahindra, L&T, Volvo"],
               ["Healthcare & Pharma","9","Apollo, AIIMS, Dr. Reddy's, Cipla"],
               ["Finance & BFSI","10","ICICI, HDFC, SBI, Deloitte, KPMG"],
               ["Government & PSU","12","DRDO, ISRO, HAL, BHEL, BSNL"],
               ["Startups & SMEs","14","30+ Hyderabad-based tech startups"]], widths=[4*cm,3.5*cm,9*cm]), SP()]
    e += [PB()]
    e += sec("2. Centres of Excellence (CoEs)")
    e += [tbl(["CoE Name","Industry Partner","Focus Area","Annual Grant"],
              [["Nexora-Google CoE in AI","Google India","Large Language Models, AI for Education","₹1.5 crore/year"],
               ["Nexora-Microsoft Azure CoE","Microsoft India","Cloud Architecture, DevSecOps","₹1.2 crore/year"],
               ["Nexora-Qualcomm 5G Lab","Qualcomm India","5G, Edge Computing, IoT Protocols","₹80 lakh/year"],
               ["Nexora-Bosch Industry 4.0 Lab","Robert Bosch","Smart Manufacturing, PLCs, Digital Twin","₹60 lakh/year"],
               ["Nexora-NVIDIA Deep Learning Lab","NVIDIA India","GPU Computing, AI Model Training","Equipment + ₹40 lakh/year"]], widths=[5*cm,4*cm,4.5*cm,3*cm]), SP()]
    e += [PB(), Paragraph("⚠  RESERVED FOR MANUAL ADMIN TESTING  ⚠", ParagraphStyle("res", fontName="Helvetica-Bold", fontSize=14, textColor=colors.red, alignment=TA_CENTER))]
    e += [Paragraph("This PDF (PDF 16) is intentionally reserved and should be uploaded manually through the Admin Portal for testing the document indexing pipeline.", ST["bd"])]
    build("Industry_Interface_MoU_Directory.pdf", e, "Industry Interface & MoU Directory")

def pdf_17():
    e = cover("NSS, NCC & Social Outreach Programme Handbook",
              "Community Engagement, Social Service & Discipline Activities","Campus")
    e += toc([("1","NSS at Nexora"),("2","NCC Wing"),("3","Annual NSS Activities"),
               ("4","Social Outreach Initiatives"),("5","Volunteer Credits"),("6","FAQs")])
    e += sec("1. NSS at Nexora University","National Service Scheme Unit No. NX-TG-042 | 800+ enrolled volunteers")
    e += sub("1.1 Programme Overview", [
        "The National Service Scheme (NSS) at Nexora University has been active since 2012. The NSS unit, designated NX-TG-042, has 800+ enrolled volunteers across all departments and programmes.",
        "NSS activities count toward student extracurricular credits (2 credits per year). Special Camp participation is mandatory for students enrolled in NSS to earn the final certificate.",
    ])
    e += [tbl(["Activity","Duration","Credits","Month"],
              [["Regular Activity (Community Work)","120 hours/year","1 credit","Year-round"],
               ["Special Camp (Village Adoption)","7 days intensive","1 credit","November"],
               ["Blood Donation Camp","1 day","0.5 credit","October"],
               ["Tree Plantation Drive","1 day","0.5 credit","July"],
               ["Swachh Bharat Abhiyan","2 days","0.5 credit","October 2"],
               ["Digital Literacy Campaign","2 days","0.5 credit","February"]], widths=[5.5*cm,3.5*cm,2.5*cm,5*cm]), SP()]
    e += [PB()]
    e += sec("2. NCC Wing")
    e += sub("2.1 About NCC at Nexora", [
        "The Nexora University NCC wing operates under 23 Telangana Battalion. Both Army and Air Wing units are available. NCC cadets receive B and C certificate benefits including 5% marks advantage in UPSC Tier I and preference in state government jobs.",
    ])
    e += [tbl(["Wing","Strength","Commanding Officer","Meeting Day"],
              [["Army Wing (Boys + Girls)","150 cadets","Col. R. Krishnaswamy (Retd.)","Tuesday & Thursday"],
               ["Air Wing (Boys + Girls)","75 cadets","Wg. Cdr. P. Subramaniam (Retd.)","Monday & Wednesday"]], widths=[5*cm,3.5*cm,5*cm,3*cm]), SP()]
    e += [PB()]
    e += sec("3. Social Outreach Initiatives")
    e += [tbl(["Initiative","Description","Scale","Year"],
              [["Nexora Digital Village","Adopted village: Chevella (30 km). Regular digital literacy & health camps","800+ beneficiaries/year","2019–present"],
               ["Teach for Nexora","Student volunteers teach in municipal schools","500 students/year (15 schools)","2020–present"],
               ["Nexora Green Campus","Campus-wide sustainability drive","Zero plastic, solar expansion","2021–present"],
               ["Health on Wheels","Mobile medical camp in tribal areas","4 camps/year, 1,000+ patients","2022–present"]], widths=[4*cm,6*cm,4*cm,2.5*cm]), SP()]
    e += faq([
        ("Is NSS/NCC participation compulsory?","No, both are voluntary. However, participation in NSS or NCC earns extracurricular credits that contribute to the final CGPA calculation (2 credits = 0.05 CGPA weightage)."),
        ("Can NCC B/C certificate holders get admission preference?","Yes. NCC C certificate holders with Army/Air wing receive 5 extra marks in NEXET and merit-based admission ranking."),
    ])
    e += [PB(), Paragraph("⚠  RESERVED FOR MANUAL ADMIN TESTING  ⚠", ParagraphStyle("res", fontName="Helvetica-Bold", fontSize=14, textColor=colors.red, alignment=TA_CENTER))]
    e += [Paragraph("This PDF (PDF 17) is intentionally reserved and should be uploaded manually through the Admin Portal.", ST["bd"])]
    build("NSS_NCC_Social_Outreach.pdf", e, "NSS, NCC & Social Outreach Handbook")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN – Run all 17 PDF generators
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Nexora University – Generating 17 Professional PDFs")
    print(f"Output directory: {KB}")
    print("=" * 60)
    generators = [
        pdf_01, pdf_02, pdf_03, pdf_04, pdf_05, pdf_06, pdf_07,
        pdf_08, pdf_09, pdf_10, pdf_11, pdf_12, pdf_13, pdf_14,
        pdf_15, pdf_16, pdf_17,
    ]
    ok, failed = 0, []
    for fn in generators:
        try:
            fn()
            ok += 1
        except Exception as ex:
            print(f"  ✗ {fn.__name__} FAILED: {ex}")
            failed.append(fn.__name__)
    print("=" * 60)
    print(f"Done: {ok}/17 PDFs generated")
    if failed:
        print(f"Failed: {failed}")
    print(f"\nPDFs 1-14 → auto-upload to Supabase Storage + Pinecone via ingest pipeline")
    print(f"PDFs 15-17 → RESERVED for manual admin upload testing:")
    print(f"  PDF 15: International_Exchange_Programme.pdf")
    print(f"  PDF 16: Industry_Interface_MoU_Directory.pdf")
    print(f"  PDF 17: NSS_NCC_Social_Outreach.pdf")
