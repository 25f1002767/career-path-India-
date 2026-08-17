export type TierType = "ELITE" | "STABLE" | "HIDDEN_GEM";
export type SectorType = "GOVT" | "PRIVATE";
export type EducationLevel = "12TH" | "DIPLOMA" | "GRADUATE" | "POST_GRADUATE";
export type StreamType = 
  | "SCIENCE_PCM" 
  | "SCIENCE_PCB" 
  | "COMMERCE" 
  | "ARTS_HUMANITIES" 
  | "ENGINEERING" 
  | "MEDICAL_HEALTHCARE" 
  | "LAW" 
  | "MANAGEMENT" 
  | "VOCATIONAL_ANY";

export type SocialCategory = "GENERAL" | "OBC" | "SC" | "ST" | "EWS" | "PWD" | "EX_SERVICEMEN";

export interface RoadmapStep {
  stepNumber: number;
  title: string;
  description: string;
  estimatedDuration?: string;
  keyResources?: string[];
}

export interface Eligibility {
  educationRequired: string;
  minEducationLevel: EducationLevel;
  ageLimit?: {
    min: number;
    max: number;
    relaxations?: {
      category: SocialCategory;
      yearsExtention: number;
      notes?: string;
    }[];
  };
  otherCriteria?: string[];
  physicalCriteria?: string;
}

export interface CompetitionStats {
  applicants?: number;
  seats?: number;
  ratio?: string;
  lastUpdated: string;
  difficultyRating?: "MODERATE" | "HIGH" | "VERY_HIGH" | "EXTREME";
}

export interface ExamTimeline {
  notificationMonth: string; // e.g. "February" or "Feb - Mar"
  examMonth?: string;        // e.g. "May / June"
  frequency: string;        // e.g. "Annual", "Bi-annual", "Rolling"
  applicationFee?: string;  // e.g. "₹100 (Exempted for Women/SC/ST)"
}

export interface SourceCitation {
  title: string;
  url: string;
}

export interface CareerPath {
  id: string;
  title: string;
  tier: TierType;
  sector: SectorType;
  domain: string;
  shortDescription: string;
  eligibility: Eligibility;
  competitionStats?: CompetitionStats;
  roadmapSteps: RoadmapStep[];
  salaryRange: {
    min: number; // In INR per month or annual LPA, normalized to PM (Per Month) in INR
    max: number;
    currency: "INR";
    payScaleCode?: string; // e.g. "Pay Level 10 (7th CPC)"
  };
  applicationPortalUrl?: string;
  sources: SourceCitation[];
  stateSpecific?: string | null; // e.g. "Maharashtra", "Uttar Pradesh", or null for Pan-India
  examTimeline?: ExamTimeline;
  growthProspects?: string;
  tags?: string[];
}

export interface UserProfile {
  name: string;
  dob?: string; // YYYY-MM-DD
  age?: number;
  educationLevel: EducationLevel;
  stream: StreamType;
  socialCategory: SocialCategory;
  sectorPreference: "GOVT" | "PRIVATE" | "BOTH";
  domains: string[];
  targetState: string; // "Pan-India" or specific state/UT
  salaryBand: "25k_50k" | "50k_1L" | "1L_PLUS";
  additionalGoals?: string;
}

export interface FilterState {
  sector: "ALL" | "GOVT" | "PRIVATE";
  tier: "ALL" | "ELITE" | "STABLE" | "HIDDEN_GEM";
  domain: string;
  searchQuery: string;
  eligibilityFilter: "ALL" | "ELIGIBLE_ONLY";
  sortBy: "RECOMMENDED" | "SALARY_HIGH" | "COMPETITION_LOW" | "DURATION_SHORT";
}

export interface AgeEligibilityStatus {
  isEligible: boolean;
  userAge: number;
  minAge: number;
  maxAgeAllowed: number;
  baseMaxAge: number;
  appliedRelaxationYears: number;
  statusText: string;
  statusBadge: "ELIGIBLE" | "RELAXED_ELIGIBLE" | "UNDERAGE" | "OVERAGE";
}
