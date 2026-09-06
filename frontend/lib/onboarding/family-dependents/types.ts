export type FamilyMember = {
  id: string;
  name: string;
  relationship: string;
  dateOfBirth: string;
  occupation: string;
  financialDependency: boolean;
  includeInPlanning: boolean;
};

export type FamilyMemberField = keyof Omit<FamilyMember, "id" | "includeInPlanning">;
export type FamilyMemberErrors = Partial<Record<FamilyMemberField, string>>;

export const emptyFamilyMember: Omit<FamilyMember, "id"> = {
  name: "",
  relationship: "",
  dateOfBirth: "",
  occupation: "",
  financialDependency: true,
  includeInPlanning: false,
};