import React, { useState } from "react";
import { UserProfile, EducationLevel, StreamType, SocialCategory } from "../types/career";
import {
  INDIAN_STATES_AND_UTS,
  EDUCATION_LEVEL_OPTIONS,
  STREAM_OPTIONS,
  CAREER_DOMAINS,
  SOCIAL_CATEGORIES,
} from "../data/indianStates";
import { Compass, CheckCircle2, AlertCircle, ArrowRight, Sparkles, Building2, Landmark, ShieldAlert } from "lucide-react";
import { calculateAge } from "../utils/ageCalculator";

interface ProfileFormProps {
  initialProfile?: UserProfile | null;
  onSubmitProfile: (profile: UserProfile) => void;
  isSubmitting?: boolean;
}

export const ProfileForm: React.FC<ProfileFormProps> = ({
  initialProfile,
  onSubmitProfile,
  isSubmitting = false,
}) => {
  const [name, setName] = useState(initialProfile?.name || "");
  const [dob, setDob] = useState(initialProfile?.dob || "2003-06-15"); // ~23 yrs default
  const [educationLevel, setEducationLevel] = useState<EducationLevel>(
    initialProfile?.educationLevel || "GRADUATE"
  );
  const [stream, setStream] = useState<StreamType>(
    initialProfile?.stream || "SCIENCE_PCM"
  );
  const [socialCategory, setSocialCategory] = useState<SocialCategory>(
    initialProfile?.socialCategory || "GENERAL"
  );
  const [sectorPreference, setSectorPreference] = useState<"GOVT" | "PRIVATE" | "BOTH">(
    initialProfile?.sectorPreference || "BOTH"
  );
  const [selectedDomains, setSelectedDomains] = useState<string[]>(
    initialProfile?.domains || [
      "Civil Services & Public Admin",
      "Software Engineering & IT",
      "Banking & Financial Services",
    ]
  );
  const [targetState, setTargetState] = useState<string>(
    initialProfile?.targetState || "Pan-India"
  );
  const [salaryBand, setSalaryBand] = useState<"25k_50k" | "50k_1L" | "1L_PLUS">(
    initialProfile?.salaryBand || "50k_1L"
  );

  const [errors, setErrors] = useState<Record<string, string>>({});

  const toggleDomain = (domain: string) => {
    if (selectedDomains.includes(domain)) {
      if (selectedDomains.length === 1) return; // Keep at least 1
      setSelectedDomains(selectedDomains.filter((d) => d !== domain));
    } else {
      setSelectedDomains([...selectedDomains, domain]);
    }
  };

  const handleValidationAndSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};

    if (!name.trim()) {
      newErrors.name = "Please enter your full name.";
    }

    if (!dob) {
      newErrors.dob = "Date of birth is required for age eligibility checks.";
    }

    if (selectedDomains.length === 0) {
      newErrors.domains = "Please select at least one career domain preference.";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setErrors({});

    const calculatedUserAge = calculateAge(dob);

    const profile: UserProfile = {
      name: name.trim(),
      dob,
      age: calculatedUserAge,
      educationLevel,
      stream,
      socialCategory,
      sectorPreference,
      domains: selectedDomains,
      targetState,
      salaryBand,
    };

    onSubmitProfile(profile);
  };

  const currentAge = calculateAge(dob);
  const categoryInfo = SOCIAL_CATEGORIES.find((c) => c.value === socialCategory);

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6">
      {/* Hero Welcome Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden mb-8">
        <div className="absolute -right-12 -top-12 w-64 h-64 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -left-12 -bottom-12 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10">
          <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30 mb-4">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" /> AI Grounded Career Roadmap for Indian Students
          </div>
          <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-white mb-2">
            Discover Your Ideal Career Path in India
          </h1>
          <p className="text-slate-300 text-sm sm:text-base max-w-2xl leading-relaxed">
            Get a personalized, tiered roadmap of <span className="text-amber-300 font-semibold">Government (UPSC, SSC, RRB, State PSC, Defence)</span> and <span className="text-indigo-300 font-semibold">Private Tech & Corporate</span> options, grounded in live 2025–2026 exam notifications and age criteria.
          </p>
        </div>
      </div>

      {/* Intake Form Container */}
      <form onSubmit={handleValidationAndSubmit} className="bg-white rounded-3xl border border-slate-200 shadow-md p-6 sm:p-8 space-y-8">
        
        {/* Section 1: Basic Info & Age */}
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center mb-4">
            <span className="w-7 h-7 rounded-lg bg-amber-100 text-amber-800 font-extrabold text-sm flex items-center justify-center mr-2">1</span>
            Basic Profile & Category (for Exact Age Eligibility)
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {/* Name */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Full Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Rahul Sharma"
                className={`w-full px-4 py-2.5 rounded-xl border text-sm focus:outline-none focus:ring-2 transition ${
                  errors.name
                    ? "border-red-500 focus:ring-red-200"
                    : "border-slate-300 focus:border-amber-500 focus:ring-amber-200"
                }`}
              />
              {errors.name && <p className="text-xs text-red-500 mt-1 flex items-center"><AlertCircle className="w-3.5 h-3.5 mr-1" />{errors.name}</p>}
            </div>

            {/* Date of Birth */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Date of Birth (DOB) <span className="text-red-500">*</span>
              </label>
              <div className="flex items-center space-x-2">
                <input
                  type="date"
                  value={dob}
                  onChange={(e) => setDob(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition"
                />
                <span className="shrink-0 bg-slate-100 text-slate-800 text-xs font-semibold px-3 py-2.5 rounded-xl border border-slate-200">
                  {currentAge} Yrs
                </span>
              </div>
              {errors.dob && <p className="text-xs text-red-500 mt-1">{errors.dob}</p>}
            </div>

            {/* Social Category */}
            <div className="sm:col-span-2">
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Reservation / Social Category (Applies Age Relaxations in Govt Exams)
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                {SOCIAL_CATEGORIES.map((cat) => (
                  <button
                    type="button"
                    key={cat.value}
                    onClick={() => setSocialCategory(cat.value as SocialCategory)}
                    className={`px-3 py-2.5 rounded-xl text-xs font-medium border text-left transition ${
                      socialCategory === cat.value
                        ? "bg-amber-50 border-amber-500 text-amber-950 font-bold ring-2 ring-amber-200"
                        : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100"
                    }`}
                  >
                    <div className="font-bold">{cat.label.split("(")[0]}</div>
                    <div className="text-[10px] text-slate-500 mt-0.5">
                      {cat.relaxation > 0 ? `+${cat.relaxation} yrs relaxation` : "Standard limit"}
                    </div>
                  </button>
                ))}
              </div>
              {categoryInfo && categoryInfo.relaxation > 0 && (
                <p className="text-xs text-amber-800 bg-amber-50 border border-amber-200 rounded-lg p-2 mt-2 flex items-center">
                  <ShieldAlert className="w-4 h-4 mr-1.5 shrink-0 text-amber-600" />
                  Category Relaxation Active: +{categoryInfo.relaxation} years extension will automatically be applied during age eligibility evaluation for Govt recruitment.
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Section 2: Education & Stream */}
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center mb-4">
            <span className="w-7 h-7 rounded-lg bg-amber-100 text-amber-800 font-extrabold text-sm flex items-center justify-center mr-2">2</span>
            Education Qualification & Stream
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {/* Education Level */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Current / Highest Education Level
              </label>
              <select
                value={educationLevel}
                onChange={(e) => setEducationLevel(e.target.value as EducationLevel)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition bg-white"
              >
                {EDUCATION_LEVEL_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Stream */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Academic Stream / Specialization
              </label>
              <select
                value={stream}
                onChange={(e) => setStream(e.target.value as StreamType)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition bg-white"
              >
                {STREAM_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Section 3: Sector & Location Preferences */}
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center mb-4">
            <span className="w-7 h-7 rounded-lg bg-amber-100 text-amber-800 font-extrabold text-sm flex items-center justify-center mr-2">3</span>
            Sector, State & Salary Preferences
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
            {/* Sector Preference */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Sector Focus
              </label>
              <div className="flex rounded-xl p-1 bg-slate-100 border border-slate-200">
                <button
                  type="button"
                  onClick={() => setSectorPreference("BOTH")}
                  className={`flex-1 py-1.5 text-xs font-bold rounded-lg transition ${
                    sectorPreference === "BOTH" ? "bg-white text-slate-900 shadow" : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  Govt + Private
                </button>
                <button
                  type="button"
                  onClick={() => setSectorPreference("GOVT")}
                  className={`flex-1 py-1.5 text-xs font-bold rounded-lg transition ${
                    sectorPreference === "GOVT" ? "bg-amber-500 text-slate-950 shadow" : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  Govt Only
                </button>
                <button
                  type="button"
                  onClick={() => setSectorPreference("PRIVATE")}
                  className={`flex-1 py-1.5 text-xs font-bold rounded-lg transition ${
                    sectorPreference === "PRIVATE" ? "bg-indigo-600 text-white shadow" : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  Private Only
                </button>
              </div>
            </div>

            {/* Target Location / State */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Target Location / State PSC Focus
              </label>
              <select
                value={targetState}
                onChange={(e) => setTargetState(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition bg-white"
              >
                {INDIAN_STATES_AND_UTS.map((st) => (
                  <option key={st} value={st}>
                    {st}
                  </option>
                ))}
              </select>
            </div>

            {/* Salary Band */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Target Monthly Salary Goal
              </label>
              <select
                value={salaryBand}
                onChange={(e) => setSalaryBand(e.target.value as any)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition bg-white"
              >
                <option value="25k_50k">₹25,000 – ₹50,000 / month (~₹3-6 LPA)</option>
                <option value="50k_1L">₹50,000 – ₹1,000,000 / month (~₹6-12 LPA)</option>
                <option value="1L_PLUS">₹1,00,000+ / month (₹12 LPA+ High Tier)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 4: Domain Selection */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-bold text-slate-900 flex items-center">
              <span className="w-7 h-7 rounded-lg bg-amber-100 text-amber-800 font-extrabold text-sm flex items-center justify-center mr-2">4</span>
              Preferred Career Domains (Multi-Select)
            </h2>
            <span className="text-xs font-medium text-slate-500">
              {selectedDomains.length} domain(s) chosen
            </span>
          </div>

          <div className="flex flex-wrap gap-2 pt-2">
            {CAREER_DOMAINS.map((domain) => {
              const isSelected = selectedDomains.includes(domain);
              return (
                <button
                  type="button"
                  key={domain}
                  onClick={() => toggleDomain(domain)}
                  className={`px-3.5 py-2 rounded-xl text-xs font-medium transition border flex items-center space-x-1.5 ${
                    isSelected
                      ? "bg-slate-900 border-slate-900 text-amber-300 font-bold shadow-sm"
                      : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100"
                  }`}
                >
                  <span>{domain}</span>
                  {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-amber-400 ml-1" />}
                </button>
              );
            })}
          </div>
          {errors.domains && <p className="text-xs text-red-500 mt-2">{errors.domains}</p>}
        </div>

        {/* Submit CTA */}
        <div className="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-xs text-slate-500 flex items-center space-x-1.5">
            <span>🔒 Automatically cross-references 2025–2026 UPSC, SSC, RRB & PSU eligibility criteria.</span>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold text-sm shadow-lg shadow-amber-500/20 hover:shadow-amber-500/30 transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <span>{isSubmitting ? "Generating AI Roadmaps..." : "Generate AI Career Roadmap"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

      </form>
    </div>
  );
};
