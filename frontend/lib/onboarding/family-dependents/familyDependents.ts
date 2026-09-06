import type { FamilyMember } from "./types";

export function createFamilyMemberId() {
  return `family-member-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

export function getDependencySummary(member: FamilyMember) {
  return member.financialDependency ? "Financially dependent" : "Financially independent";
}