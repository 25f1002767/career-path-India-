import React from "react";
import { CareerPath, UserProfile } from "../types/career";
import { CareerCard } from "./CareerCard";
import { Bookmark, Download, Trash2, Compass, ShieldCheck } from "lucide-react";
import { generateCareerRoadmapPDF } from "../utils/pdfExport";

interface BookmarksViewProps {
  bookmarkedCareers: CareerPath[];
  profile: UserProfile | null;
  onSelectCareer: (career: CareerPath) => void;
  onToggleBookmark: (career: CareerPath) => void;
  comparedIds: string[];
  onToggleCompare: (career: CareerPath) => void;
  onClearBookmarks: () => void;
}

export const BookmarksView: React.FC<BookmarksViewProps> = ({
  bookmarkedCareers,
  profile,
  onSelectCareer,
  onToggleBookmark,
  comparedIds,
  onToggleCompare,
  onClearBookmarks,
}) => {
  if (bookmarkedCareers.length === 0) {
    return (
      <div className="max-w-4xl mx-auto py-16 px-4 text-center">
        <div className="w-16 h-16 bg-amber-50 rounded-2xl flex items-center justify-center mx-auto mb-4 text-amber-600 border border-amber-200">
          <Bookmark className="w-8 h-8" />
        </div>
        <h3 className="text-xl font-bold text-slate-900 mb-2">No Saved Careers Yet</h3>
        <p className="text-sm text-slate-500 max-w-md mx-auto mb-6">
          Bookmark career options while browsing recommendations to build your offline preparation shortlist.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 text-white rounded-3xl p-6 shadow-xl border border-slate-800">
        <div>
          <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30 mb-2">
            <Bookmark className="w-3.5 h-3.5 mr-1.5 fill-amber-400" /> Saved Career Shortlist
          </div>
          <h1 className="text-2xl font-extrabold text-white">
            {bookmarkedCareers.length} Saved Career Roadmaps
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Access your saved career paths anytime. Syncs across browser sessions.
          </p>
        </div>

        <button
          onClick={onClearBookmarks}
          className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold transition flex items-center space-x-1.5 shrink-0 border border-slate-700"
        >
          <Trash2 className="w-3.5 h-3.5 text-rose-400" />
          <span>Clear All Saved</span>
        </button>
      </div>

      {/* Grid of Saved Career Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {bookmarkedCareers.map((career) => (
          <CareerCard
            key={career.id}
            career={career}
            profile={profile}
            onSelect={onSelectCareer}
            isBookmarked={true}
            onToggleBookmark={onToggleBookmark}
            isCompared={comparedIds.includes(career.id)}
            onToggleCompare={onToggleCompare}
          />
        ))}
      </div>
    </div>
  );
};
