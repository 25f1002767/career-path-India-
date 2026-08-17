import React, { useState } from "react";
import { CareerPath } from "../types/career";
import { Calendar, ExternalLink, ChevronRight, Landmark, Building2, Search, Filter } from "lucide-react";

interface ExamCalendarViewProps {
  careers: CareerPath[];
  onSelectCareer: (career: CareerPath) => void;
}

const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
  "Year-round",
];

export const ExamCalendarView: React.FC<ExamCalendarViewProps> = ({
  careers,
  onSelectCareer,
}) => {
  const [selectedMonth, setSelectedMonth] = useState<string>("ALL");
  const [sectorFilter, setSectorFilter] = useState<"ALL" | "GOVT" | "PRIVATE">("ALL");

  const filteredCareers = careers.filter((c) => {
    if (sectorFilter !== "ALL" && c.sector !== sectorFilter) return false;
    
    if (selectedMonth !== "ALL") {
      const notif = (c.examTimeline?.notificationMonth || "").toLowerCase();
      if (!notif.includes(selectedMonth.toLowerCase()) && selectedMonth !== "Year-round") {
        return false;
      }
    }
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-8">
      {/* Header Banner */}
      <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30 mb-3">
              <Calendar className="w-3.5 h-3.5 mr-1.5" /> 2025–2026 Official Exam Cycle
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
              Annual Recruitment Exam Calendar
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-xl">
              Track official notification months, application form deadlines, and exam schedules across UPSC, SSC, Banking, Railways, State PSC, and Private Tech hiring.
            </p>
          </div>

          <div className="flex items-center space-x-2 bg-slate-800 p-1.5 rounded-2xl border border-slate-700 shrink-0">
            <button
              onClick={() => setSectorFilter("ALL")}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition ${
                sectorFilter === "ALL" ? "bg-amber-500 text-slate-950 shadow" : "text-slate-300 hover:text-white"
              }`}
            >
              All
            </button>
            <button
              onClick={() => setSectorFilter("GOVT")}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition ${
                sectorFilter === "GOVT" ? "bg-amber-500 text-slate-950 shadow" : "text-slate-300 hover:text-white"
              }`}
            >
              Govt Exams
            </button>
            <button
              onClick={() => setSectorFilter("PRIVATE")}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition ${
                sectorFilter === "PRIVATE" ? "bg-indigo-600 text-white shadow" : "text-slate-300 hover:text-white"
              }`}
            >
              Private Hiring
            </button>
          </div>
        </div>

        {/* Month Selector Carousel */}
        <div className="mt-6 pt-6 border-t border-slate-800 flex items-center space-x-2 overflow-x-auto pb-2">
          <button
            onClick={() => setSelectedMonth("ALL")}
            className={`px-4 py-2 rounded-xl text-xs font-extrabold transition shrink-0 ${
              selectedMonth === "ALL"
                ? "bg-amber-500 text-slate-950 shadow"
                : "bg-slate-800 text-slate-300 hover:bg-slate-700"
            }`}
          >
            All Months ({careers.length})
          </button>

          {MONTHS.map((m) => {
            const count = careers.filter((c) =>
              (c.examTimeline?.notificationMonth || "").toLowerCase().includes(m.toLowerCase())
            ).length;

            return (
              <button
                key={m}
                onClick={() => setSelectedMonth(m)}
                className={`px-3.5 py-2 rounded-xl text-xs font-bold transition shrink-0 flex items-center space-x-1.5 ${
                  selectedMonth === m
                    ? "bg-amber-500 text-slate-950 shadow"
                    : "bg-slate-800 text-slate-300 hover:bg-slate-700"
                }`}
              >
                <span>{m}</span>
                {count > 0 && (
                  <span className="bg-slate-900/60 px-1.5 py-0.5 rounded text-[10px] font-mono">
                    {count}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Calendar List View */}
      <div className="space-y-4">
        {filteredCareers.map((career) => (
          <div
            key={career.id}
            className="bg-white rounded-2xl border border-slate-200 p-5 hover:border-slate-300 shadow-sm transition flex flex-col md:flex-row md:items-center justify-between gap-4"
          >
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-800 font-extrabold text-xs flex flex-col items-center justify-center border border-amber-200 shrink-0 text-center p-1">
                <Calendar className="w-4 h-4 text-amber-600 mb-0.5" />
                <span className="truncate max-w-[44px]">
                  {career.examTimeline?.notificationMonth?.split(" ")[0] || "Annual"}
                </span>
              </div>

              <div>
                <div className="flex flex-wrap items-center gap-1.5 mb-1">
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                    {career.domain}
                  </span>
                  <span
                    className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded ${
                      career.sector === "GOVT"
                        ? "bg-amber-100 text-amber-900"
                        : "bg-indigo-100 text-indigo-900"
                    }`}
                  >
                    {career.sector}
                  </span>
                  <span className="text-[10px] font-semibold text-slate-500">
                    Freq: {career.examTimeline?.frequency || "Annual"}
                  </span>
                </div>

                <h3
                  onClick={() => onSelectCareer(career)}
                  className="text-base font-bold text-slate-900 hover:text-amber-600 transition cursor-pointer"
                >
                  {career.title}
                </h3>

                <p className="text-xs text-slate-600 mt-0.5">
                  Exam Month: <span className="font-semibold text-slate-800">{career.examTimeline?.examMonth || "As per official schedule"}</span> | Fee: {career.examTimeline?.applicationFee || "Standard"}
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2 shrink-0 border-t md:border-t-0 pt-3 md:pt-0 border-slate-100">
              {career.applicationPortalUrl && (
                <a
                  href={career.applicationPortalUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold transition flex items-center space-x-1"
                >
                  <span>Portal</span>
                  <ExternalLink className="w-3.5 h-3.5 text-slate-500" />
                </a>
              )}

              <button
                onClick={() => onSelectCareer(career)}
                className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-amber-500 hover:text-slate-950 text-white font-bold text-xs transition flex items-center space-x-1"
              >
                <span>Full Roadmap</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
