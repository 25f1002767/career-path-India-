import React, { useState } from "react";
import { CareerPath, UserProfile } from "../types/career";
import {
  X,
  Sparkles,
  Download,
  ExternalLink,
  ShieldCheck,
  ShieldAlert,
  Calendar,
  CheckCircle2,
  Clock,
  Landmark,
  Building2,
  IndianRupee,
  BookOpen,
  Users,
  Target,
  AlertTriangle,
  Award,
  ChevronRight,
} from "lucide-react";
import { checkAgeEligibility } from "../utils/ageCalculator";
import { generateCareerRoadmapPDF } from "../utils/pdfExport";

interface CareerDetailModalProps {
  career: CareerPath | null;
  profile: UserProfile | null;
  onClose: () => void;
  isBookmarked: boolean;
  onToggleBookmark: (career: CareerPath) => void;
}

export const CareerDetailModal: React.FC<CareerDetailModalProps> = ({
  career,
  profile,
  onClose,
  isBookmarked,
  onToggleBookmark,
}) => {
  if (!career) return null;

  const [activeTab, setActiveTab] = useState<"ROADMAP" | "ELIGIBILITY" | "COMPETITION" | "EXAM_TIMELINE">("ROADMAP");

  const userAge = profile?.age || 21;
  const userCategory = profile?.socialCategory || "GENERAL";
  const ageStatus = checkAgeEligibility(userAge, career.eligibility, userCategory);

  const handleExportPDF = () => {
    generateCareerRoadmapPDF(career, profile || undefined);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm overflow-y-auto">
      <div
        className="bg-white w-full max-w-4xl rounded-3xl border border-slate-200 shadow-2xl overflow-hidden flex flex-col max-h-[90vh] my-auto animate-in fade-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Top Header */}
        <div className="bg-slate-900 text-white p-6 relative">
          <button
            onClick={onClose}
            className="absolute right-5 top-5 p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition"
          >
            <X className="w-5 h-5" />
          </button>

          <div className="flex flex-wrap items-center gap-2 mb-3">
            <span className="bg-amber-500 text-slate-950 text-xs font-extrabold px-2.5 py-0.5 rounded-md uppercase tracking-wide">
              {career.tier} TIER
            </span>
            <span className="bg-slate-800 text-slate-200 text-xs font-semibold px-2.5 py-0.5 rounded-md flex items-center space-x-1">
              {career.sector === "GOVT" ? <Landmark className="w-3.5 h-3.5 mr-1 text-amber-400" /> : <Building2 className="w-3.5 h-3.5 mr-1 text-indigo-400" />}
              <span>{career.sector} SECTOR</span>
            </span>
            <span className="bg-slate-800/80 text-amber-300 text-xs font-medium px-2.5 py-0.5 rounded-md">
              {career.domain}
            </span>
            {career.stateSpecific && (
              <span className="bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-semibold px-2.5 py-0.5 rounded-md">
                {career.stateSpecific}
              </span>
            )}
          </div>

          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white mb-2">
            {career.title}
          </h2>
          <p className="text-slate-300 text-xs sm:text-sm max-w-2xl leading-relaxed">
            {career.shortDescription}
          </p>

          {/* Action Header Buttons */}
          <div className="flex flex-wrap items-center gap-3 mt-5">
            <button
              onClick={handleExportPDF}
              className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold text-xs transition flex items-center space-x-1.5 shadow"
            >
              <Download className="w-4 h-4" />
              <span>Download PDF Roadmap</span>
            </button>

            {career.applicationPortalUrl && (
              <a
                href={career.applicationPortalUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs transition flex items-center space-x-1.5 border border-slate-700"
              >
                <span>Official Application Portal</span>
                <ExternalLink className="w-3.5 h-3.5 text-amber-400" />
              </a>
            )}

            <button
              onClick={() => onToggleBookmark(career)}
              className={`px-3 py-2 rounded-xl text-xs font-semibold transition border ${
                isBookmarked
                  ? "bg-amber-500/20 text-amber-300 border-amber-500/40"
                  : "bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700"
              }`}
            >
              {isBookmarked ? "★ Saved in Bookmarks" : "☆ Save Career"}
            </button>
          </div>
        </div>

        {/* Modal Navigation Tabs */}
        <div className="flex items-center space-x-2 border-b border-slate-200 bg-slate-50 px-6 pt-3 overflow-x-auto">
          <button
            onClick={() => setActiveTab("ROADMAP")}
            className={`pb-3 px-3 text-xs sm:text-sm font-bold border-b-2 transition shrink-0 ${
              activeTab === "ROADMAP"
                ? "border-amber-500 text-amber-600"
                : "border-transparent text-slate-500 hover:text-slate-900"
            }`}
          >
            Roadmap Steps ({career.roadmapSteps.length})
          </button>

          <button
            onClick={() => setActiveTab("ELIGIBILITY")}
            className={`pb-3 px-3 text-xs sm:text-sm font-bold border-b-2 transition shrink-0 ${
              activeTab === "ELIGIBILITY"
                ? "border-amber-500 text-amber-600"
                : "border-transparent text-slate-500 hover:text-slate-900"
            }`}
          >
            Eligibility & Age Check
          </button>

          <button
            onClick={() => setActiveTab("COMPETITION")}
            className={`pb-3 px-3 text-xs sm:text-sm font-bold border-b-2 transition shrink-0 ${
              activeTab === "COMPETITION"
                ? "border-amber-500 text-amber-600"
                : "border-transparent text-slate-500 hover:text-slate-900"
            }`}
          >
            Competition Stats
          </button>

          <button
            onClick={() => setActiveTab("EXAM_TIMELINE")}
            className={`pb-3 px-3 text-xs sm:text-sm font-bold border-b-2 transition shrink-0 ${
              activeTab === "EXAM_TIMELINE"
                ? "border-amber-500 text-amber-600"
                : "border-transparent text-slate-500 hover:text-slate-900"
            }`}
          >
            2025–2026 Exam Timeline
          </button>
        </div>

        {/* Modal Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1">
          
          {/* TAB 1: ROADMAP */}
          {activeTab === "ROADMAP" && (
            <div className="space-y-6">
              <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-start space-x-3">
                <Sparkles className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                <div className="text-xs text-amber-900 leading-relaxed">
                  <span className="font-bold">Preparation Strategy:</span> Follow these chronologically ordered steps to qualify for this career track. Estimated preparation time is realistic for first-time aspirants.
                </div>
              </div>

              <div className="space-y-4">
                {career.roadmapSteps.map((step) => (
                  <div
                    key={step.stepNumber}
                    className="flex items-start space-x-4 bg-slate-50 border border-slate-200 rounded-2xl p-4 sm:p-5 hover:border-slate-300 transition"
                  >
                    <div className="w-9 h-9 rounded-xl bg-slate-900 text-amber-300 font-extrabold text-sm flex items-center justify-center shrink-0 shadow">
                      {step.stepNumber}
                    </div>

                    <div className="flex-1">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-1">
                        <h4 className="text-sm sm:text-base font-bold text-slate-900">
                          {step.title}
                        </h4>
                        {step.estimatedDuration && (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-[11px] font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200 shrink-0">
                            <Clock className="w-3 h-3 mr-1" />
                            {step.estimatedDuration}
                          </span>
                        )}
                      </div>

                      <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        {step.description}
                      </p>

                      {step.keyResources && step.keyResources.length > 0 && (
                        <div className="mt-2.5 pt-2 border-t border-slate-200/60 flex flex-wrap gap-1.5">
                          {step.keyResources.map((res, i) => (
                            <span key={i} className="text-[10px] font-medium text-slate-600 bg-white border border-slate-200 px-2 py-0.5 rounded-md">
                              📚 {res}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* Career Growth Prospects */}
              {career.growthProspects && (
                <div className="bg-slate-900 text-white rounded-2xl p-5 border border-slate-800">
                  <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2 flex items-center">
                    <Award className="w-4 h-4 mr-1.5" /> Promotion & Career Advancement Ladder
                  </h4>
                  <p className="text-xs sm:text-sm text-slate-200 font-medium leading-relaxed">
                    {career.growthProspects}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* TAB 2: ELIGIBILITY & AGE */}
          {activeTab === "ELIGIBILITY" && (
            <div className="space-y-6">
              
              {/* User Age Check Card */}
              <div className={`p-5 rounded-2xl border ${
                ageStatus.isEligible ? "bg-emerald-50 border-emerald-200 text-emerald-950" : "bg-rose-50 border-rose-200 text-rose-950"
              }`}>
                <div className="flex items-center space-x-2 font-bold text-sm sm:text-base mb-1">
                  {ageStatus.isEligible ? (
                    <ShieldCheck className="w-5 h-5 text-emerald-600" />
                  ) : (
                    <ShieldAlert className="w-5 h-5 text-rose-600" />
                  )}
                  <span>Age Eligibility Status for {profile?.name || "Student"} ({userAge} Yrs, Category: {userCategory})</span>
                </div>
                <p className="text-xs leading-relaxed ml-7 font-medium">
                  {ageStatus.statusText}
                </p>
              </div>

              {/* General Eligibility Breakdown */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4">
                  <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                    Required Education
                  </h4>
                  <p className="text-sm font-bold text-slate-900">
                    {career.eligibility.educationRequired}
                  </p>
                  <p className="text-xs text-slate-500 mt-1">
                    Minimum level: <span className="font-semibold text-slate-800">{career.eligibility.minEducationLevel}</span>
                  </p>
                </div>

                <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4">
                  <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                    Age Limits & Cut-offs
                  </h4>
                  {career.eligibility.ageLimit ? (
                    <div>
                      <p className="text-sm font-bold text-slate-900">
                        {career.eligibility.ageLimit.min} to {career.eligibility.ageLimit.max} Years (General)
                      </p>
                      <p className="text-xs text-slate-500 mt-1">
                        Relaxed max age for {userCategory}: <span className="font-semibold text-emerald-700">{ageStatus.maxAgeAllowed} Yrs</span>
                      </p>
                    </div>
                  ) : (
                    <p className="text-sm text-slate-600 font-medium">No strict age cap specified</p>
                  )}
                </div>
              </div>

              {/* Relaxations Table */}
              {career.eligibility.ageLimit?.relaxations && career.eligibility.ageLimit.relaxations.length > 0 && (
                <div className="bg-white border border-slate-200 rounded-2xl p-4">
                  <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3">
                    Category Wise Age Relaxations
                  </h4>
                  <div className="space-y-2">
                    {career.eligibility.ageLimit.relaxations.map((rel, idx) => (
                      <div key={idx} className="flex items-center justify-between text-xs bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                        <span className="font-bold text-slate-900">{rel.category} Category</span>
                        <span className="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                          +{rel.yearsExtention} Years Extension
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Other Criteria */}
              {career.eligibility.otherCriteria && career.eligibility.otherCriteria.length > 0 && (
                <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4">
                  <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                    Other Criteria & Requirements
                  </h4>
                  <ul className="list-disc list-inside text-xs text-slate-600 space-y-1">
                    {career.eligibility.otherCriteria.map((crit, idx) => (
                      <li key={idx}>{crit}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* TAB 3: COMPETITION */}
          {activeTab === "COMPETITION" && (
            <div className="space-y-6">
              {career.competitionStats ? (
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 text-center">
                    <Users className="w-6 h-6 text-indigo-600 mx-auto mb-2" />
                    <div className="text-xs text-slate-500 font-medium">Annual Applicants</div>
                    <div className="text-lg font-extrabold text-slate-900 mt-1">
                      {career.competitionStats.applicants ? career.competitionStats.applicants.toLocaleString("en-IN") : "N/A"}
                    </div>
                  </div>

                  <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 text-center">
                    <Target className="w-6 h-6 text-amber-600 mx-auto mb-2" />
                    <div className="text-xs text-slate-500 font-medium">Seats / Vacancies</div>
                    <div className="text-lg font-extrabold text-slate-900 mt-1">
                      {career.competitionStats.seats ? career.competitionStats.seats.toLocaleString("en-IN") : "N/A"}
                    </div>
                  </div>

                  <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 text-center">
                    <Award className="w-6 h-6 text-emerald-600 mx-auto mb-2" />
                    <div className="text-xs text-slate-500 font-medium">Selection Ratio</div>
                    <div className="text-lg font-extrabold text-slate-900 mt-1">
                      {career.competitionStats.ratio || "N/A"}
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-xs text-slate-500">No competition statistics available.</p>
              )}

              {/* Salary Breakdown */}
              <div className="bg-slate-900 text-white rounded-2xl p-5">
                <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2 flex items-center">
                  <IndianRupee className="w-4 h-4 mr-1" /> Compensation & Pay Scale
                </h4>
                <div className="text-2xl font-extrabold text-white mb-1">
                  ₹{(career.salaryRange.min/1000).toFixed(0)}k – ₹{(career.salaryRange.max/1000).toFixed(0)}k / month
                </div>
                {career.salaryRange.payScaleCode && (
                  <p className="text-xs text-slate-300">
                    Pay Scale Code: <span className="text-amber-200 font-semibold">{career.salaryRange.payScaleCode}</span>
                  </p>
                )}
              </div>
            </div>
          )}

          {/* TAB 4: EXAM TIMELINE */}
          {activeTab === "EXAM_TIMELINE" && (
            <div className="space-y-6">
              <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5 space-y-4">
                <div className="flex items-center space-x-3 text-slate-900 font-bold text-base">
                  <Calendar className="w-5 h-5 text-amber-500" />
                  <span>2025–2026 Examination Schedule</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                  <div className="bg-white p-3 rounded-xl border border-slate-200">
                    <div className="text-slate-400 font-medium">Notification Month</div>
                    <div className="text-sm font-bold text-slate-900 mt-1">
                      {career.examTimeline?.notificationMonth || "Annual"}
                    </div>
                  </div>

                  <div className="bg-white p-3 rounded-xl border border-slate-200">
                    <div className="text-slate-400 font-medium">Exam Conduct Month</div>
                    <div className="text-sm font-bold text-slate-900 mt-1">
                      {career.examTimeline?.examMonth || "As announced in official calendar"}
                    </div>
                  </div>

                  <div className="bg-white p-3 rounded-xl border border-slate-200">
                    <div className="text-slate-400 font-medium">Frequency</div>
                    <div className="text-sm font-bold text-slate-900 mt-1">
                      {career.examTimeline?.frequency || "Annual"}
                    </div>
                  </div>

                  <div className="bg-white p-3 rounded-xl border border-slate-200">
                    <div className="text-slate-400 font-medium">Application Fee</div>
                    <div className="text-sm font-bold text-slate-900 mt-1">
                      {career.examTimeline?.applicationFee || "₹100 (Exempted for SC/ST/Female)"}
                    </div>
                  </div>
                </div>
              </div>

              {/* Grounded Sources */}
              {career.sources && career.sources.length > 0 && (
                <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4">
                  <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                    Verified Grounded Sources
                  </h4>
                  <div className="space-y-2">
                    {career.sources.map((src, i) => (
                      <a
                        key={i}
                        href={src.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center justify-between text-xs text-amber-700 hover:text-amber-800 bg-white p-2.5 rounded-xl border border-slate-200 transition group"
                      >
                        <span className="font-semibold truncate">{src.title}</span>
                        <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-amber-600 shrink-0 ml-2" />
                      </a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Footer Disclaimer */}
          <div className="pt-4 border-t border-slate-100 text-[11px] text-slate-500 flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0" />
            <span>
              Disclaimer: Govt notifications and quotas change. Please verify eligibility & exam dates on official portals. Last checked Aug 2026.
            </span>
          </div>

        </div>

      </div>
    </div>
  );
};
