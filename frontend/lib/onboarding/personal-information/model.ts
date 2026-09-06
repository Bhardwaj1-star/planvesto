export const genderOptions = ["Female", "Male", "Non-binary", "Prefer not to say"] as const;
export const maritalStatusOptions = ["Single", "Married", "Divorced", "Widowed"] as const;

export type SelectOption<T extends string = string> = {
  value: T;
  label: string;
};

export type PersonalInformation = {
  fullName: string;
  dateOfBirth: string;
  gender: string;
  maritalStatus: string;
  mobileNumber: string;
  address: string;
  city: string;
  state: string;
  country: string;
  occupation: string;
};

export type PersonalInformationField = keyof PersonalInformation;
export type PersonalInformationErrors = Partial<
  Record<PersonalInformationField, string>
>;

export const initialPersonalInformation: PersonalInformation = {
  fullName: "",
  dateOfBirth: "",
  gender: "",
  maritalStatus: "",
  mobileNumber: "",
  address: "",
  city: "",
  state: "",
  country: "",
  occupation: "",
};

export const genderSelectOptions: SelectOption[] = genderOptions.map((value) => ({
  value,
  label: value,
}));

export const maritalStatusSelectOptions: SelectOption[] =
  maritalStatusOptions.map((value) => ({ value, label: value }));
