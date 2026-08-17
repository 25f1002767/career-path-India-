import React, { useState, useEffect, useMemo } from "react";
import { UserProfile, CareerPath, FilterState } from "./types/career";
import { FALLBACK_CAREER_PATHS } from "./data/fallbackCareers";
import { Header } from "./components/Header";
import { ProfileForm } from "./components/ProfileForm";
import { AnalysisLoader } from "./components/AnalysisLoader";
import { FilterBar } from "./components/FilterBar";
import { CareerCard } from "./components/CareerCard";
import { CareerDetailModal } from "./components/CareerDetailModal";
import { AgeCalculatorView } from "./components/AgeCalculatorView";
import { CompareModal } from "./components/CompareModal";
import { ExamCalendarView } from "./components/ExamCalendarView";
import { BookmarksView } from "./components/BookmarksView";
import { ApiKeyModal } from "./components/ApiKeyModal";
import { checkAgeEligibility } from "./utils/ageCalculator";
import { matchesSelectedDomains } from "./utils/domainMatcher";
import { generateDomainCareers } from "./data/domainCareerGenerator";
import { Compass, Sparkles, RefreshCw, AlertCircle, ShieldCheck } from "lucide-react";

export default function App() {
  // Navigation State
  const [activeTab, setActiveTab] = useState<
    "RECOMMENDATIONS" | "AGE_CALCULATOR" | "EXAM_CALENDAR" | "BOOKMARKS" | "COMPARE"
  >("RECOMMENDATIONS");

  // Profile State
  const [profile, setProfile] = useState<UserProfile | null>(() => {
    try {
      const saved = localStorage.getItem("cpi_user_profile");
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const [isEditingProfile, setIsEditingProfile] = useState<boolean>(!profile);

  // Custom User Gemini API Key (BYOK)
  const [customApiKey, setCustomApiKey] = useState<string>(() => {
    try {
      return localStorage.getItem("custom_gemini_api_key") || "";
    } catch {
      return "";
    }
  });
  const [isApiKeyModalOpen, setIsApiKeyModalOpen] = useState<boolean>(false);

  // Careers Dataset State
  const [careers, setCareers] = useState<CareerPath[]>(() => {
    try {
      const savedProfile = localStorage.getItem("cpi_user_profile");
      if (savedProfile) {
        const parsed = JSON.parse(savedProfile);
        if (parsed.domains && parsed.domains.length > 0) {
          return generateDomainCareers(parsed.domains, parsed);
        }
      }
    } catch {
      // fallback
    }
    return FALLBACK_CAREER_PATHS;
  });
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [apiError, setApiError] = useState<string | null>(null);

  // Modal State
  const [selectedCareerModal, setSelectedCareerModal] = useState<CareerPath | null>(null);

  // Bookmarks State
  const [bookmarks, setBookmarks] = useState<CareerPath[]>(() => {
    try {
      const saved = localStorage.getItem("cpi_bookmarks");
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // Comparison State
  const [comparedIds, setComparedIds] = useState<string[]>(() => {
    try {
      const saved = localStorage.getItem("cpi_compared_ids");
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // Filter State
  const [filter, setFilter] = useState<FilterState>({
    sector: "ALL",
    tier: "ALL",
    domain: "ALL",
    searchQuery: "",
    eligibilityFilter: "ALL",
    sortBy: "RECOMMENDED",
  });

  // Persist local state changes
  useEffect(() => {
    if (profile) {
      localStorage.setItem("cpi_user_profile", JSON.stringify(profile));
    }
  }, [profile]);

  useEffect(() => {
    localStorage.setItem("cpi_bookmarks", JSON.stringify(bookmarks));
  }, [bookmarks]);

  useEffect(() => {
    localStorage.setItem("cpi_compared_ids", JSON.stringify(comparedIds));
  }, [comparedIds]);

  // Handle Profile Submission -> Trigger AI Pipeline
  const handleProfileSubmit = async (newProfile: UserProfile) => {
    setProfile(newProfile);
    setIsEditingProfile(false);
    setIsLoading(true);
    setApiError(null);

    // Reset UI filters so nothing is unintentionally hidden
    setFilter({
      sector: "ALL",
      tier: "ALL",
      domain: "ALL",
      searchQuery: "",
      eligibilityFilter: "ALL",
      sortBy: "RECOMMENDED",
    });

    const hasDomains = newProfile.domains && newProfile.domains.length > 0;
    const domainList = hasDomains
      ? generateDomainCareers(newProfile.domains, newProfile)
      : FALLBACK_CAREER_PATHS;

    try {
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (customApiKey && customApiKey.trim()) {
        headers["x-gemini-api-key"] = customApiKey.trim();
      }

      const res = await fetch("/api/careers/recommend", {
        method: "POST",
        headers,
        body: JSON.stringify({ profile: newProfile, userApiKey: customApiKey }),
      });

      const json = await res.json();

      if (json.success && Array.isArray(json.data) && json.data.length > 0) {
        const receivedPaths: CareerPath[] = json.data;
        const sanitizedPaths = hasDomains
          ? receivedPaths.filter((c) => matchesSelectedDomains(c, newProfile.domains))
          : receivedPaths;

        // If count is less than 110, pad with domain-generated careers to guarantee the ~110 volume
        if (sanitizedPaths.length < 110 && hasDomains) {
          const seen = new Set(sanitizedPaths.map((p) => p.title.toLowerCase().trim()));
          const domainPadding = generateDomainCareers(newProfile.domains, newProfile);
          for (const p of domainPadding) {
            const norm = p.title.toLowerCase().trim();
            if (!seen.has(norm)) {
              seen.add(norm);
              sanitizedPaths.push(p);
            }
          }
        }

        setCareers(sanitizedPaths.length > 0 ? sanitizedPaths : domainList);
      } else {
        console.warn("API response returned empty data, using domain-filtered baseline fallback.");
        setCareers(domainList);
      }
    } catch (err: any) {
      console.error("Failed to fetch recommendations:", err);
      setApiError("Unable to reach AI pipeline server. Displaying verified baseline career database for your domain.");
      setCareers(domainList);
    } finally {
      setIsLoading(false);
    }
  };

  // Toggle Bookmark
  const handleToggleBookmark = (career: CareerPath) => {
    if (bookmarks.some((b) => b.id === career.id)) {
      setBookmarks(bookmarks.filter((b) => b.id !== career.id));
    } else {
      setBookmarks([...bookmarks, career]);
    }
  };

  // Toggle Compare
  const handleToggleCompare = (career: CareerPath) => {
    if (comparedIds.includes(career.id)) {
      setComparedIds(comparedIds.filter((id) => id !== career.id));
    } else {
      if (comparedIds.length >= 4) {
        alert("You can compare up to 4 career paths simultaneously.");
        return;
      }
      setComparedIds([...comparedIds, career.id]);
    }
  };

  // Filter & Sort Logic
  const filteredCareers = useMemo(() => {
    let result = [...careers];

    // Strictly enforce profile selected domains
    if (profile?.domains && profile.domains.length > 0) {
      result = result.filter((c) => matchesSelectedDomains(c, profile.domains));
    }

    // Sector Filter
    if (filter.sector !== "ALL") {
      result = result.filter((c) => c.sector === filter.sector);
    }

    // Tier Filter
    if (filter.tier !== "ALL") {
      result = result.filter((c) => c.tier === filter.tier);
    }

    // Secondary UI Domain Filter (if user filters inside the chosen domain)
    if (filter.domain !== "ALL") {
      result = result.filter((c) => matchesSelectedDomains(c, [filter.domain]));
    }

    // Search Query
    if (filter.searchQuery.trim()) {
      const q = filter.searchQuery.toLowerCase();
      result = result.filter(
        (c) =>
          c.title.toLowerCase().includes(q) ||
          c.domain.toLowerCase().includes(q) ||
          c.shortDescription.toLowerCase().includes(q) ||
          (c.stateSpecific && c.stateSpecific.toLowerCase().includes(q))
      );
    }

    // Age Eligibility Filter
    if (filter.eligibilityFilter === "ELIGIBLE_ONLY" && profile) {
      const userAge = profile.age || 21;
      const userCategory = profile.socialCategory || "GENERAL";
      result = result.filter((c) => checkAgeEligibility(userAge, c.eligibility, userCategory).isEligible);
    }

    // Sort By
    if (filter.sortBy === "SALARY_HIGH") {
      result.sort((a, b) => b.salaryRange.min - a.salaryRange.min);
    } else if (filter.sortBy === "COMPETITION_LOW") {
      result.sort((a, b) => (a.competitionStats?.seats || 0) - (b.competitionStats?.seats || 0));
    } else if (filter.sortBy === "DURATION_SHORT") {
      result.sort((a, b) => a.roadmapSteps.length - b.roadmapSteps.length);
    }

    return result;
  }, [careers, filter, profile]);

  const comparedCareersList = useMemo(() => {
    return careers.filter((c) => comparedIds.includes(c.id));
  }, [careers, comparedIds]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans flex flex-col selection:bg-blue-600 selection:text-white">
      
      {/* Navigation Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        profile={profile}
        onEditProfile={() => setIsEditingProfile(true)}
        bookmarksCount={bookmarks.length}
        compareCount={comparedIds.length}
        hasCustomApiKey={!!customApiKey}
        onOpenApiKeyModal={() => setIsApiKeyModalOpen(true)}
      />

      {/* Main Container */}
      <main className="flex-1">
        
        {/* Profile Editing Form View */}
        {isEditingProfile ? (
          <ProfileForm
            initialProfile={profile}
            onSubmitProfile={handleProfileSubmit}
            isSubmitting={isLoading}
          />
        ) : isLoading ? (
          /* Live AI Analysis Pipeline Progress Loader */
          <AnalysisLoader />
        ) : (
          /* Main Tab Routing */
          <>
            {activeTab === "RECOMMENDATIONS" && (
              <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-6">
                
                {/* User Profile Summary Bar */}
                {profile && (
                  <div className="bg-white text-slate-900 rounded-2xl p-6 shadow-xs border border-slate-200 flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 rounded-xl bg-blue-600 text-white font-bold text-xl flex items-center justify-center shadow-xs shrink-0">
                        {profile.name ? profile.name.charAt(0).toUpperCase() : "S"}
                      </div>
                      <div>
                        <div className="flex flex-wrap items-center gap-2">
                          <h2 className="text-xl font-bold text-slate-900">{profile.name}'s Customized Roadmap</h2>
                          <span className="bg-blue-50 text-blue-700 text-xs font-semibold px-2.5 py-0.5 rounded-full border border-blue-200">
                            Age {profile.age} Yrs ({profile.socialCategory})
                          </span>
                          <span className="bg-emerald-50 text-emerald-800 text-[11px] font-semibold px-2 py-0.5 rounded-full border border-emerald-300 flex items-center space-x-1">
                            <ShieldCheck className="w-3 h-3 text-emerald-600" />
                            <span>Verified 2025–2026 Pathways</span>
                          </span>
                        </div>
                        <p className="text-xs text-slate-500 mt-0.5">
                          {profile.educationLevel} ({profile.stream}) • Target Location: <span className="text-slate-900 font-semibold">{profile.targetState}</span> • Sector: {profile.sectorPreference}
                        </p>
                        {profile.domains && profile.domains.length > 0 && (
                          <div className="flex flex-wrap items-center gap-1.5 mt-2">
                            <span className="text-[11px] font-medium text-slate-500">Selected Domains:</span>
                            {profile.domains.map((dom) => (
                              <span
                                key={dom}
                                className="inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-semibold bg-blue-100 text-blue-800"
                              >
                                {dom}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>

                    <button
                      onClick={() => setIsEditingProfile(true)}
                      className="px-4 py-2 rounded-lg bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 text-xs font-semibold transition flex items-center space-x-1.5 shrink-0 self-start md:self-auto"
                    >
                      <RefreshCw className="w-3.5 h-3.5 text-blue-600" />
                      <span>Update Intake Profile</span>
                    </button>
                  </div>
                )}

                {/* API Warning Notice if fallback used */}
                {apiError && (
                  <div className="bg-amber-50 border border-amber-200 text-amber-900 rounded-2xl p-4 text-xs flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
                      <span>{apiError}</span>
                    </div>
                  </div>
                )}

                {/* Filter Controls */}
                <FilterBar
                  filter={filter}
                  setFilter={setFilter}
                  totalResultsCount={filteredCareers.length}
                  userDomains={profile?.domains}
                />

                {/* Results Count Summary */}
                <div className="flex items-center justify-between text-xs font-semibold text-slate-500 px-1">
                  <span>Showing {filteredCareers.length} Grounded Career Paths</span>
                  <span>Categorized by Elite, Stable & Hidden Gems</span>
                </div>

                {/* Grid of Career Cards */}
                {filteredCareers.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredCareers.map((career) => (
                      <CareerCard
                        key={career.id}
                        career={career}
                        profile={profile}
                        onSelect={setSelectedCareerModal}
                        isBookmarked={bookmarks.some((b) => b.id === career.id)}
                        onToggleBookmark={handleToggleBookmark}
                        isCompared={comparedIds.includes(career.id)}
                        onToggleCompare={handleToggleCompare}
                      />
                    ))}
                  </div>
                ) : (
                  <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
                    <Compass className="w-12 h-12 text-slate-300 mx-auto" />
                    <h3 className="text-lg font-bold text-slate-900">No career paths match your filters</h3>
                    <p className="text-xs text-slate-500 max-w-sm mx-auto">
                      Try resetting domain filters or clearing search terms to expand career options.
                    </p>
                    <button
                      onClick={() =>
                        setFilter({
                          sector: "ALL",
                          tier: "ALL",
                          domain: "ALL",
                          searchQuery: "",
                          eligibilityFilter: "ALL",
                          sortBy: "RECOMMENDED",
                        })
                      }
                      className="px-4 py-2 rounded-lg bg-blue-600 text-white font-semibold text-xs hover:bg-blue-700 transition"
                    >
                      Reset Filters
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* TAB: AGE & ELIGIBILITY CALCULATOR */}
            {activeTab === "AGE_CALCULATOR" && (
              <AgeCalculatorView
                careers={careers}
                onSelectCareer={setSelectedCareerModal}
              />
            )}

            {/* TAB: EXAM CALENDAR */}
            {activeTab === "EXAM_CALENDAR" && (
              <ExamCalendarView
                careers={careers}
                onSelectCareer={setSelectedCareerModal}
              />
            )}

            {/* TAB: SAVED BOOKMARKS */}
            {activeTab === "BOOKMARKS" && (
              <BookmarksView
                bookmarkedCareers={bookmarks}
                profile={profile}
                onSelectCareer={setSelectedCareerModal}
                onToggleBookmark={handleToggleBookmark}
                comparedIds={comparedIds}
                onToggleCompare={handleToggleCompare}
                onClearBookmarks={() => setBookmarks([])}
              />
            )}

            {/* TAB: COMPARE MATRIX */}
            {activeTab === "COMPARE" && (
              <CompareModal
                comparedCareers={comparedCareersList}
                profile={profile}
                onRemoveFromCompare={(id) => setComparedIds(comparedIds.filter((i) => i !== id))}
                onClearAll={() => setComparedIds([])}
                onSelectCareer={setSelectedCareerModal}
              />
            )}
          </>
        )}

      </main>

      {/* Detail Modal */}
      <CareerDetailModal
        career={selectedCareerModal}
        profile={profile}
        onClose={() => setSelectedCareerModal(null)}
        isBookmarked={selectedCareerModal ? bookmarks.some((b) => b.id === selectedCareerModal.id) : false}
        onToggleBookmark={handleToggleBookmark}
      />

      {/* Custom Gemini API Key (BYOK) Modal */}
      <ApiKeyModal
        isOpen={isApiKeyModalOpen}
        onClose={() => setIsApiKeyModalOpen(false)}
        currentApiKey={customApiKey}
        onSaveApiKey={(key) => {
          setCustomApiKey(key);
          if (key) {
            localStorage.setItem("custom_gemini_api_key", key);
          } else {
            localStorage.removeItem("custom_gemini_api_key");
          }
        }}
      />

      {/* Footer */}
      <footer className="bg-white text-slate-600 border-t border-slate-200 py-8 px-4 text-center text-xs mt-12">
        <div className="max-w-7xl mx-auto space-y-2">
          <div className="flex items-center justify-center space-x-2 text-slate-900 font-bold">
            <div className="w-5 h-5 rounded bg-blue-600 text-white flex items-center justify-center text-[10px]">
              <Compass className="w-3.5 h-3.5" />
            </div>
            <span>CAREER PATH INDIA</span>
          </div>
          <p className="text-slate-500 max-w-xl mx-auto">
            Grounding AI Career Guidance Platform for 12th & Graduate Aspirants across Union & State Government Recruitment & Private Technology Sectors.
          </p>
          <p className="text-slate-400 text-[10px]">
            © {new Date().getFullYear()} Career Path India. Grounded in official recruitment portals (UPSC, SSC, RRB, State PSC, NTA, IBPS).
          </p>
        </div>
      </footer>

    </div>
  );
}
