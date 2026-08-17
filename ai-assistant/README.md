# Indian Career GPS & Exam Navigator

A comprehensive full-stack career guidance and exam navigation platform tailored for Indian aspirants across 15 career domains (Civil Services, Defense, Banking, Software Engineering, AI & Analytics, Railways, PSU, Healthcare, Legal, Teaching, and more).

---

## 🚀 Running Locally on Localhost

All 1,600+ curated career paths, domain datasets, pay scales, syllabus trackers, eligibility engines, and offline fallbacks are bundled directly in the codebase. You can run this completely on your local machine.

### Prerequisites
- **Node.js**: v18.0.0 or higher (Node 20+ recommended)
- **npm**: v9.0.0 or higher

---

### Step-by-Step Local Setup

1. **Download / Extract the Project Folder**
   - In Google AI Studio Build, open the top-right settings menu and click **Export ZIP** (or export to **GitHub** and clone locally).
   - Extract the `.zip` file to your computer.

2. **Open Terminal in the Project Folder**
   ```bash
   cd career-gps-app
   ```

3. **Install Dependencies**
   ```bash
   npm install
   ```

4. **(Optional) Configure API Key**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Add your free Gemini API key to `.env` if you want real-time dynamic AI career generation and interview simulations:
     ```env
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     ```
   - *Note*: If you run without an API key, the built-in catalog of **110+ careers per domain (1,600+ paths total)** will load automatically offline.

5. **Start the Local Development Server**
   ```bash
   npm run dev
   ```

6. **Open in Browser**
   - Navigate to: `http://localhost:3000` (or the port displayed in your terminal).

---

## 📦 What is Included in the Folder

- **`src/data/domainCareerGenerator.ts`**: Master database of 110+ career blueprints per domain across all 15 Indian domains (50 Elite, 50 Stable, 10 Hidden Gems).
- **`src/data/careers.ts`**: Flagship government & private sector career profiles with complete eligibility criteria, step-by-step milestones, notifications, and pay matrix.
- **`src/data/indianStates.ts`**: All 28 Indian States & 8 Union Territories with state PSC portals and local language matrices.
- **`src/utils/eligibilityEngine.ts`**: Rule engine for age relaxations (OBC/SC/ST/EWS/PwBD), educational stream matching, and category reservations.
- **`src/components/`**: Interactive UI components for Roadmap visualizations, Mock Test simulations, Comparative Pay Matrices, PDF exports, and Domain Career Hubs.
- **`server.ts` & `server/geminiService.ts`**: Express backend server for AI generation, caching, and career counseling.
