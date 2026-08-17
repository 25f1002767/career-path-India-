import React, { useState } from "react";
import { CareerPath, SocialCategory } from "../types/career";
import { SOCIAL_CATEGORIES } from "../data/indianStates";
import { calculateAge, checkAgeEligibility } from "../utils/ageCalculator";
import { ShieldCheck, ShieldAlert, Calendar, User, Search, CheckCircle2, ChevronRight, Award } from "lucide-react";

interface AgeCalculatorViewProps {
  careers: CareerPath[];
  onSelectCareer: (career: CareerPath) => void;
}

export const AgeCalculatorView: React.FC<AgeCalculatorViewProps> = ({
  careers,
  onSelectCareer,
}) => {
  const [dob, setDob] = useState("2003-06-15"); // ~23 yrs
  const [category, setCategory] = useState<SocialCategory>("GENERAL");
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<"ALL" | "ELIGIBLE_ONLY">("ALL");

  const userAge = calculateAge(dob);

  const evaluatedCareers = careers.map((career) => {
    const status = checkAgeEligibility(userAge, career.eligibility, category);
    return {
      career,
      status,
    };
  });

  const filtered = evaluatedCareers.filter(({ career, status }) => {
    if (statusFilter === "ELIGIBLE_ONLY" && !status.isEligible) return false;
    if (
      search &&
      !career.title.toLowerCase().includes(search.toLowerCase()) &&
      !career.domain.toLowerCase().includes(search.toLowerCase())
    ) {
      return false;
    }
    return true;
  });

  const eligibleCount = evaluatedCareers.filter(({ status }) => status.isEligible).length;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-8">
      {/* Header Banner */}
      <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 mb-3">
              <ShieldCheck className="w-3.5 h-3.5 mr-1.5" /> Instant Age & Cut-off Checker
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
              Age & Category Eligibility Calculator
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-xl">
              Cross-check your exact Date of Birth & Reservation Category against 2025–2026 government cut-off dates and relaxation policies.
            </p>
          </div>

          {/* Quick Stats Pill */}
          <div className="bg-slate-800/80 border border-slate-700 rounded-2xl p-4 text-center shrink-0">
            <div className="text-xs text-slate-400 font-medium">Eligible Recruitment Exams</div>
            <div className="text-2xl font-extrabold text-amber-400 mt-0.5">
              {eligibleCount} / {careers.length} Exams
            </div>
            <div className="text-[10px] text-slate-400 mt-1">Calculated for Age {userAge} Yrs ({category})</div>
          </div>
        </div>

        {/* Input Bar */}
        <div className="mt-6 pt-6 border-t border-slate-800 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* DOB Input */}
          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">
              Select Date of Birth (DOB)
            </label>
            <input
              type="date"
              value={dob}
              onChange={(e) => setDob(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:outline-none focus:border-amber-500 transition"
            />
          </div>

          {/* Category Input */}
          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">
              Reservation Category
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value as SocialCategory)}
              className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:outline-none focus:border-amber-500 transition"
            >
              {SOCIAL_CATEGORIES.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label} ({cat.relaxation > 0 ? `+${cat.relaxation} yrs` : "No extra relaxation"})
                </option>
              ))}
            </select>
          </div>

          {/* Search Filter */}
          <div className="sm:col-span-2 lg:col-span-1">
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">
              Search Exam Title
            </label>
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-500" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Filter by UPSC, SSC, Bank..."
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:outline-none focus:border-amber-500 transition"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setStatusFilter("ALL")}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition border ${
              statusFilter === "ALL"
                ? "bg-slate-900 text-white border-slate-900"
                : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
            }`}
          >
            All Exams ({evaluatedCareers.length})
          </button>

          <button
            onClick={() => setStatusFilter("ELIGIBLE_ONLY")}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition border flex items-center space-x-1.5 ${
              statusFilter === "ELIGIBLE_ONLY"
                ? "bg-emerald-600 text-white border-emerald-600"
                : "bg-emerald-50 text-emerald-900 border-emerald-200 hover:bg-emerald-100"
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Eligible Only ({eligibleCount})</span>
          </button>
        </div>
      </div>

      {/* Results Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map(({ career, status }) => (
          <div
            key={career.id}
            className={`p-5 rounded-2xl border transition-all flex flex-col justify-between ${
              status.isEligible
                ? "bg-white border-slate-200 hover:border-emerald-400 shadow-sm"
                : "bg-slate-50/80 border-slate-200 opacity-80"
            }`}
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700 px-2 py-0.5 rounded">
                  {career.domain}
                </span>

                <span
                  className={`text-[11px] font-extrabold px-2.5 py-0.5 rounded-md flex items-center space-x-1 ${
                    status.isEligible
                      ? "bg-emerald-100 text-emerald-800 border border-emerald-300"
                      : "bg-rose-100 text-rose-800 border border-rose-300"
                  }`}
                >
                  {status.isEligible ? (
                    <>
                      <ShieldCheck className="w-3.5 h-3.5 mr-1" /> Eligible
                    </>
                  ) : (
                    <>
                      <ShieldAlert className="w-3.5 h-3.5 mr-1" /> Ineligible
                    </>
                  )}
                </span>
              </div>

              <h3
                onClick={() => onSelectCareer(career)}
                className="text-base font-bold text-slate-900 hover:text-amber-600 transition cursor-pointer mb-1"
              >
                {career.title}
              </h3>

              <p className="text-xs text-slate-600 line-clamp-2 mb-3">
                {career.shortDescription}
              </p>

              {/* Status explanation */}
              <div
                className={`p-2.5 rounded-xl text-xs font-medium border mb-4 ${
                  status.isEligible
                    ? "bg-emerald-50/50 border-emerald-200/80 text-emerald-900"
                    : "bg-rose-50/50 border-rose-200/80 text-rose-900"
                }`}
              >
                {status.statusText}
              </div>
            </div>

            <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
              <span className="text-slate-500 font-medium">
                Base Limit: {career.eligibility.ageLimit?.min || 18}–{career.eligibility.ageLimit?.max || 30} yrs
              </span>

              <button
                onClick={() => onSelectCareer(career)}
                className="text-amber-600 font-bold hover:underline flex items-center space-x-1"
              >
                <span>Roadmap & Details</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
