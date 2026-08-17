import React, { useEffect, useState } from "react";
import { Compass, Sparkles, CheckCircle2, Loader2, Globe, ShieldCheck, FileCheck, Timer, Award, Lightbulb } from "lucide-react";

const STAGES = [
  { id: 1, label: "Querying live 2025-2026 UPSC, SSC, RRB & PSU notifications", icon: Globe, durationWeight: 2 },
  { id: 2, label: "Validating age criteria, category relaxations & 7th CPC matrices", icon: ShieldCheck, durationWeight: 2 },
  { id: 3, label: "Synthesizing 50 Elite + 50 Stable + 10 Hidden Gem career tracks", icon: FileCheck, durationWeight: 2 },
  { id: 4, label: "Finalizing state-wise cutoffs, official portals & exam calendar", icon: Sparkles, durationWeight: 2 },
];

const ASPIRANT_TIPS = [
  "Tip: OBC candidates get 3 years, and SC/ST candidates get 5 years age relaxation across Central & State exams.",
  "Tip: PSU recruitment through GATE score often has higher direct starting CTC than private engineering roles.",
  "Tip: Hidden Gem regulatory exams (RBI, SEBI, NABARD, FSSAI) often have lower applicant volumes than SSC/UPSC.",
  "Tip: State PSC Group-B executive posts offer gazetted status with faster promotional cadres."
];

const ESTIMATED_TOTAL_SECONDS = 8;

export const AnalysisLoader: React.FC = () => {
  const [secondsRemaining, setSecondsRemaining] = useState(ESTIMATED_TOTAL_SECONDS);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [currentTipIndex, setCurrentTipIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setElapsedSeconds((prev) => prev + 1);
      setSecondsRemaining((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);

    const tipTimer = setInterval(() => {
      setCurrentTipIndex((prev) => (prev + 1) % ASPIRANT_TIPS.length);
    }, 3000);

    return () => {
      clearInterval(timer);
      clearInterval(tipTimer);
    };
  }, []);

  // Compute percentage progress from 0% to 98% (reserving 100% for actual response)
  const progressPercent = Math.min(
    96,
    Math.round((elapsedSeconds / ESTIMATED_TOTAL_SECONDS) * 100)
  );

  // Compute active stage based on elapsed time
  const currentStageIndex = Math.min(
    STAGES.length - 1,
    Math.floor((elapsedSeconds / ESTIMATED_TOTAL_SECONDS) * STAGES.length)
  );

  // Format time as 00:SS
  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="max-w-2xl mx-auto my-12 p-8 bg-slate-900 border border-slate-800 rounded-3xl text-white shadow-2xl relative overflow-hidden">
      {/* Background ambient lighting */}
      <div className="absolute -right-12 -top-12 w-56 h-56 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -left-12 -bottom-12 w-56 h-56 bg-blue-500/15 rounded-full blur-3xl pointer-events-none" />

      {/* Header Countdown Showcase */}
      <div className="flex flex-col items-center text-center mb-8 relative z-10">
        
        {/* Countdown Badge & Clock */}
        <div className="mb-4 inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-slate-800/80 border border-slate-700 text-xs text-amber-400 font-medium shadow-inner">
          <Timer className="w-4 h-4 text-amber-400 animate-pulse" />
          <span>Live Analysis Pipeline Active</span>
        </div>

        {/* Big Countdown Display */}
        <div className="flex items-baseline space-x-2 mb-2">
          <div className="text-5xl sm:text-6xl font-black font-mono tracking-tight text-white drop-shadow-sm">
            {formatTime(secondsRemaining)}
          </div>
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Estimated Left
          </span>
        </div>

        <p className="text-xs text-slate-400 max-w-md">
          {secondsRemaining > 0
            ? `Generating tailored career recommendations grounded in official notifications`
            : "Finalizing synthesis and organizing 110 career paths... Almost ready!"}
        </p>

        {/* Target Quota Tag */}
        <div className="mt-3 inline-flex items-center space-x-2 px-3 py-1 rounded-lg bg-blue-950/60 border border-blue-800/50 text-[11px] text-blue-300 font-medium">
          <Award className="w-3.5 h-3.5 text-blue-400" />
          <span>Synthesizing 110 Total Paths: 50 Elite • 50 Stable • 10 Hidden Gems</span>
        </div>
      </div>

      {/* Progress Bar & Elapsed stats */}
      <div className="mb-8 relative z-10">
        <div className="flex justify-between items-center text-xs text-slate-400 mb-2 font-mono">
          <span className="flex items-center space-x-1">
            <span className="text-slate-500">Elapsed:</span>
            <span className="text-slate-200 font-semibold">{formatTime(elapsedSeconds)}</span>
          </span>
          <span className="text-amber-400 font-bold">{progressPercent}%</span>
        </div>

        <div className="w-full bg-slate-950 rounded-full h-3 p-0.5 border border-slate-800 shadow-inner overflow-hidden">
          <div
            className="bg-gradient-to-r from-blue-500 via-indigo-500 to-amber-500 h-full rounded-full transition-all duration-700 ease-out shadow-sm shadow-blue-500/50"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Multi-Stage Live Pipeline Checklist */}
      <div className="space-y-2.5 text-left max-w-lg mx-auto mb-8 relative z-10">
        {STAGES.map((stage, idx) => {
          const isDone = idx < currentStageIndex;
          const isCurrent = idx === currentStageIndex;
          const Icon = stage.icon;

          return (
            <div
              key={stage.id}
              className={`flex items-center space-x-3 p-3 rounded-xl border text-xs transition-all ${
                isCurrent
                  ? "bg-slate-800/90 border-amber-500/60 text-amber-300 font-semibold shadow-md ring-1 ring-amber-500/30"
                  : isDone
                  ? "bg-slate-900/60 border-slate-800 text-emerald-400"
                  : "bg-slate-950/40 border-slate-900/80 text-slate-600"
              }`}
            >
              {isDone ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              ) : isCurrent ? (
                <Loader2 className="w-4 h-4 text-amber-400 animate-spin shrink-0" />
              ) : (
                <Icon className="w-4 h-4 text-slate-600 shrink-0" />
              )}
              <span className="truncate flex-1">{stage.label}</span>
              {isDone && (
                <span className="text-[10px] text-emerald-500 font-mono font-medium">DONE</span>
              )}
              {isCurrent && (
                <span className="text-[10px] text-amber-400 font-mono font-medium animate-pulse">PROCESSING</span>
              )}
            </div>
          );
        })}
      </div>

      {/* Aspirant Tips Banner */}
      <div className="bg-slate-950/70 border border-slate-800 rounded-2xl p-4 flex items-start space-x-3 text-left relative z-10">
        <Lightbulb className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
        <div className="text-xs text-slate-300 leading-relaxed">
          <span className="font-semibold text-white">Aspirant Insight: </span>
          {ASPIRANT_TIPS[currentTipIndex]}
        </div>
      </div>

      <div className="mt-4 text-center text-[11px] text-slate-500">
        Expected response time: ~6–8 seconds. Real-time grounding ensures 2025-2026 data accuracy.
      </div>
    </div>
  );
};

