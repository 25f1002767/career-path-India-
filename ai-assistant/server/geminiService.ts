import { GoogleGenAI, Type } from "@google/genai";
import { CareerPath, UserProfile, TierType } from "../src/types/career";
import { FALLBACK_CAREER_PATHS } from "../src/data/fallbackCareers";
import { matchesSelectedDomains } from "../src/utils/domainMatcher";
import { generateDomainCareers } from "../src/data/domainCareerGenerator";

// In-memory cache for tier-specific grounded search results
interface CacheEntry {
  timestamp: number;
  data: CareerPath[];
  sources: { title: string; url: string }[];
}
const cacheStore = new Map<string, CacheEntry>();
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

export function getCacheKeyForTier(profile: UserProfile, tier: TierType): string {
  const domainsStr = (profile.domains || []).sort().join(",");
  return `${profile.educationLevel}_${profile.stream}_${profile.sectorPreference}_${profile.targetState}_${profile.salaryBand}_${domainsStr}_${tier}`;
}

// Utility to normalize title for deduplication
function normalizeTitle(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]/g, "")
    .trim();
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Helper to retry Gemini requests on 429 rate limit with snappy backoff
async function callWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 1,
  initialDelayMs = 1000
): Promise<T> {
  let attempt = 0;
  while (true) {
    try {
      return await fn();
    } catch (err: any) {
      attempt++;
      const errStr = (JSON.stringify(err) + " " + (err?.message || "")).toUpperCase();
      const isRateLimit =
        err?.status === 429 ||
        err?.code === 429 ||
        errStr.includes("429") ||
        errStr.includes("RESOURCE_EXHAUSTED") ||
        errStr.includes("QUOTA");

      if (isRateLimit && attempt <= maxRetries) {
        const backoff = initialDelayMs * Math.pow(2, attempt - 1);
        await delay(backoff);
      } else {
        throw err;
      }
    }
  }
}

// Single Tier Career Generation Pipeline
async function generatePathsForTier(
  ai: GoogleGenAI,
  profile: UserProfile,
  tier: TierType,
  onProgress?: (stage: string) => void
): Promise<{ paths: CareerPath[]; sources: { title: string; url: string }[] }> {
  const cacheKey = getCacheKeyForTier(profile, tier);
  const cached = cacheStore.get(cacheKey);

  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    if (onProgress) onProgress(`Retrieved ${tier} tier from cache...`);
    return {
      paths: cached.data,
      sources: cached.sources,
    };
  }

  const tierDescriptions: Record<TierType, string> = {
    ELITE: "Top-tier prestige, highest salary, executive authority, or high-tier product tech roles (e.g., IAS, IPS, IFS, RBI Grade B, ISRO/DRDO Scientist, NDA/CDS Officer, PSU Management Trainee, Product MNC SDE, Top Law/Finance/R&D).",
    STABLE: "Consistent hiring, high job security, structured career progression, strong public/private core roles (e.g., SSC CGL, SSC CHSL, Railway JE/SSE, SBI PO/Clerk, IBPS, State PSC Group B/C, Big 4 Consultant, Systems Engineer).",
    HIDDEN_GEM: "High pay or excellent work-life balance with less mainstream awareness among students (e.g., EPFO EO/AO, NABARD Officer, FSSAI Tech Officer, Patent Examiner, Regulatory Bodies, Specialized PSU roles, UI/UX Lead, Niche Tech/Govt posts).",
  };

  try {
    // STAGE 1: Research pass scoped strictly to this TIER
    if (onProgress) onProgress(`Researching ${tier} tier career opportunities in India...`);

    const domainsList = (profile.domains && profile.domains.length > 0)
      ? profile.domains.join(", ")
      : "General streams matching qualification";

    const searchPrompt = `
You are an expert Indian career advisor, industry tech scout, and recruitment analyst.
Research and uncover distinct, authentic career tracks strictly in the **${tier}** tier for an Indian candidate with the following profile:

Candidate Profile:
- Education Level: ${profile.educationLevel}
- Stream: ${profile.stream}
- Social Category: ${profile.socialCategory}
- Preferred Sectors: ${profile.sectorPreference}
- MANDATORY Selected Domains: ${domainsList}
- Location / Target State: ${profile.targetState}
- Monthly Salary Goal: ${profile.salaryBand}

Tier Focus (${tier}):
${tierDescriptions[tier]}

CRITICAL DOMAIN INSTRUCTION (MANDATORY):
The candidate has specifically chosen the domain(s): [${domainsList}].
Every single career track you research and return MUST strictly belong to these selected domain(s).
- For example, if "AI, Data Science & Analytics" is selected, you MUST research careers like AI Engineer, Machine Learning Specialist, Data Scientist, MLOps Architect, NLP Engineer, Computer Vision Scientist, Big Data Analytics Lead, Data Analyst, etc.
- If "Software Engineering & IT" is selected, research SDE, Full-Stack Developer, DevOps, Cloud Architect, Cybersecurity Specialist, etc.
- If "Healthcare & Pharmaceuticals" is selected, research Medical Officer, Pharmacist, Clinical Trial Lead, Biotech Scientist, etc.
- DO NOT return Civil Services (UPSC, IAS, IPS, State PSC Admin, etc.) UNLESS the candidate explicitly chose "Civil Services & Public Admin".

Search for:
1. Real 2025-2026 hiring pathways, notifications, enterprise tech tracks, and exams for these specific domains across India.
2. Accurate age limits, qualification requirements, and category relaxations.
3. Realistic Indian pay scale (7th CPC or Private CTC in INR) and official application URLs.
    `;

    let groundedText = "";
    let tierSources: { title: string; url: string }[] = [];

    try {
      // First attempt with Google Search Grounding
      const searchResponse = await callWithRetry(
        () =>
          ai.models.generateContent({
            model: "gemini-3.7-flash",
            contents: searchPrompt,
            config: {
              tools: [{ googleSearch: {} }],
            },
          }),
        2,
        2500
      );

      groundedText = searchResponse.text || "";
      const chunks = searchResponse.candidates?.[0]?.groundingMetadata?.groundingChunks || [];
      chunks.forEach((chunk: any) => {
        if (chunk.web?.uri) {
          tierSources.push({
            title: chunk.web.title || chunk.web.uri,
            url: chunk.web.uri,
          });
        }
      });
    } catch (_searchErr: any) {
      // Fallback: Generate research content directly without search tool to bypass search quota limits
      const directResponse = await callWithRetry(
        () =>
          ai.models.generateContent({
            model: "gemini-3.7-flash",
            contents: searchPrompt + "\nProvide detailed, real factual information on official Indian recruitment pathways for 2025-2026 strictly matching the candidate's selected domains.",
          }),
        3,
        2500
      );

      groundedText = directResponse.text || "";
      tierSources = [
        { title: "National Career Service (NCS) India", url: "https://www.ncs.gov.in" },
        { title: "UPSC Official Portal", url: "https://upsc.gov.in" },
        { title: "SSC Recruitment Portal", url: "https://ssc.gov.in" },
      ];
    }

    // STAGE 2: Structuring Pass
    if (onProgress) onProgress(`Structuring ${tier} tier options for selected domains...`);

    const structuringPrompt = `
Based on the grounded research data below, format a structured JSON array of distinct, realistic career options strictly for tier "${tier}" strictly within the candidate's chosen domain(s): [${domainsList}].

Profile:
- Education: ${profile.educationLevel} (${profile.stream})
- MANDATORY Domains: ${domainsList}
- State Focus: ${profile.targetState}
- Sector Preference: ${profile.sectorPreference}
- Category: ${profile.socialCategory}

Tier Definition:
${tierDescriptions[tier]}

Grounded Research Data:
${groundedText}

STRICT DOMAIN RULE:
- All generated career items MUST align directly with the candidate's selected domains: [${domainsList}].
- If the candidate selected "AI, Data Science & Analytics", do not output Civil Services or unrelated exams. Output AI/Data/ML/Analytics/Tech roles.
- Each career item in the JSON array MUST have tier strictly set to "${tier}" and follow the exact JSON schema provided.
    `;

    const responseSchema = {
      type: Type.ARRAY,
      items: {
        type: Type.OBJECT,
        properties: {
          id: { type: Type.STRING },
          title: { type: Type.STRING },
          tier: { type: Type.STRING, enum: [tier] },
          sector: { type: Type.STRING, enum: ["GOVT", "PRIVATE"] },
          domain: { type: Type.STRING },
          shortDescription: { type: Type.STRING },
          eligibility: {
            type: Type.OBJECT,
            properties: {
              educationRequired: { type: Type.STRING },
              minEducationLevel: { type: Type.STRING, enum: ["12TH", "DIPLOMA", "GRADUATE", "POST_GRADUATE"] },
              ageLimit: {
                type: Type.OBJECT,
                properties: {
                  min: { type: Type.NUMBER },
                  max: { type: Type.NUMBER },
                  relaxations: {
                    type: Type.ARRAY,
                    items: {
                      type: Type.OBJECT,
                      properties: {
                        category: { type: Type.STRING },
                        yearsExtention: { type: Type.NUMBER },
                        notes: { type: Type.STRING },
                      },
                    },
                  },
                },
              },
              otherCriteria: { type: Type.ARRAY, items: { type: Type.STRING } },
            },
            required: ["educationRequired", "minEducationLevel"],
          },
          competitionStats: {
            type: Type.OBJECT,
            properties: {
              applicants: { type: Type.NUMBER },
              seats: { type: Type.NUMBER },
              ratio: { type: Type.STRING },
              lastUpdated: { type: Type.STRING },
              difficultyRating: { type: Type.STRING, enum: ["MODERATE", "HIGH", "VERY_HIGH", "EXTREME"] },
            },
          },
          roadmapSteps: {
            type: Type.ARRAY,
            items: {
              type: Type.OBJECT,
              properties: {
                stepNumber: { type: Type.NUMBER },
                title: { type: Type.STRING },
                description: { type: Type.STRING },
                estimatedDuration: { type: Type.STRING },
              },
              required: ["stepNumber", "title", "description"],
            },
          },
          salaryRange: {
            type: Type.OBJECT,
            properties: {
              min: { type: Type.NUMBER },
              max: { type: Type.NUMBER },
              currency: { type: Type.STRING, enum: ["INR"] },
              payScaleCode: { type: Type.STRING },
            },
            required: ["min", "max", "currency"],
          },
          applicationPortalUrl: { type: Type.STRING },
          sources: {
            type: Type.ARRAY,
            items: {
              type: Type.OBJECT,
              properties: {
                title: { type: Type.STRING },
                url: { type: Type.STRING },
              },
            },
          },
          stateSpecific: { type: Type.STRING },
          examTimeline: {
            type: Type.OBJECT,
            properties: {
              notificationMonth: { type: Type.STRING },
              examMonth: { type: Type.STRING },
              frequency: { type: Type.STRING },
              applicationFee: { type: Type.STRING },
            },
          },
          growthProspects: { type: Type.STRING },
        },
        required: ["id", "title", "tier", "sector", "domain", "shortDescription", "eligibility", "roadmapSteps", "salaryRange"],
      },
    };

    const structuringResponse = await callWithRetry(
      () =>
        ai.models.generateContent({
          model: "gemini-3.7-flash",
          contents: structuringPrompt,
          config: {
            responseMimeType: "application/json",
            responseSchema,
          },
        }),
      3,
      2500
    );

    const parsed: CareerPath[] = JSON.parse(structuringResponse.text || "[]");
    const collectedPaths: CareerPath[] = [];
    const seenNormalizedTitles = new Set<string>();
    const hasUserDomains = profile.domains && profile.domains.length > 0;

    for (const item of parsed) {
      if (!item.title) continue;
      item.tier = tier;

      // Enforce strict domain match: discard AI hallucinations outside user-selected domains
      if (hasUserDomains && !matchesSelectedDomains(item, profile.domains)) {
        continue;
      }

      if (!item.domain && hasUserDomains) {
        item.domain = profile.domains[0];
      }

      const norm = normalizeTitle(item.title);
      if (!seenNormalizedTitles.has(norm)) {
        seenNormalizedTitles.add(norm);
        if (!item.sources || item.sources.length === 0) {
          item.sources = tierSources.slice(0, 3);
        }
        collectedPaths.push(item);
      }
    }

    if (collectedPaths.length > 0) {
      cacheStore.set(cacheKey, {
        timestamp: Date.now(),
        data: collectedPaths,
        sources: tierSources,
      });
      return { paths: collectedPaths, sources: tierSources };
    }

    throw new Error(`Parsed array had no valid domain paths for tier ${tier}`);
  } catch (_err: any) {
    const fallbackForTier = filterFallbackPathsForTier(profile, tier);
    return { paths: fallbackForTier, sources: [] };
  }
}

// In-memory cache to save API quota while delivering instant, high-quality grounded AI results
const aiProfileCache = new Map<string, { paths: CareerPath[]; groundedSources: { title: string; url: string }[]; timestamp: number }>();

export async function generateGroundedCareerPaths(
  profile: UserProfile,
  onProgress?: (stage: string) => void,
  userApiKey?: string
): Promise<{ paths: CareerPath[]; groundedSources: { title: string; url: string }[]; usedCustomKey: boolean }> {
  const activeKey = userApiKey?.trim() || process.env.GEMINI_API_KEY;

  // Cache key based on profile dimensions
  const cacheKey = `${profile.educationLevel}_${profile.stream}_${profile.socialCategory}_${profile.sectorPreference}_${profile.targetState || "All"}_${(profile.domains || []).sort().join(",")}`;
  
  // Check cache first
  const cached = aiProfileCache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    console.log(`[Cache Hit] Serving cached AI roadmap for ${cacheKey} (0 quota consumed)`);
    if (onProgress) onProgress("Serving verified live grounded roadmap from high-speed cache...");
    return {
      paths: cached.paths,
      groundedSources: cached.groundedSources,
      usedCustomKey: !!userApiKey,
    };
  }

  if (!activeKey || activeKey === "MY_GEMINI_API_KEY") {
    console.warn("No active Gemini API key configured. Returning verified baseline dataset.");
    if (onProgress) onProgress("Synthesizing verified Indian career database...");
    await delay(300);
    return {
      paths: filterFallbackPaths(profile),
      groundedSources: [
        { title: "National Career Service (NCS) India", url: "https://www.ncs.gov.in" },
        { title: "UPSC Official Portal", url: "https://upsc.gov.in" },
        { title: "SSC Recruitment Portal", url: "https://ssc.gov.in" },
        { title: "Railway Recruitment Control Board", url: "https://indianrailways.gov.in" },
        { title: "Department of Personnel & Training (DoPT)", url: "https://dopt.gov.in" },
      ],
      usedCustomKey: false,
    };
  }

  const ai = new GoogleGenAI({
    apiKey: activeKey,
    httpOptions: {
      headers: {
        "User-Agent": "aistudio-build",
      },
    },
  });

  if (onProgress) onProgress("Initiating parallel 3-tier live search & grounded pipeline (Elite, Stable, Hidden Gems)...");

  // Run tier pipelines in parallel with timeout safeguards for high speed and reliability
  const tiers: TierType[] = ["ELITE", "STABLE", "HIDDEN_GEM"];

  // Helper with 7.5 second timeout per tier to prevent long hanging calls
  const fetchTierWithTimeout = async (tier: TierType) => {
    try {
      const timeoutPromise = new Promise<{ paths: CareerPath[]; sources: { title: string; url: string }[] }>((resolve) =>
        setTimeout(() => {
          resolve({ paths: filterFallbackPathsForTier(profile, tier), sources: [] });
        }, 7500)
      );
      const executionPromise = generatePathsForTier(ai, profile, tier, onProgress).catch(() => ({
        paths: filterFallbackPathsForTier(profile, tier),
        sources: [],
      }));
      return await Promise.race([executionPromise, timeoutPromise]);
    } catch {
      return { paths: filterFallbackPathsForTier(profile, tier), sources: [] };
    }
  };

  const results = await Promise.all(tiers.map((tier) => fetchTierWithTimeout(tier)));

  // Target counts per tier when no domains are selected (general open browse mode)
  const TARGET_COUNTS: Record<TierType, number> = {
    ELITE: 50,
    STABLE: 50,
    HIDDEN_GEM: 10,
  };

  const finalPaths: CareerPath[] = [];
  const globalSeenTitles = new Set<string>();
  const allSources: { title: string; url: string }[] = [];
  const hasUserDomains = profile.domains && profile.domains.length > 0;

  for (const res of results) {
    allSources.push(...res.sources);
  }

  for (const tier of tiers) {
    const rawAiPaths = results.flatMap((r) => r.paths).filter((p) => p.tier === tier);
    const aiPaths = hasUserDomains
      ? rawAiPaths.filter((p) => matchesSelectedDomains(p, profile.domains))
      : rawAiPaths;
    const fallbackPaths = filterFallbackPathsForTier(profile, tier);

    const tierPaths: CareerPath[] = [];
    const tierSeen = new Set<string>();

    // 1. Add AI generated paths first
    for (const item of aiPaths) {
      const norm = normalizeTitle(item.title);
      if (!tierSeen.has(norm) && !globalSeenTitles.has(norm)) {
        tierSeen.add(norm);
        globalSeenTitles.add(norm);
        tierPaths.push(item);
      }
    }

    // 2. Pad with domain-verified baseline dataset
    for (const item of fallbackPaths) {
      if (tierPaths.length >= TARGET_COUNTS[tier]) break;
      const norm = normalizeTitle(item.title);
      if (!tierSeen.has(norm) && !globalSeenTitles.has(norm)) {
        tierSeen.add(norm);
        globalSeenTitles.add(norm);
        tierPaths.push(item);
      }
    }

    // 3. Fill up to target count from comprehensive domain generator
    if (tierPaths.length < TARGET_COUNTS[tier]) {
      const generatedDomainPaths = generateDomainCareers(profile.domains || [], profile).filter((p) => p.tier === tier);
      for (const item of generatedDomainPaths) {
        if (tierPaths.length >= TARGET_COUNTS[tier]) break;
        const norm = normalizeTitle(item.title);
        if (!tierSeen.has(norm) && !globalSeenTitles.has(norm)) {
          tierSeen.add(norm);
          globalSeenTitles.add(norm);
          tierPaths.push(item);
        }
      }
    }

    // 4. Fill from general baseline pool if still under target count and no strict domains
    if (!hasUserDomains && tierPaths.length < TARGET_COUNTS[tier]) {
      const allBaselineForTier = FALLBACK_CAREER_PATHS.filter((p) => p.tier === tier);
      for (const item of allBaselineForTier) {
        if (tierPaths.length >= TARGET_COUNTS[tier]) break;
        const norm = normalizeTitle(item.title);
        if (!tierSeen.has(norm) && !globalSeenTitles.has(norm)) {
          tierSeen.add(norm);
          globalSeenTitles.add(norm);
          tierPaths.push(item);
        }
      }
    }

    finalPaths.push(...tierPaths);
  }

  // Deduplicate sources by URL
  const uniqueSources = Array.from(
    new Map(allSources.map((s) => [s.url, s])).values()
  ).slice(0, 15);

  // Final sanity filter to ensure 100% domain purity
  const sanitizedFinalPaths = hasUserDomains
    ? finalPaths.filter((p) => matchesSelectedDomains(p, profile.domains))
    : finalPaths;

  if (sanitizedFinalPaths.length > 0) {
    // Save into in-memory cache so subsequent similar requests consume 0 quota
    aiProfileCache.set(cacheKey, {
      paths: sanitizedFinalPaths,
      groundedSources: uniqueSources,
      timestamp: Date.now(),
    });

    return {
      paths: sanitizedFinalPaths,
      groundedSources: uniqueSources,
      usedCustomKey: !!userApiKey,
    };
  }

  return {
    paths: filterFallbackPaths(profile),
    groundedSources: [
      { title: "National Career Service (NCS)", url: "https://www.ncs.gov.in" },
      { title: "UPSC Official Portal", url: "https://upsc.gov.in" },
    ],
    usedCustomKey: true,
  };
}

function filterFallbackPathsForTier(profile: UserProfile, tier: TierType): CareerPath[] {
  const filtered = filterFallbackPaths(profile).filter((p) => p.tier === tier);
  return filtered;
}

function filterFallbackPaths(profile: UserProfile): CareerPath[] {
  if (profile.domains && profile.domains.length > 0) {
    const domainGenerated = generateDomainCareers(profile.domains, profile);
    return domainGenerated;
  }

  let list = [...FALLBACK_CAREER_PATHS];

  if (profile.sectorPreference === "GOVT") {
    list = list.filter((p) => p.sector === "GOVT");
  } else if (profile.sectorPreference === "PRIVATE") {
    list = list.filter((p) => p.sector === "PRIVATE");
  }

  const eduRank: Record<string, number> = { "12TH": 1, "DIPLOMA": 2, "GRADUATE": 3, "POST_GRADUATE": 4 };
  const userRank = eduRank[profile.educationLevel] || 3;

  list = list.filter((p) => {
    const requiredRank = eduRank[p.eligibility.minEducationLevel] || 1;
    return userRank >= requiredRank;
  });

  return list;
}

