export const UNIVERSITY = {
  name: "Nexora University",
  tagline: "Where Innovation Meets Excellence",
  shortDescription:
    "Empowering Innovation, Inspiring Future Leaders through quality education, research, and industry collaboration.",
  established: "2010",
  email: "info@nexorauniversity.edu",
  phone: "+91 98765 43210",
  address: "Nexora Campus, Innovation District, Hyderabad, Telangana 500032",
  social: {
    facebook: "https://facebook.com/nexorauniversity",
    twitter: "https://twitter.com/nexorauniversity",
    linkedin: "https://linkedin.com/school/nexorauniversity",
    instagram: "https://instagram.com/nexorauniversity",
  },
};

export const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About" },
  { href: "/admissions", label: "Admissions" },
  { href: "/academics", label: "Academics" },
  { href: "/departments", label: "Departments" },
  { href: "/faculty", label: "Faculty" },
  { href: "/placements", label: "Placements" },
  { href: "/scholarships", label: "Scholarships" },
  { href: "/hostel", label: "Hostel" },
  { href: "/library", label: "Library" },
  { href: "/events", label: "Events" },
  { href: "/clubs", label: "Clubs" },
  { href: "/transport", label: "Transport" },
  { href: "/notices", label: "Notices" },
  { href: "/documents", label: "Documents" },
];

export const QUICK_ACCESS = [
  { href: "/admissions", label: "Admissions", icon: "GraduationCap", description: "Apply and explore programs" },
  { href: "/academics", label: "Academics", icon: "BookOpen", description: "Programs and curriculum" },
  { href: "/placements", label: "Placements", icon: "Briefcase", description: "Career opportunities" },
  { href: "/scholarships", label: "Scholarships", icon: "Award", description: "Financial aid options" },
  { href: "/hostel", label: "Hostel", icon: "Home", description: "Campus accommodation" },
  { href: "/library", label: "Library", icon: "Library", description: "Resources and services" },
  { href: "/notices", label: "Notices", icon: "Bell", description: "Official announcements" },
  { href: "/events", label: "Events", icon: "Calendar", description: "Campus activities" },
];

export const HIGHLIGHTS = [
  { value: "50+", label: "Programs" },
  { value: "12", label: "Departments" },
  { value: "200+", label: "Faculty" },
  { value: "95%", label: "Placement Rate" },
];

export const SUGGESTED_QUESTIONS = [
  "How can I apply for admission?",
  "What are the hostel facilities?",
  "What courses are available?",
  "What scholarships are offered?",
  "What are the examination rules?",
  "What is the fee structure?",
];

export const DOCUMENT_CATEGORIES = [
  "Admissions",
  "Academics",
  "Examination",
  "Finance",
  "Hostel",
  "Placements",
  "Scholarships",
  "Campus",
  "Library",
  "Transport",
  "Events",
  "Departments",
  "General",
] as const;


export type DocumentCategory = (typeof DOCUMENT_CATEGORIES)[number];
