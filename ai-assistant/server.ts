import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import dotenv from "dotenv";
import { generateGroundedCareerPaths } from "./server/geminiService";
import { UserProfile } from "./src/types/career";

dotenv.config();

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API Route: Health check
  app.get("/api/health", (_req, res) => {
    res.json({ status: "ok", service: "Career Path India AI Engine" });
  });

  // API Route: Recommend Careers (Two-Stage Gemini Grounded Pipeline)
  app.post("/api/careers/recommend", async (req, res) => {
    try {
      const profile: UserProfile = req.body.profile;
      const userApiKey = (req.headers["x-gemini-api-key"] as string) || req.body.userApiKey;

      if (!profile || !profile.educationLevel || !profile.stream) {
        res.status(400).json({ error: "Invalid profile data provided. Education level and stream are required." });
        return;
      }

      console.log(`[AI Pipeline] Processing career recommendations for: ${profile.name || "Anonymous"}, Level: ${profile.educationLevel}, Sector: ${profile.sectorPreference} ${userApiKey ? "(Using Custom User API Key)" : "(Verified Database Mode - Server Key Protected)"}`);

      const result = await generateGroundedCareerPaths(
        profile,
        (stageMessage) => {
          console.log(`[AI Stage] ${stageMessage}`);
        },
        userApiKey
      );

      res.json({
        success: true,
        data: result.paths,
        groundedSources: result.groundedSources,
        usedCustomKey: result.usedCustomKey,
        profile,
        generatedAt: new Date().toISOString()
      });
    } catch (error: any) {
      console.error("[API Error /api/careers/recommend]:", error);
      res.status(500).json({ error: "Failed to generate career recommendations", details: error.message });
    }
  });

  // Vite middleware setup for development vs production
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (_req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`🚀 Career Path India Server running on http://0.0.0.0:${PORT}`);
  });
}

startServer();
