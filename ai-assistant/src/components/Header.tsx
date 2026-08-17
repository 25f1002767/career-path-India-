import React from "react";
import { Compass, Calendar, Bookmark, Scale, User, Shield, Sparkles, Key } from "lucide-react";
import { UserProfile } from "../types/career";

interface HeaderProps {
  activeTab: "RECOMMENDATIONS" | "AGE_CALCULATOR" | "EXAM_CALENDAR" | "BOOKMARKS" | "COMPARE";
  setActiveTab: (tab: "RECOMMENDATIONS" | "AGE_CALCULATOR" | "EXAM_CALENDAR" | "BOOKMARKS" | "COMPARE") => void;
  profile: UserProfile | null;
  onEditProfile: () => void;
  bookmarksCount: number;
  compareCount: number;
  hasCustomApiKey: boolean;
  onOpenApiKeyModal: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  profile,
  onEditProfile,
  bookmarksCount,
  compareCount,
  hasCustomApiKey,
  onOpenApiKeyModal,
}) => {
  return (
    <header className="bg-white border-b border-slate-200 text-slate-900 sticky top-0 z-30 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo & Name */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab("RECOMMENDATIONS")}>
            <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-sm">
              <Compass className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="font-bold text-lg tracking-tight text-slate-900">
                  CareerPath <span className="text-blue-600">India</span>
                </h1>
                <div className="hidden sm:flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full bg-slate-100 border border-slate-200">
                  <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                  <span className="text-[10px] font-semibold text-slate-600 uppercase tracking-wider">
                    Live Data Active
                  </span>
                </div>
              </div>
              <p className="text-[10px] uppercase tracking-widest text-slate-500 font-semibold hidden sm:block">
                AI-POWERED GUIDANCE ENGINE
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center space-x-1 sm:space-x-1.5">
            <button
              onClick={() => setActiveTab("RECOMMENDATIONS")}
              className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                activeTab === "RECOMMENDATIONS"
                  ? "bg-blue-600 text-white font-bold shadow-xs"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Compass className="w-4 h-4" />
              <span>Roadmaps</span>
            </button>

            <button
              onClick={() => setActiveTab("AGE_CALCULATOR")}
              className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                activeTab === "AGE_CALCULATOR"
                  ? "bg-blue-600 text-white font-bold shadow-xs"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Shield className="w-4 h-4" />
              <span className="hidden md:inline">Age & Eligibility</span>
              <span className="md:hidden">Eligibility</span>
            </button>

            <button
              onClick={() => setActiveTab("EXAM_CALENDAR")}
              className={`flex items-center space-x-1.5 px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                activeTab === "EXAM_CALENDAR"
                  ? "bg-blue-600 text-white font-bold shadow-xs"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Calendar className="w-4 h-4" />
              <span className="hidden md:inline">Exam Calendar</span>
              <span className="md:hidden">Calendar</span>
            </button>

            <button
              onClick={() => setActiveTab("BOOKMARKS")}
              className={`relative flex items-center space-x-1.5 px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                activeTab === "BOOKMARKS"
                  ? "bg-blue-600 text-white font-bold shadow-xs"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Bookmark className="w-4 h-4" />
              <span>Saved</span>
              {bookmarksCount > 0 && (
                <span className={`ml-1 text-[10px] font-extrabold px-1.5 py-0.5 rounded-full ${
                  activeTab === "BOOKMARKS" ? "bg-white text-blue-600" : "bg-blue-100 text-blue-700"
                }`}>
                  {bookmarksCount}
                </span>
              )}
            </button>

            <button
              onClick={() => setActiveTab("COMPARE")}
              className={`relative flex items-center space-x-1.5 px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                activeTab === "COMPARE"
                  ? "bg-blue-600 text-white font-bold shadow-xs"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`}
            >
              <Scale className="w-4 h-4" />
              <span className="hidden sm:inline">Compare</span>
              {compareCount > 0 && (
                <span className={`ml-1 text-[10px] font-extrabold px-1.5 py-0.5 rounded-full ${
                  activeTab === "COMPARE" ? "bg-white text-blue-600" : "bg-blue-100 text-blue-700"
                }`}>
                  {compareCount}
                </span>
              )}
            </button>
          </nav>

          {/* Right Action Group: Settings & Profile Badge */}
          <div className="flex items-center space-x-2">
            <button
              onClick={onOpenApiKeyModal}
              className={`p-2 rounded-lg border text-xs font-semibold transition ${
                hasCustomApiKey
                  ? "bg-amber-50 border-amber-300 text-amber-900 hover:bg-amber-100"
                  : "bg-white border-slate-200 text-slate-500 hover:text-slate-800 hover:bg-slate-50"
              }`}
              title={hasCustomApiKey ? "Custom Gemini Key Active" : "Settings & API Configuration"}
              aria-label="Settings"
            >
              <Key className={`w-4 h-4 ${hasCustomApiKey ? "text-amber-600" : "text-slate-500"}`} />
            </button>

            {/* Profile Badge / Change Profile Button */}
            {profile && (
              <button
                onClick={onEditProfile}
                className="hidden lg:flex items-center space-x-2 bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 px-3 py-1.5 rounded-lg text-xs font-medium transition"
                title="Edit Intake Profile"
              >
                <User className="w-3.5 h-3.5 text-blue-600" />
                <span className="max-w-[100px] truncate font-semibold text-slate-900">{profile.name || "Student"}</span>
                <span className="text-[10px] text-slate-500 bg-white border border-slate-200 px-1.5 py-0.5 rounded font-mono">
                  {profile.educationLevel}
                </span>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
