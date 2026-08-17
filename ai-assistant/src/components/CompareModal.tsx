import React from "react";
import { CareerPath, UserProfile } from "../types/career";
import { X, Scale, Sparkles, Download, CheckCircle2, IndianRupee, Calendar, Clock, Award, ShieldCheck, Trash2 } from "lucide-react";
import { generateCareerRoadmapPDF } from "../utils/pdfExport";

interface CompareModalProps {
  comparedCareers: CareerPath[];
  profile: UserProfile | null;
  onRemoveFromCompare: (careerId: string) => void;
  onClearAll: () => void;
  onSelectCareer: (career: CareerPath) => void;
}

export const CompareModal: React.FC<CompareModalProps> = ({
  comparedCareers,
  profile,
  onRemoveFromCompare,
  onClearAll,
  onSelectCareer,
}) => {
  if (comparedCareers.length === 0) {
    return (
      <div className="max-w-4xl mx-auto py-16 px-4 text-center">
        <div className="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-4 text-slate-400">
          <Scale className="w-8 h-8" />
        </div>
        <h3 className="text-xl font-bold text-slate-900 mb-2">No Careers Selected for Comparison</h3>
        <p className="text-sm text-slate-500 max-w-md mx-auto mb-6">
          Click the comparison scale icon <Scale className="w-4 h-4 inline text-indigo-600" /> on any career card to compare salary, exam timelines, competition ratios, and age limits side-by-side.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 text-white rounded-3xl p-6 shadow-xl border border-slate-800">
        <div>
          <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 mb-2">
            <Scale className="w-3.5 h-3.5 mr-1.5" /> Side-by-Side Career Matrix
          </div>
          <h1 className="text-2xl font-extrabold text-white">
            Comparing {comparedCareers.length} Career Tracks
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Compare salary ranges, competition ratios, prep duration, and exam cycles.
          </p>
        </div>

        <button
          onClick={onClearAll}
          className="px-4 py-2 rounded-xl bg-rose-500/20 text-rose-300 hover:bg-rose-500/30 border border-rose-500/40 text-xs font-bold transition flex items-center space-x-1.5 shrink-0"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>Clear Comparison</span>
        </button>
      </div>

      {/* Side by Side Matrix Table */}
      <div className="bg-white border border-slate-200 rounded-3xl shadow-md overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[700px]">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50">
              <th className="p-4 text-xs font-bold text-slate-500 uppercase tracking-wider w-48 sticky left-0 bg-slate-50">
                Attribute
              </th>
              {comparedCareers.map((c) => (
                <th key={c.id} className="p-4 min-w-[240px] align-top">
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-amber-100 text-amber-900 border border-amber-300/50">
                        {c.tier}
                      </span>
                      <h3
                        onClick={() => onSelectCareer(c)}
                        className="text-base font-bold text-slate-900 hover:text-amber-600 transition cursor-pointer mt-1"
                      >
                        {c.title}
                      </h3>
                    </div>
                    <button
                      onClick={() => onRemoveFromCompare(c.id)}
                      className="text-slate-400 hover:text-rose-500 p-1"
                      title="Remove"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </th>
              ))}
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100 text-xs">
            {/* Sector & Domain */}
            <tr>
              <td className="p-4 font-bold text-slate-700 bg-slate-50/50 sticky left-0">Sector & Domain</td>
              {comparedCareers.map((c) => (
                <td key={c.id} className="p-4 font-medium text-slate-800">
                  <div className="font-bold">{c.sector} Sector</div>
                  <div className="text-slate-500">{c.domain}</div>
                </td>
              ))}
            </tr>

            {/* Salary Range */}
            <tr>
              <td className="p-4 font-bold text-slate-700 bg-slate-50/50 sticky left-0">Starting Salary</td>
              {comparedCareers.map((c) => (
                <td key={c.id} className="p-4">
                  <div className="font-extrabold text-slate-900 text-sm">
                    ₹{Math.round(c.salaryRange.min/1000)}k – ₹{Math.round(c.salaryRange.max/1000)}k / pm
                  </div>
                  <div className="text-emerald-700 font-semibold">
                    ~{(c.salaryRange.min * 12 / 100000).toFixed(1)}–{(c.salaryRange.max * 12 / 100000).toFixed(1)} LPA
                  </div>
                </td>
              ))}
            </tr>

            {/* Exam Cycle */}
            <tr>
              <td className="p-4 font-bold text-slate-700 bg-slate-50/50 sticky left-0">Exam Cycle & Fee</td>
              {comparedCareers.map((c) => (
                <td key={c.id} className="p-4 font-medium text-slate-800">
                  <div className="font-bold">{c.examTimeline?.notificationMonth || "Annual"}</div>
                  <div className="text-slate-500">{c.examTimeline?.frequency || "Annual"}</div>
                  <div className="text-slate-500 text-[11px] mt-0.5">{c.examTimeline?.applicationFee || "Fee varies"}</div>
                </td>
              ))}
            </tr>

            {/* Competition Stats */}
            <tr>
              <td className="p-4 font-bold text-slate-700 bg-slate-50/50 sticky left-0">Competition Ratio</td>
              {comparedCareers.map((c) => (
                <td key={c.id} className="p-4 font-medium">
                  <div className="font-extrabold text-slate-900">
                    {c.competitionStats?.ratio || "N/A"}
                  </div>
                  <div className="text-slate-500">
                    Difficulty: <span className="font-semibold text-amber-700">{c.competitionStats?.difficultyRating || "HIGH"}</span>
                  </div>
                </td>
              ))}
            </tr>

            {/* Eligibility & Age Limits */}
            <tr>
              <td className="p-4 font-bold text-slate-700 bg-slate-50/50 sticky left-0">Age Limit & Edu</td>
              {comparedCareers.map((c) => (
                <td key={c.id} className="p-4 text-slate-800">
                  <div className="font-bold">{c.eligibility.educationRequired}</div>
                  <div className="text-slate-500 mt-1">
                    Age: {c.eligibility.ageLimit ? `${c.eligibility.ageLimit.min}–${c.eligibility.ageLimit.max} Yrs` : "N/A"}
                  </div>
                </td>
              ))}
            </tr>

            {/* Roadmap Steps Count */}
            <tr>
              <td className="p-4 font-bold text-slate-700 bg-slate-50/50 sticky left-0">Roadmap Steps</td>
              {comparedCareers.map((c) => (
                <td key={c.id} className="p-4">
                  <div className="font-bold text-slate-900">{c.roadmapSteps.length} Milestones</div>
                  <button
                    onClick={() => onSelectCareer(c)}
                    className="text-amber-600 font-bold hover:underline mt-1 block"
                  >
                    View Roadmap ➔
                  </button>
                </td>
              ))}
            </tr>

            {/* Action Row */}
            <tr>
              <td className="p-4 font-bold text-slate-700 bg-slate-50/50 sticky left-0">Export PDF</td>
              {comparedCareers.map((c) => (
                <td key={c.id} className="p-4">
                  <button
                    onClick={() => generateCareerRoadmapPDF(c, profile || undefined)}
                    className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-amber-500 hover:text-slate-950 text-white font-bold text-xs transition flex items-center space-x-1"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Download PDF</span>
                  </button>
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
