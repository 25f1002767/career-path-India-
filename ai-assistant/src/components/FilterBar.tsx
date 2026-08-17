import React from "react";
import { FilterState } from "../types/career";
import { CAREER_DOMAINS } from "../data/indianStates";
import { Search, ShieldCheck, SlidersHorizontal, ArrowUpDown, Sparkles } from "lucide-react";

interface FilterBarProps {
  filter: FilterState;
  setFilter: React.Dispatch<React.SetStateAction<FilterState>>;
  totalResultsCount: number;
  userDomains?: string[];
}

export const FilterBar: React.FC<FilterBarProps> = ({
  filter,
  setFilter,
  totalResultsCount,
  userDomains,
}) => {
  const hasUserDomains = userDomains && userDomains.length > 0;
  const availableDomains = hasUserDomains ? userDomains : CAREER_DOMAINS;
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs mb-6 space-y-4">
      {/* Top Row: Search input + Domain Dropdown + Sorting */}
      <div className="flex flex-col md:flex-row items-center gap-3">
        {/* Search */}
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
          <input
            type="text"
            value={filter.searchQuery}
            onChange={(e) => setFilter((prev) => ({ ...prev, searchQuery: e.target.value }))}
            placeholder="Search exam (UPSC, SSC, SDE, Bank PO, ISRO, IAS...)"
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 text-xs sm:text-sm focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition"
          />
        </div>

        {/* Domain Filter */}
        <div className="w-full md:w-60">
          <select
            value={filter.domain}
            onChange={(e) => setFilter((prev) => ({ ...prev, domain: e.target.value }))}
            className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs sm:text-sm focus:outline-none focus:border-blue-600 transition bg-white"
          >
            <option value="ALL">
              {hasUserDomains
                ? userDomains.length === 1
                  ? `Selected Domain (${userDomains[0]})`
                  : `All Selected Domains (${userDomains.length})`
                : "All Career Domains"}
            </option>
            {availableDomains.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </div>

        {/* Sort By */}
        <div className="w-full md:w-52 flex items-center space-x-1.5">
          <ArrowUpDown className="w-4 h-4 text-slate-400 shrink-0 hidden sm:block" />
          <select
            value={filter.sortBy}
            onChange={(e) => setFilter((prev) => ({ ...prev, sortBy: e.target.value as any }))}
            className="w-full px-3 py-2 rounded-xl border border-slate-200 text-xs sm:text-sm focus:outline-none focus:border-blue-600 transition bg-white"
          >
            <option value="RECOMMENDED">Recommended Match</option>
            <option value="SALARY_HIGH">Salary: High to Low</option>
            <option value="COMPETITION_LOW">Competition: Easier Ratio</option>
            <option value="DURATION_SHORT">Prep Duration: Shortest</option>
          </select>
        </div>
      </div>

      {/* Bottom Row: Sector Tabs & Tier Chips */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3 pt-2 border-t border-slate-100">
        
        {/* Sector Tabs */}
        <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-xl">
          <button
            onClick={() => setFilter((prev) => ({ ...prev, sector: "ALL" }))}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
              filter.sector === "ALL" ? "bg-white text-slate-900 shadow-xs" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            All Sectors
          </button>
          <button
            onClick={() => setFilter((prev) => ({ ...prev, sector: "GOVT" }))}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
              filter.sector === "GOVT" ? "bg-blue-600 text-white shadow-xs" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Govt Jobs
          </button>
          <button
            onClick={() => setFilter((prev) => ({ ...prev, sector: "PRIVATE" }))}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
              filter.sector === "PRIVATE" ? "bg-slate-900 text-white shadow-xs" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Private Tech/Corp
          </button>
        </div>

        {/* Tier Badges */}
        <div className="flex items-center space-x-1.5 overflow-x-auto pb-1 lg:pb-0">
          <button
            onClick={() => setFilter((prev) => ({ ...prev, tier: "ALL" }))}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition ${
              filter.tier === "ALL"
                ? "bg-slate-900 text-white border-slate-900"
                : "bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100"
            }`}
          >
            All Tiers
          </button>

          <button
            onClick={() => setFilter((prev) => ({ ...prev, tier: "ELITE" }))}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition flex items-center space-x-1 ${
              filter.tier === "ELITE"
                ? "bg-purple-600 text-white border-purple-600 font-bold"
                : "bg-purple-50 text-purple-900 border-purple-200 hover:bg-purple-100"
            }`}
          >
            <Sparkles className="w-3 h-3 text-purple-600" />
            <span>Elite</span>
          </button>

          <button
            onClick={() => setFilter((prev) => ({ ...prev, tier: "STABLE" }))}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition ${
              filter.tier === "STABLE"
                ? "bg-teal-600 text-white border-teal-600 font-bold"
                : "bg-teal-50 text-teal-900 border-teal-200 hover:bg-teal-100"
            }`}
          >
            Stable Core
          </button>

          <button
            onClick={() => setFilter((prev) => ({ ...prev, tier: "HIDDEN_GEM" }))}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition ${
              filter.tier === "HIDDEN_GEM"
                ? "bg-amber-500 text-slate-950 border-amber-500 font-bold"
                : "bg-amber-50 text-amber-900 border-amber-200 hover:bg-amber-100"
            }`}
          >
            Hidden Gems 💎
          </button>
        </div>

        {/* Eligibility Only Toggle */}
        <button
          onClick={() =>
            setFilter((prev) => ({
              ...prev,
              eligibilityFilter: prev.eligibilityFilter === "ALL" ? "ELIGIBLE_ONLY" : "ALL",
            }))
          }
          className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition flex items-center space-x-1.5 ${
            filter.eligibilityFilter === "ELIGIBLE_ONLY"
              ? "bg-emerald-600 text-white border-emerald-600 shadow-xs"
              : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
          }`}
        >
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>{filter.eligibilityFilter === "ELIGIBLE_ONLY" ? "Eligible Only" : "Show All Ages"}</span>
        </button>

      </div>
    </div>
  );
};
