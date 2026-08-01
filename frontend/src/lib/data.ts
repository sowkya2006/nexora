import type { DocumentCategory } from "./constants";

export interface Document {
  id: string;
  name: string;
  category: DocumentCategory;
  description: string;
  version: string;
  updatedAt: string;
  fileUrl?: string;
  file_name?: string;
  pages?: number;
  size?: string;
  status?: string;
}

export interface Notice {
  id: string;
  title: string;
  description: string;
  category: "Academic" | "Examination" | "Events" | "Administration";
  date: string;
  attachmentUrl?: string;
  status: "published" | "draft" | "archived";
}

export interface Event {
  id: string;
  name: string;
  description: string;
  date: string;
  venue: string;
  organizer: string;
  status: "upcoming" | "active" | "completed" | "archived";
  brochureUrl?: string;
}

export interface Faculty {
  id: string;
  name: string;
  department: string;
  designation: string;
  qualification: string;
  researchInterests: string[];
  email: string;
}

export interface Department {
  id: string;
  name: string;
  overview: string;
  programs: string[];
  researchAreas: string[];
  facilities: string[];
}

export const documents: Document[] = [
  { id: "1", name: "Admission Brochure 2026", category: "Admissions", description: "Complete guide to admission procedures, eligibility, and fee structure", version: "2026", updatedAt: "2026-07-01", file_name: "Admission_Brochure_2026.pdf", fileUrl: "/knowledge_base/Admission_Brochure_2026.pdf", pages: 12, size: "1.4 MB", status: "indexed" },
  { id: "2", name: "Academic Calendar 2026", category: "Academics", description: "Important academic dates, semester schedule, and exam timetables", version: "2026-27", updatedAt: "2026-06-15", file_name: "Academic_Calendar_2026.pdf", fileUrl: "/knowledge_base/Academic_Calendar_2026.pdf", pages: 10, size: "1.1 MB", status: "indexed" },
  { id: "3", name: "Examination Regulations 2026", category: "Examination", description: "Rules, credit evaluations, and regulations for university examinations", version: "2026", updatedAt: "2026-05-20", file_name: "Examination_Regulations_2026.pdf", fileUrl: "/knowledge_base/Examination_Regulations_2026.pdf", pages: 14, size: "1.5 MB", status: "indexed" },
  { id: "4", name: "Fee Structure 2026", category: "Finance", description: "Detailed fee structure, mess charges, and payment guidelines for all programs", version: "2026-27", updatedAt: "2026-06-01", file_name: "Fee_Structure_2026.pdf", fileUrl: "/knowledge_base/Fee_Structure_2026.pdf", pages: 10, size: "1.2 MB", status: "indexed" },
  { id: "5", name: "Course Catalog and Programs", category: "Academics", description: "Syllabus, curriculum, and electives for all undergraduate and postgraduate programs", version: "2026", updatedAt: "2026-05-10", file_name: "Course_Catalog_and_Programs.pdf", fileUrl: "/knowledge_base/Course_Catalog_and_Programs.pdf", pages: 16, size: "1.8 MB", status: "indexed" },
  { id: "6", name: "Hostel Rules and Fees 2026", category: "Hostel", description: "Comprehensive guidelines, mess rules, and fee structure for hostel residents", version: "2026", updatedAt: "2026-04-01", file_name: "Hostel_Rules_and_Fees_2026.pdf", fileUrl: "/knowledge_base/Hostel_Rules_and_Fees_2026.pdf", pages: 12, size: "1.3 MB", status: "indexed" },
  { id: "7", name: "Placement Brochure 2026", category: "Placements", description: "Placement statistics, recruiting partners, and internship guidelines", version: "2026", updatedAt: "2026-07-10", file_name: "Placement_Brochure_2026.pdf", fileUrl: "/knowledge_base/Placement_Brochure_2026.pdf", pages: 15, size: "1.7 MB", status: "indexed" },
  { id: "8", name: "Scholarship Handbook 2026", category: "Scholarships", description: "Available merit-based and need-based scholarships and application procedures", version: "2026", updatedAt: "2026-06-20", file_name: "Scholarship_Handbook_2026.pdf", fileUrl: "/knowledge_base/Scholarship_Handbook_2026.pdf", pages: 11, size: "1.2 MB", status: "indexed" },
  { id: "9", name: "Library Guide 2026", category: "Library", description: "Central library membership, digital resources, and borrowing regulations", version: "2026", updatedAt: "2026-04-10", file_name: "Library_Guide_2026.pdf", fileUrl: "/knowledge_base/Library_Guide_2026.pdf", pages: 10, size: "1.0 MB", status: "indexed" },
  { id: "10", name: "Transport Handbook 2026", category: "Transport", description: "Campus bus routes, schedules, pass fees, and safety policies", version: "2026", updatedAt: "2026-06-01", file_name: "Transport_Handbook_2026.pdf", fileUrl: "/knowledge_base/Transport_Handbook_2026.pdf", pages: 10, size: "1.1 MB", status: "indexed" },
  { id: "11", name: "Student Code of Conduct 2026", category: "General", description: "Ethics, anti-ragging policies, disciplinary procedure, and campus code of conduct", version: "2026", updatedAt: "2026-05-15", file_name: "Student_Code_of_Conduct_2026.pdf", fileUrl: "/knowledge_base/Student_Code_of_Conduct_2026.pdf", pages: 13, size: "1.4 MB", status: "indexed" },
  { id: "12", name: "Campus Facilities Guide 2026", category: "Campus", description: "Overview of sports complex, labs, cafeteria, medical center, and amenities", version: "2026", updatedAt: "2026-04-15", file_name: "Campus_Facilities_Guide_2026.pdf", fileUrl: "/knowledge_base/Campus_Facilities_Guide_2026.pdf", pages: 12, size: "1.3 MB", status: "indexed" },
  { id: "13", name: "Department Handbook 2026", category: "Departments", description: "Faculty profiles, department labs, research centers, and specializations", version: "2026", updatedAt: "2026-07-01", file_name: "Department_Handbook_2026.pdf", fileUrl: "/knowledge_base/Department_Handbook_2026.pdf", pages: 14, size: "1.6 MB", status: "indexed" },
  { id: "14", name: "Admission Handbook 2026", category: "Admissions", description: "Detailed counseling guide, NRI quota guidelines, and seat matrix", version: "2026", updatedAt: "2026-06-10", file_name: "Admission_Handbook_2026.pdf", fileUrl: "/knowledge_base/Admission_Handbook_2026.pdf", pages: 12, size: "1.4 MB", status: "indexed" },
];

export const notices: Notice[] = [
  { id: "1", title: "Examination Schedule Released", description: "The end-semester examination schedule for July 2026 has been published. All students must check their hall tickets.", category: "Examination", date: "2026-07-25", status: "published" },
  { id: "2", title: "Scholarship Applications Open", description: "Merit-based and need-based scholarship applications are now open for the academic year 2026-27.", category: "Academic", date: "2026-07-20", status: "published" },
  { id: "3", title: "Technical Workshop Announcement", description: "A 3-day workshop on AI and Machine Learning will be conducted from August 5-7, 2026.", category: "Events", date: "2026-07-18", status: "published" },
  { id: "4", title: "Hostel Allotment Results", description: "First-year hostel allotment results have been published on the student portal.", category: "Administration", date: "2026-07-15", status: "published" },
  { id: "5", title: "Library Extended Hours", description: "Central library will remain open until 10 PM during examination period.", category: "Academic", date: "2026-07-10", status: "published" },
];

export const events: Event[] = [
  { id: "1", name: "Nexora Hackathon 2026", description: "48-hour coding marathon with prizes worth ₹5 Lakhs. Open to all engineering students.", date: "2026-08-15", venue: "Innovation Lab", organizer: "CSE Department", status: "upcoming" },
  { id: "2", name: "AI & ML Workshop", description: "Hands-on workshop covering deep learning fundamentals and practical applications.", date: "2026-08-05", venue: "Seminar Hall A", organizer: "AI Club", status: "upcoming" },
  { id: "3", name: "Annual Cultural Fest", description: "Three days of music, dance, drama, and art competitions.", date: "2026-09-20", venue: "Open Air Theatre", organizer: "Cultural Committee", status: "upcoming" },
  { id: "4", name: "Industry Connect Summit", description: "Meet recruiters from top companies and explore internship opportunities.", date: "2026-08-25", venue: "Convention Center", organizer: "Placement Cell", status: "upcoming" },
];

export const departments: Department[] = [
  {
    id: "cse",
    name: "Computer Science and Engineering",
    overview: "Leading department in AI, data science, and software development with state-of-the-art labs.",
    programs: ["B.Tech CSE", "M.Tech CSE", "M.Tech AI & ML", "Ph.D."],
    researchAreas: ["Artificial Intelligence", "Data Science", "Cybersecurity", "Cloud Computing"],
    facilities: ["AI Lab", "Cloud Computing Lab", "Software Development Center"],
  },
  {
    id: "ece",
    name: "Electronics and Communication Engineering",
    overview: "Excellence in communication systems, embedded systems, and VLSI design.",
    programs: ["B.Tech ECE", "M.Tech VLSI", "M.Tech Communication Systems", "Ph.D."],
    researchAreas: ["5G Networks", "Embedded Systems", "Signal Processing", "IoT"],
    facilities: ["VLSI Lab", "Communication Lab", "Embedded Systems Lab"],
  },
  {
    id: "mech",
    name: "Mechanical Engineering",
    overview: "Focus on manufacturing, automation, and design with modern workshop facilities.",
    programs: ["B.Tech Mechanical", "M.Tech Manufacturing", "M.Tech Design", "Ph.D."],
    researchAreas: ["Manufacturing", "Automation", "Robotics", "Thermal Engineering"],
    facilities: ["CAD/CAM Lab", "Workshop", "Robotics Lab"],
  },
  {
    id: "eee",
    name: "Electrical and Electronics Engineering",
    overview: "Power systems, renewable energy, and electrical machine design.",
    programs: ["B.Tech EEE", "M.Tech Power Systems", "Ph.D."],
    researchAreas: ["Renewable Energy", "Power Electronics", "Smart Grid"],
    facilities: ["Power Systems Lab", "Electrical Machines Lab"],
  },
];

export const faculty: Faculty[] = [
  { id: "1", name: "Dr. Rajesh Kumar", department: "Computer Science and Engineering", designation: "Professor & HOD", qualification: "Ph.D. in Computer Science, IIT Delhi", researchInterests: ["Machine Learning", "Natural Language Processing"], email: "rajesh.kumar@nexorauniversity.edu" },
  { id: "2", name: "Dr. Priya Sharma", department: "Computer Science and Engineering", designation: "Associate Professor", qualification: "Ph.D. in AI, IISc Bangalore", researchInterests: ["Deep Learning", "Computer Vision"], email: "priya.sharma@nexorauniversity.edu" },
  { id: "3", name: "Dr. Anil Reddy", department: "Electronics and Communication Engineering", designation: "Professor", qualification: "Ph.D. in ECE, NIT Warangal", researchInterests: ["5G Networks", "VLSI Design"], email: "anil.reddy@nexorauniversity.edu" },
  { id: "4", name: "Dr. Meera Patel", department: "Mechanical Engineering", designation: "Associate Professor", qualification: "Ph.D. in Mechanical Engineering, IIT Bombay", researchInterests: ["Robotics", "Automation"], email: "meera.patel@nexorauniversity.edu" },
  { id: "5", name: "Dr. Suresh Nair", department: "Electrical and Electronics Engineering", designation: "Professor", qualification: "Ph.D. in Power Systems, IIT Madras", researchInterests: ["Renewable Energy", "Smart Grid"], email: "suresh.nair@nexorauniversity.edu" },
];

export const clubs = [
  { name: "AI Club", description: "Exploring artificial intelligence through projects, workshops, and competitions.", activities: ["Hackathons", "ML Workshops", "Research Projects"], achievements: "Winner of National AI Challenge 2025" },
  { name: "Robotics Club", description: "Building robots and participating in national robotics competitions.", activities: ["Robot Building", "Competitions", "Workshops"], achievements: "2nd place in RoboFest 2025" },
  { name: "Coding Club", description: "Competitive programming and software development community.", activities: ["Codeathons", "DSA Sessions", "Open Source"], achievements: "50+ members placed in top companies" },
  { name: "Cultural Club", description: "Promoting arts, music, dance, and cultural activities on campus.", activities: ["Annual Fest", "Inter-college Events", "Workshops"], achievements: "Best Cultural Club Award 2025" },
];

export const busRoutes = [
  { route: "Route 1", areas: ["Secunderabad", "Begumpet", "Ameerpet"], timing: "7:00 AM - 6:30 PM" },
  { route: "Route 2", areas: ["Gachibowli", "HITEC City", "Madhapur"], timing: "7:15 AM - 6:45 PM" },
  { route: "Route 3", areas: ["LB Nagar", "Dilsukhnagar", "Malakpet"], timing: "7:00 AM - 6:30 PM" },
  { route: "Route 4", areas: ["Kukatpally", "Miyapur", "Bachupally"], timing: "7:30 AM - 7:00 PM" },
];
