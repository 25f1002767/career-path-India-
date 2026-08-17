import React from "react";
import { CareerPath, UserProfile } from "../types/career";
import {
  Sparkles,
  Bookmark,
  Scale,
  Calendar,
  ExternalLink,
  ChevronRight,
  ShieldCheck,
  ShieldAlert,
  Building2,
  Landmark,
  IndianRupee,
  Clock,
  Award,
} from "lucide-react";
import { checkAgeEligibility } from "../utils/ageCalculator";

interface CareerCardProps {
  career: CareerPath;
  profile: UserProfile | null;
  onSelect: (career: CareerPath) => void;
  isBookmarked: boolean;
  onToggleBookmark: (career: CareerPath) => void;
  isCompared: boolean;
  onToggleCompare: (career: CareerPath) => void;
}

export const CareerCard: React.FC<CareerCardProps> = ({
  career,
  profile,
  onSelect,
  isBookmarked,
  onToggleBookmark,
  isCompared,
  onToggleCompare,
}) => {
  const userAge = profile?.age || 21;
  const userCategory = profile?.socialCategory || "GENERAL";
  const ageStatus = checkAgeEligibility(userAge, career.eligibility, userCategory);

  // Format Salary
  const minMin = Math.round(career.salaryRange.min / 1000);
  const maxMax = Math.round(career.salaryRange.max / 1000);
  const minLPA = (career.salaryRange.min * 12 / 100000).toFixed(1);
  const maxLPA = (career.salaryRange.max * 12 / 100000).toFixed(1);

  // Tier Colors
  const tierConfig = {
    ELITE: {
      label: "ELITE TIER",
      stripe: "bg-purple-600",
      badge: "bg-purple-100 text-purple-700 font-bold",
      icon: Sparkles,
    },
    STABLE: {
      label: "STABLE TIER",
      stripe: "bg-teal-500",
      badge: "bg-teal-100 text-teal-700 font-bold",
      icon: Award,
    },
    HIDDEN_GEM: {
      label: "HIDDEN GEM 💎",
      stripe: "bg-amber-500",
      badge: "bg-amber-100 text-amber-800 font-bold",
      icon: Sparkles,
    },
  }[career.tier];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 hover:border-slate-300 shadow-sm hover:shadow-md transition-all flex flex-col justify-between p-6 relative overflow-hidden group">
      
      {/* Left Accent Stripe */}
      <div className={`absolute top-0 left-0 w-1.5 h-full ${tierConfig.stripe}`} />

      {/* Top Header Row */}
      <div className="pl-1">
        <div className="flex items-center justify-between gap-2 mb-3">
          <div className="flex flex-wrap items-center gap-1.5">
            {/* Tier Badge */}
            <span className={`px-2.5 py-1 rounded text-[10px] tracking-wider uppercase ${tierConfig.badge}`}>
              {tierConfig.label}
            </span>

            {/* Sector Badge */}
            <span
              className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider flex items-center space-x-1 ${
                career.sector === "GOVT"
                  ? "bg-slate-100 text-slate-700 border border-slate-200"
                  : "bg-blue-50 text-blue-700 border border-blue-200"
              }`}
            >
              {career.sector === "GOVT" ? (
                <>
                  <Landmark className="w-3 h-3 mr-0.5" /> Govt
                </>
              ) : (
                <>
                  <Building2 className="w-3 h-3 mr-0.5" /> Private
                </>
              )}
            </span>

            {/* State Badge if State Specific */}
            {career.stateSpecific && (
              <span className="bg-slate-100 text-slate-600 text-[10px] font-semibold px-2 py-0.5 rounded border border-slate-200">
                {career.stateSpecific}
              </span>
            )}
          </div>

          {/* Quick Actions (Bookmark & Compare) */}
          <div className="flex items-center space-x-1">
            <button
              onClick={() => onToggleCompare(career)}
              title={isCompared ? "Remove from comparison" : "Add to comparison"}
              className={`p-1.5 rounded-lg text-xs transition ${
                isCompared
                  ? "bg-blue-100 text-blue-700 border border-blue-300"
                  : "text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              }`}
            >
              <Scale className="w-4 h-4" />
            </button>

            <button
              onClick={() => onToggleBookmark(career)}
              title={isBookmarked ? "Remove bookmark" : "Save career path"}
              className={`p-1.5 rounded-lg text-xs transition ${
                isBookmarked
                  ? "bg-blue-100 text-blue-700 border border-blue-300"
                  : "text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              }`}
            >
              <Bookmark className={`w-4 h-4 ${isBookmarked ? "fill-blue-600 text-blue-600" : ""}`} />
            </button>
          </div>
        </div>

        {/* Title & Domain */}
        <div className="mb-2">
          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-0.5">
            {career.domain}
          </div>
          <h3
            onClick={() => onSelect(career)}
            className="text-base sm:text-lg font-bold text-slate-900 group-hover:text-blue-600 transition cursor-pointer leading-snug"
          >
            {career.title}
          </h3>
        </div>

        {/* Short Description */}
        <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed mb-4">
          {career.shortDescription}
        </p>

        {/* Key Attributes Bar */}
        <div className="grid grid-cols-2 gap-2 bg-slate-50 border border-slate-100 rounded-xl p-3 mb-4 text-xs">
          
          {/* Salary */}
          <div>
            <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Monthly Salary</div>
            <div className="font-bold text-slate-900 text-sm flex items-center mt-0.5">
              <span>₹{minMin}k – ₹{maxMax}k</span>
            </div>
            <div className="text-[10px] text-slate-500 font-medium">
              (~{minLPA}–{maxLPA} LPA)
            </div>
          </div>

          {/* Exam Timeline */}
          <div>
            <div className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Notification</div>
            <div className="font-semibold text-slate-800 flex items-center mt-0.5 truncate">
              <Calendar className="w-3.5 h-3.5 mr-1 text-blue-600 shrink-0" />
              <span className="truncate">{career.examTimeline?.notificationMonth || "Annual"}</span>
            </div>
            <div className="text-[10px] text-slate-500 font-medium truncate">
              {career.examTimeline?.frequency || "Annual"}
            </div>
          </div>

        </div>

        {/* Age Eligibility Status Ribbon */}
        <div className="mb-4">
          {ageStatus.isEligible ? (
            <div className="flex items-center text-[11px] font-medium text-emerald-800 bg-emerald-50 border border-emerald-200/80 rounded-lg px-2.5 py-1.5">
              <ShieldCheck className="w-3.5 h-3.5 mr-1.5 text-emerald-600 shrink-0" />
              <span className="truncate">{ageStatus.statusText}</span>
            </div>
          ) : (
            <div className="flex items-center text-[11px] font-medium text-rose-800 bg-rose-50 border border-rose-200/80 rounded-lg px-2.5 py-1.5">
              <ShieldAlert className="w-3.5 h-3.5 mr-1.5 text-rose-600 shrink-0" />
              <span className="truncate">{ageStatus.statusText}</span>
            </div>
          )}
        </div>
      </div>

      {/* Card Footer: Steps Count & CTA */}
      <div className="pl-1 pt-3 border-t border-slate-100 flex items-center justify-between">
        <div className="flex items-center space-x-1 text-xs text-slate-500 font-medium">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span>{career.roadmapSteps.length} Steps</span>
        </div>

        <button
          onClick={() => onSelect(career)}
          className="px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-800 font-semibold text-xs hover:bg-blue-600 hover:text-white hover:border-blue-600 transition-colors flex items-center space-x-1"
        >
          <span>View Roadmap</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
      </div>

    </div>
  );
};
