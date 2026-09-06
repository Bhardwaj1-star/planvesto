import type { FamilyMember, FamilyMemberErrors } from "./types";

function isValidDate(value: string) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) return false;
  const [, year, month, day] = match.map(Number);
  const date = new Date(year, month - 1, day);
  return date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day;
}

export function validateFamilyMember(member: FamilyMember): FamilyMemberErrors {
  const errors: FamilyMemberErrors = {};

  if (!member.name.trim()) {
    errors.name = "Enter this family member's name.";
  } else if (member.name.trim().length < 2) {
    errors.name = "Enter at least 2 characters.";
  }

  if (!member.relationship.trim()) {
    errors.relationship = "Enter their relationship to you.";
  }

  if (!member.dateOfBirth) {
    errors.dateOfBirth = "Enter their date of birth.";
  } else if (!isValidDate(member.dateOfBirth)) {
    errors.dateOfBirth = "Enter a valid date.";
  } else if (member.dateOfBirth > new Date().toISOString().slice(0, 10)) {
    errors.dateOfBirth = "Date of birth cannot be in the future.";
  }

  if (typeof member.financialDependency !== "boolean") {
    errors.financialDependency = "Select whether this family member is financially dependent.";
  }

  return errors;
}