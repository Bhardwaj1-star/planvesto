import type {
  PersonalInformation,
  PersonalInformationErrors,
} from "./model";

function isValidDate(value: string) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) return false;
  const [, year, month, day] = match.map(Number);
  const date = new Date(year, month - 1, day);
  return date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day;
}

export function validatePersonalInformation(
  values: PersonalInformation,
): PersonalInformationErrors {
  const errors: PersonalInformationErrors = {};
  const fullName = values.fullName.trim();
  const occupation = values.occupation.trim();
  const address = values.address.trim();
  const city = values.city.trim();
  const state = values.state.trim();
  const country = values.country.trim();
  const mobile = values.mobileNumber.trim();

  if (!fullName) {
    errors.fullName = "Enter your full name.";
  } else if (fullName.length < 2) {
    errors.fullName = "Your name should be at least 2 characters.";
  }

  if (!values.dateOfBirth) {
    errors.dateOfBirth = "Enter your date of birth.";
  } else if (!isValidDate(values.dateOfBirth)) {
    errors.dateOfBirth = "Enter a valid date.";
  } else if (values.dateOfBirth > new Date().toISOString().slice(0, 10)) {
    errors.dateOfBirth = "Date of birth cannot be in the future.";
  }

  if (!values.maritalStatus) {
    errors.maritalStatus = "Select your marital status.";
  }

  if (!occupation) {
    errors.occupation = "Enter your occupation or profession.";
  } else if (occupation.length < 2) {
    errors.occupation = "Enter at least 2 characters.";
  }

  if (mobile && !/^[\d\s+\-()]{7,20}$/.test(mobile)) {
    errors.mobileNumber = "Enter a valid mobile number.";
  }

  if (!address) {
    errors.address = "Enter your street address.";
  } else if (address.length < 3) {
    errors.address = "Enter at least 3 characters.";
  }

  if (!city) {
    errors.city = "Enter the city where you live.";
  } else if (city.length < 2) {
    errors.city = "Enter at least 2 characters.";
  }

  if (!state) {
    errors.state = "Enter your state or province.";
  } else if (state.length < 2) {
    errors.state = "Enter at least 2 characters.";
  }

  if (!country) {
    errors.country = "Enter your country.";
  } else if (country.length < 2) {
    errors.country = "Enter at least 2 characters.";
  }

  return errors;
}
