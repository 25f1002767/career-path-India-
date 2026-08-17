import { CareerPath } from "../types/career";

/**
 * Strict domain mapping keywords for all 15 official Career Domains
 */
export const DOMAIN_KEYWORDS: Record<string, { aliases: string[]; terms: string[] }> = {
  "Civil Services & Public Admin": {
    aliases: ["civil services", "public admin", "administrative", "public administration", "state psc", "civil service"],
    terms: ["upsc", "ias", "ips", "ifs", "irs", "ssc cgl", "state psc", "bpsc", "uppsc", "mpsc", "ras", "wbcs", "administrative officer", "civil service", "collector", "magistrate", "deputy collector", "tehsildar", "secretariat", "sdm", "block development"],
  },
  "Defense, Police & Security": {
    aliases: ["defense", "police", "security", "armed forces", "military", "paramilitary"],
    terms: ["nda", "cds", "afcat", "army", "navy", "air force", "capf", "cisf", "crpf", "bsf", "itbp", "ssb", "sub-inspector", "si", "police", "coast guard", "defense", "commando", "security officer", "intelligence bureau", "raw", "constable", "dsp", "acp"],
  },
  "Banking & Financial Services": {
    aliases: ["banking", "financial services", "finance", "insurance", "accounting", "fintech"],
    terms: ["rbi", "sbi", "ibps", "bank", "nabard", "lic", "sebi", "actuarial", "actuary", "investment bank", "chartered accountant", "ca", "equity", "financial analyst", "fintech", "credit analyst", "treasury", "risk manager", "loan officer", "wealth management", "audit"],
  },
  "Railways & Public Transport": {
    aliases: ["railways", "railway", "public transport", "metro", "transportation"],
    terms: ["rrb", "railway", "ntpc", "loco pilot", "station master", "dmrc", "metro", "indian railway", "irms", "train manager", "track maintainer", "section engineer", "rail"],
  },
  "Public Sector Undertakings (PSUs)": {
    aliases: ["public sector", "psu", "psus", "maharatna", "navratna", "miniratna"],
    terms: ["psu", "ongc", "bhel", "iocl", "ntpc", "sail", "bpcl", "hpcl", "powergrid", "gail", "hal", "bel", "coal india", "nhpc", "oil india", "management trainee psu", "executive trainee"],
  },
  "Software Engineering & IT": {
    aliases: ["software engineering", "information technology", "it", "software development", "computer science"],
    terms: ["sde", "software", "developer", "full stack", "backend", "frontend", "devops", "cloud", "aws", "azure", "cybersecurity", "cyber", "nic scientist", "nielit", "systems engineer", "mobile app", "qa engineer", "penetration tester", "architect", "programmer", "tech lead", "embedded software"],
  },
  "AI, Data Science & Analytics": {
    aliases: ["ai", "data science", "analytics", "artificial intelligence", "machine learning", "deep learning", "big data"],
    terms: ["ai", "data scientist", "data analyst", "machine learning", "mlops", "deep learning", "computer vision", "nlp", "analytics", "big data", "llm", "genai", "generative ai", "neural", "power bi", "tableau", "data engineer", "data warehouse", "spark", "pytorch", "tensorflow", "predictive", "statistics", "business analyst"],
  },
  "Healthcare & Pharmaceuticals": {
    aliases: ["healthcare", "pharmaceuticals", "medical", "pharma", "nursing", "clinical", "biotech"],
    terms: ["mbbs", "doctor", "medical officer", "aiims", "pharmacist", "pharmacy", "drug inspector", "clinical", "nurse", "nursing officer", "biotech", "dentist", "hospital", "physiotherapy", "pathology", "biomedical", "fssai"],
  },
  "Design, Product & Creative Arts": {
    aliases: ["design", "product management", "creative arts", "ui/ux", "multimedia", "animation"],
    terms: ["ui", "ux", "ui/ux", "product designer", "product manager", "industrial design", "graphic designer", "animator", "3d artist", "nid", "nift", "game designer", "visual designer", "creative director", "motion graphics", "brand designer"],
  },
  "Teaching, Education & Academia": {
    aliases: ["teaching", "education", "academia", "academic", "professorship", "school"],
    terms: ["ugc net", "professor", "assistant professor", "kvs", "nvs", "tgt", "pgt", "ctet", "instructional design", "edtech", "teacher", "lecturer", "curriculum", "phd", "academic research", "dean"],
  },
  "Aviation & Aerospace R&D": {
    aliases: ["aviation", "aerospace", "space", "aeronautical", "flight"],
    terms: ["isro", "drdo aerospace", "pilot", "commercial pilot", "air traffic", "atc", "dgca", "drone", "aerospace", "avionics", "aircraft", "aeronautical", "satellite", "propulsion"],
  },
  "Law & Judicial Services": {
    aliases: ["law", "judicial", "judiciary", "legal", "courts"],
    terms: ["judge", "judicial", "magistrate", "prosecutor", "lawyer", "advocate", "patent attorney", "legal advisor", "legal counsel", "sebi legal", "ibps law", "clat", "bar council", "corporate counsel", "solicitor"],
  },
  "Core Engineering & Construction": {
    aliases: ["core engineering", "construction", "civil engineering", "mechanical", "electrical", "infrastructure"],
    terms: ["ies", "ese", "cpwd", "central engineering", "automotive", "tata motors", "l&t", "cad", "solidworks", "site engineer", "civil engineer", "mechanical engineer", "electrical engineer", "structural", "gis", "remote sensing", "construction manager", "metallurgy"],
  },
  "Media, Journalism & PR": {
    aliases: ["media", "journalism", "public relations", "pr", "mass communication", "broadcasting"],
    terms: ["indian information service", "iis", "pib", "journalist", "news anchor", "content strategist", "pr lead", "media officer", "corporate communications", "editor", "broadcaster", "press officer", "copywriter"],
  },
  "Agri-Tech & Forest Services": {
    aliases: ["agri-tech", "agriculture", "forest", "forestry", "farming", "horticulture", "soil"],
    terms: ["indian forest service", "ifos", "icar", "ars scientist", "forest service", "agriculture officer", "nabard", "agritech", "export inspection", "eic", "fssai", "agronomy", "horticulture", "soil science", "crop", "krishi"],
  },
};

/**
 * Determines whether a career path strictly belongs to the user's selected domains.
 * If userDomains is empty or contains "ALL", returns true.
 */
export function matchesSelectedDomains(career: CareerPath, userDomains?: string[]): boolean {
  if (!userDomains || userDomains.length === 0 || (userDomains.length === 1 && userDomains[0] === "ALL")) {
    return true;
  }

  const cDomain = (career.domain || "").toLowerCase().trim();
  const cTitle = (career.title || "").toLowerCase().trim();
  const cDesc = (career.shortDescription || "").toLowerCase().trim();
  const cTags = (career.tags || []).map((t) => t.toLowerCase()).join(" ");
  const cFullText = `${cDomain} ${cTitle} ${cDesc} ${cTags}`;

  // Check if career matches ANY of the chosen user domains
  return userDomains.some((selectedDomain) => {
    const selClean = selectedDomain.toLowerCase().trim();

    // 1. Direct domain equality or containment
    if (cDomain === selClean || cDomain.includes(selClean) || selClean.includes(cDomain)) {
      return true;
    }

    // 2. Dictionary alias check on domain string
    const dict = DOMAIN_KEYWORDS[selectedDomain];
    if (dict) {
      for (const alias of dict.aliases) {
        if (cDomain.includes(alias) || alias.includes(cDomain)) return true;
      }
    }

    // 3. If career's domain is explicitly set to ANOTHER known domain from our list,
    // do NOT let generic keywords leak it across domains!
    const isOtherKnownDomain = Object.keys(DOMAIN_KEYWORDS).some((otherDom) => {
      if (otherDom === selectedDomain) return false;
      const otherClean = otherDom.toLowerCase().trim();
      if (cDomain === otherClean || cDomain.includes(otherClean)) return true;
      const otherDict = DOMAIN_KEYWORDS[otherDom];
      return otherDict?.aliases.some((a) => cDomain.includes(a));
    });

    if (isOtherKnownDomain) {
      return false; // Strongly belongs to another domain, reject
    }

    // 4. If domain wasn't explicitly another known domain, check specific terms in title/text
    if (dict) {
      for (const term of dict.terms) {
        const regex = new RegExp(`\\b${term}\\b`, "i");
        if (regex.test(cFullText)) {
          return true;
        }
      }
    }

    // 5. Fallback token overlap on domain
    const tokens = selClean.split(/[ ,&/]+/).filter((t) => t.length > 2 && t !== "and" && t !== "services");
    return tokens.some((token) => cDomain.includes(token));
  });
}
