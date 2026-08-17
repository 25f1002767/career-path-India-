import { AgeEligibilityStatus, Eligibility, SocialCategory } from "../types/career";

export function calculateAge(dobString: string): number {
  if (!dobString) return 21; // Default fallback age
  const dob = new Date(dobString);
  const today = new Date();
  let age = today.getFullYear() - dob.getFullYear();
  const m = today.getMonth() - dob.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
    age--;
  }
  return Math.max(age, 14);
}

export function checkAgeEligibility(
  userAge: number,
  eligibility: Eligibility,
  userCategory: SocialCategory = "GENERAL"
): AgeEligibilityStatus {
  if (!eligibility.ageLimit) {
    return {
      isEligible: true,
      userAge,
      minAge: 18,
      maxAgeAllowed: 60,
      baseMaxAge: 60,
      appliedRelaxationYears: 0,
      statusText: "No age limit specified",
      statusBadge: "ELIGIBLE"
    };
  }

  const { min, max, relaxations } = eligibility.ageLimit;
  let relaxationYears = 0;

  if (relaxations && relaxations.length > 0 && userCategory !== "GENERAL") {
    const matched = relaxations.find((r) => r.category === userCategory);
    if (matched) {
      relaxationYears = matched.yearsExtention;
    } else {
      // Standard category relaxation fallback
      if (userCategory === "OBC") relaxationYears = 3;
      if (userCategory === "SC" || userCategory === "ST") relaxationYears = 5;
      if (userCategory === "PWD") relaxationYears = 10;
      if (userCategory === "EX_SERVICEMEN") relaxationYears = 3;
    }
  }

  const maxAllowed = max + relaxationYears;

  if (userAge < min) {
    return {
      isEligible: false,
      userAge,
      minAge: min,
      maxAgeAllowed: maxAllowed,
      baseMaxAge: max,
      appliedRelaxationYears: relaxationYears,
      statusText: `Underage: Requires minimum ${min} years (Current: ${userAge} yrs)`,
      statusBadge: "UNDERAGE"
    };
  }

  if (userAge > maxAllowed) {
    const overBy = userAge - maxAllowed;
    return {
      isEligible: false,
      userAge,
      minAge: min,
      maxAgeAllowed: maxAllowed,
      baseMaxAge: max,
      appliedRelaxationYears: relaxationYears,
      statusText: `Overage: Max age limit is ${maxAllowed} yrs (${max} + ${relaxationYears} yrs relaxation). Exceeded by ${overBy} yr(s).`,
      statusBadge: "OVERAGE"
    };
  }

  if (userAge > max && relaxationYears > 0) {
    return {
      isEligible: true,
      userAge,
      minAge: min,
      maxAgeAllowed: maxAllowed,
      baseMaxAge: max,
      appliedRelaxationYears: relaxationYears,
      statusText: `Eligible via Category Relaxation (+${relaxationYears} yrs extension applied)`,
      statusBadge: "RELAXED_ELIGIBLE"
    };
  }

  return {
    isEligible: true,
    userAge,
    minAge: min,
    maxAgeAllowed: maxAllowed,
    baseMaxAge: max,
    appliedRelaxationYears: relaxationYears,
    statusText: `Eligible (Current age ${userAge} yrs is within ${min}–${maxAllowed} yrs)`,
    statusBadge: "ELIGIBLE"
  };
}
