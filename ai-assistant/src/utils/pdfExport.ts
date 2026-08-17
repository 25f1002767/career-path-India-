import jsPDF from "jspdf";
import { CareerPath, UserProfile } from "../types/career";

export function generateCareerRoadmapPDF(career: CareerPath, profile?: UserProfile) {
  const doc = new jsPDF({
    orientation: "portrait",
    unit: "mm",
    format: "a4"
  });

  const pageWidth = doc.internal.pageSize.getWidth();
  let y = 15;

  // Header Banner
  doc.setFillColor(15, 23, 42); // slate-900
  doc.rect(0, 0, pageWidth, 28, "F");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  doc.setTextColor(255, 255, 255);
  doc.text("CAREER PATH INDIA — Personalized Roadmap", 14, 12);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(9);
  doc.setTextColor(203, 213, 225);
  doc.text(`Generated on: ${new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })} | Verified Grounded Career Guide`, 14, 19);

  y = 35;

  // Career Title
  doc.setFont("helvetica", "bold");
  doc.setFontSize(14);
  doc.setTextColor(15, 23, 42);
  doc.text(career.title, 14, y);

  y += 7;

  // Badges Line
  doc.setFontSize(9);
  doc.setFont("helvetica", "bold");
  doc.setTextColor(30, 58, 138); // Blue
  const metaText = `Tier: ${career.tier}  |  Sector: ${career.sector}  |  Domain: ${career.domain}`;
  doc.text(metaText, 14, y);

  y += 8;

  // Short Description
  doc.setFont("helvetica", "normal");
  doc.setFontSize(9.5);
  doc.setTextColor(51, 65, 85);
  const descLines = doc.splitTextToSize(career.shortDescription, pageWidth - 28);
  doc.text(descLines, 14, y);
  y += descLines.length * 5 + 4;

  // Highlights Box (Salary, Exam Timeline, Eligibility)
  doc.setFillColor(248, 250, 252);
  doc.setDrawColor(226, 232, 240);
  doc.roundedRect(14, y, pageWidth - 28, 26, 2, 2, "FD");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(9);
  doc.setTextColor(15, 23, 42);
  doc.text("Salary Band:", 18, y + 6);
  doc.setFont("helvetica", "normal");
  doc.text(`₹${(career.salaryRange.min/1000).toFixed(0)}k – ₹${(career.salaryRange.max/1000).toFixed(0)}k / month ${career.salaryRange.payScaleCode ? `(${career.salaryRange.payScaleCode})` : ""}`, 42, y + 6);

  doc.setFont("helvetica", "bold");
  doc.text("Exam Cycle:", 18, y + 12);
  doc.setFont("helvetica", "normal");
  doc.text(`${career.examTimeline?.notificationMonth || 'Annual'} (Freq: ${career.examTimeline?.frequency || 'Annual'})`, 42, y + 12);

  doc.setFont("helvetica", "bold");
  doc.text("Eligibility:", 18, y + 18);
  doc.setFont("helvetica", "normal");
  const ageText = career.eligibility.ageLimit ? `${career.eligibility.ageLimit.min}–${career.eligibility.ageLimit.max} yrs` : "N/A";
  doc.text(`${career.eligibility.educationRequired} | Age: ${ageText}`, 42, y + 18);

  y += 32;

  // Roadmap Section Header
  doc.setFont("helvetica", "bold");
  doc.setFontSize(11);
  doc.setTextColor(15, 23, 42);
  doc.text("STEP-BY-STEP PREPARATION ROADMAP", 14, y);
  doc.setLineWidth(0.4);
  doc.setDrawColor(203, 213, 225);
  doc.line(14, y + 2, pageWidth - 14, y + 2);

  y += 8;

  // Roadmap Steps Loop
  career.roadmapSteps.forEach((step) => {
    if (y > 260) {
      doc.addPage();
      y = 20;
    }

    doc.setFillColor(238, 242, 255); // indigo-50
    doc.roundedRect(14, y, 7, 7, 1.5, 1.5, "F");

    doc.setFont("helvetica", "bold");
    doc.setFontSize(9);
    doc.setTextColor(67, 56, 202); // indigo-700
    doc.text(String(step.stepNumber), 16.5, y + 5);

    doc.setFont("helvetica", "bold");
    doc.setFontSize(10);
    doc.setTextColor(15, 23, 42);
    doc.text(step.title, 24, y + 5);

    if (step.estimatedDuration) {
      doc.setFont("helvetica", "italic");
      doc.setFontSize(8.5);
      doc.setTextColor(100, 116, 139);
      doc.text(`Duration: ${step.estimatedDuration}`, pageWidth - 14, y + 5, { align: "right" });
    }

    y += 7;

    doc.setFont("helvetica", "normal");
    doc.setFontSize(9);
    doc.setTextColor(71, 85, 105);
    const stepDesc = doc.splitTextToSize(step.description, pageWidth - 38);
    doc.text(stepDesc, 24, y);

    y += stepDesc.length * 4.5 + 5;
  });

  y += 4;

  // Portals & Sources
  if (y > 250) {
    doc.addPage();
    y = 20;
  }

  doc.setFont("helvetica", "bold");
  doc.setFontSize(10);
  doc.setTextColor(15, 23, 42);
  doc.text("OFFICIAL PORTAL & VERIFIED SOURCES", 14, y);
  y += 5;

  doc.setFont("helvetica", "normal");
  doc.setFontSize(8.5);
  doc.setTextColor(37, 99, 235);
  if (career.applicationPortalUrl) {
    doc.text(`Official Portal: ${career.applicationPortalUrl}`, 14, y);
    y += 4.5;
  }

  if (career.sources && career.sources.length > 0) {
    career.sources.forEach((src) => {
      doc.text(`Source: ${src.title} (${src.url})`, 14, y);
      y += 4.5;
    });
  }

  y += 6;

  // Disclaimer
  doc.setFont("helvetica", "italic");
  doc.setFontSize(7.5);
  doc.setTextColor(148, 163, 184);
  doc.text("Disclaimer: Exam dates, quotas, and age limits are subject to official government notifications. Always verify on official portals.", 14, y);

  doc.save(`${career.id}-career-roadmap.pdf`);
}
