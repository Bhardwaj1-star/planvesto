"use client";

import {
  genderSelectOptions,
  maritalStatusSelectOptions,
  type PersonalInformationField,
  type SelectOption,
} from "../../../lib/onboarding/personal-information/model";
import { usePersonalInformationForm } from "../../../hooks/onboarding/personal-information/usePersonalInformationForm";
import { useFamilyDependents } from "../../../hooks/onboarding/family-dependents/useFamilyDependents";
import OnboardingShell from "../OnboardingShell";
import FamilySummary from "../family-dependents/FamilySummary";
import FamilyMemberForm from "../family-dependents/FamilyMemberForm";

type FieldProps = {
  name: PersonalInformationField;
  label: string;
  error?: string;
  required?: boolean;
  children: React.ReactNode;
};

function Field({ name, label, error, required = true, children }: FieldProps) {
  const errorId = `${name}-error`;

  return (
    <div>
      <label htmlFor={name} className="mb-2 block text-sm font-semibold text-navy-900">
        {label}
        {!required && <span className="ml-1 font-normal text-slate-400">(optional)</span>}
      </label>
      {children}
      {error && (
        <p id={errorId} className="mt-2 text-xs font-medium text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

function fieldClasses(hasError: boolean) {
  return `form-field w-full rounded-xl border bg-white px-4 py-3.5 text-sm text-navy-900 placeholder:text-slate-400 transition focus:border-teal-500 focus:outline-none focus:ring-4 focus:ring-teal-50 ${
    hasError ? "border-red-300" : "border-slate-200"
  }`;
}

function SelectField({
  name,
  options,
  value,
  error,
  onChange,
  onBlur,
}: {
  name: PersonalInformationField;
  options: SelectOption[];
  value: string;
  error?: string;
  onChange: (value: string) => void;
  onBlur: () => void;
}) {
  return (
    <select
      id={name}
      name={name}
      value={value}
      onChange={(event) => onChange(event.target.value)}
      onBlur={onBlur}
      aria-invalid={Boolean(error)}
      aria-describedby={error ? `${name}-error` : undefined}
      className={`${fieldClasses(Boolean(error))} appearance-none`}
    >
      <option value="">Select an option</option>
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}

export default function PersonalInformationForm() {
  const {
    values,
    errors,
    handleChange,
    handleBlur,
    handleSubmit,
    isComplete,
  } = usePersonalInformationForm();
  const family = useFamilyDependents();
  const today = new Date().toISOString().slice(0, 10);

  return (
    <OnboardingShell
      currentStep={1}
      title="Let's start with your profile"
      subtitle="Help us understand your life and household today. This gives your financial plan the context it deserves."
      stepContext="Profile & Household"
      badge={family.members.length > 0 ? `${family.members.length} member${family.members.length > 1 ? "s" : ""}` : undefined}
    >
      <div className="space-y-8">
        <form id="personal-info-form" noValidate onSubmit={handleSubmit} className="space-y-6">
          {/* Section 01: About You */}
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8" aria-labelledby="identity-heading">
            <div className="mb-6 border-b border-slate-100 pb-5">
              <div className="flex items-center gap-2">
                <span className="flex h-6 w-6 items-center justify-center rounded-md bg-teal-50 text-xs font-bold text-teal-700">01</span>
                <h2 id="identity-heading" className="text-lg font-bold text-navy-900 sm:text-xl">A little about you</h2>
              </div>
              <p className="mt-1 text-sm text-slate-500">The essentials that shape your financial context.</p>
            </div>
            <div className="grid gap-5 sm:grid-cols-2">
              <Field name="fullName" label="Full name" error={errors.fullName}>
                <input
                  id="fullName"
                  name="fullName"
                  type="text"
                  autoComplete="name"
                  value={values.fullName}
                  onChange={(event) => handleChange({ name: "fullName", value: event.target.value })}
                  onBlur={() => handleBlur("fullName")}
                  aria-invalid={Boolean(errors.fullName)}
                  aria-describedby={errors.fullName ? "fullName-error" : undefined}
                  placeholder="Your full name"
                  className={fieldClasses(Boolean(errors.fullName))}
                />
              </Field>
              <Field name="dateOfBirth" label="Date of birth" error={errors.dateOfBirth}>
                <input
                  id="dateOfBirth"
                  name="dateOfBirth"
                  type="date"
                  max={today}
                  autoComplete="bday"
                  value={values.dateOfBirth}
                  onChange={(event) => handleChange({ name: "dateOfBirth", value: event.target.value })}
                  onBlur={() => handleBlur("dateOfBirth")}
                  aria-invalid={Boolean(errors.dateOfBirth)}
                  aria-describedby={errors.dateOfBirth ? "dateOfBirth-error" : undefined}
                  className={fieldClasses(Boolean(errors.dateOfBirth))}
                />
              </Field>
              <Field name="gender" label="Gender" error={errors.gender} required={false}>
                <SelectField
                  name="gender"
                  options={genderSelectOptions}
                  value={values.gender}
                  error={errors.gender}
                  onChange={(value) => handleChange({ name: "gender", value })}
                  onBlur={() => handleBlur("gender")}
                />
              </Field>
              <Field name="maritalStatus" label="Marital status" error={errors.maritalStatus}>
                <SelectField
                  name="maritalStatus"
                  options={maritalStatusSelectOptions}
                  value={values.maritalStatus}
                  error={errors.maritalStatus}
                  onChange={(value) => handleChange({ name: "maritalStatus", value })}
                  onBlur={() => handleBlur("maritalStatus")}
                />
              </Field>
              <div className="sm:col-span-2">
                <Field name="mobileNumber" label="Mobile number" error={errors.mobileNumber} required={false}>
                  <input
                    id="mobileNumber"
                    name="mobileNumber"
                    type="tel"
                    autoComplete="tel"
                    value={values.mobileNumber}
                    onChange={(event) => handleChange({ name: "mobileNumber", value: event.target.value })}
                    onBlur={() => handleBlur("mobileNumber")}
                    aria-invalid={Boolean(errors.mobileNumber)}
                    aria-describedby={errors.mobileNumber ? "mobileNumber-error" : undefined}
                    placeholder="e.g. +1 555 123 4567"
                    className={fieldClasses(Boolean(errors.mobileNumber))}
                  />
                </Field>
              </div>
            </div>
          </section>

          {/* Section 02: Your Work */}
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8" aria-labelledby="work-heading">
            <div className="mb-6 border-b border-slate-100 pb-5">
              <div className="flex items-center gap-2">
                <span className="flex h-6 w-6 items-center justify-center rounded-md bg-teal-50 text-xs font-bold text-teal-700">02</span>
                <h2 id="work-heading" className="text-lg font-bold text-navy-900 sm:text-xl">Your work</h2>
              </div>
              <p className="mt-1 text-sm text-slate-500">Your occupation helps us understand your earning context.</p>
            </div>
            <Field name="occupation" label="Occupation / profession" error={errors.occupation}>
              <input
                id="occupation"
                name="occupation"
                type="text"
                autoComplete="organization-title"
                value={values.occupation}
                onChange={(event) => handleChange({ name: "occupation", value: event.target.value })}
                onBlur={() => handleBlur("occupation")}
                aria-invalid={Boolean(errors.occupation)}
                aria-describedby={errors.occupation ? "occupation-error" : undefined}
                placeholder="e.g. Product designer, Engineer, Physician"
                className={fieldClasses(Boolean(errors.occupation))}
              />
            </Field>
          </section>

          {/* Section 03: Where You Live */}
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8" aria-labelledby="life-heading">
            <div className="mb-6 border-b border-slate-100 pb-5">
              <div className="flex items-center gap-2">
                <span className="flex h-6 w-6 items-center justify-center rounded-md bg-teal-50 text-xs font-bold text-teal-700">03</span>
                <h2 id="life-heading" className="text-lg font-bold text-navy-900 sm:text-xl">Where you live</h2>
              </div>
              <p className="mt-1 text-sm text-slate-500">Your address and location keep your financial plan grounded in your reality.</p>
            </div>
            <div className="grid gap-5 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <Field name="address" label="Street address" error={errors.address}>
                  <input
                    id="address"
                    name="address"
                    type="text"
                    autoComplete="street-address"
                    value={values.address}
                    onChange={(event) => handleChange({ name: "address", value: event.target.value })}
                    onBlur={() => handleBlur("address")}
                    aria-invalid={Boolean(errors.address)}
                    aria-describedby={errors.address ? "address-error" : undefined}
                    placeholder="e.g. 123 Main St, Apt 4B"
                    className={fieldClasses(Boolean(errors.address))}
                  />
                </Field>
              </div>
              <Field name="city" label="City" error={errors.city}>
                <input
                  id="city"
                  name="city"
                  type="text"
                  autoComplete="address-level2"
                  value={values.city}
                  onChange={(event) => handleChange({ name: "city", value: event.target.value })}
                  onBlur={() => handleBlur("city")}
                  aria-invalid={Boolean(errors.city)}
                  aria-describedby={errors.city ? "city-error" : undefined}
                  placeholder="City"
                  className={fieldClasses(Boolean(errors.city))}
                />
              </Field>
              <Field name="state" label="State / Province" error={errors.state}>
                <input
                  id="state"
                  name="state"
                  type="text"
                  autoComplete="address-level1"
                  value={values.state}
                  onChange={(event) => handleChange({ name: "state", value: event.target.value })}
                  onBlur={() => handleBlur("state")}
                  aria-invalid={Boolean(errors.state)}
                  aria-describedby={errors.state ? "state-error" : undefined}
                  placeholder="State or Province"
                  className={fieldClasses(Boolean(errors.state))}
                />
              </Field>
              <div className="sm:col-span-2">
                <Field name="country" label="Country" error={errors.country}>
                  <input
                    id="country"
                    name="country"
                    type="text"
                    autoComplete="country-name"
                    value={values.country}
                    onChange={(event) => handleChange({ name: "country", value: event.target.value })}
                    onBlur={() => handleBlur("country")}
                    aria-invalid={Boolean(errors.country)}
                    aria-describedby={errors.country ? "country-error" : undefined}
                    placeholder="Country"
                    className={fieldClasses(Boolean(errors.country))}
                  />
                </Field>
              </div>
            </div>
          </section>
        </form>

        {/* Section 04: Family & Dependents */}
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8" aria-labelledby="family-heading">
          <div className="mb-6 border-b border-slate-100 pb-5">
            <div className="flex items-center gap-2">
              <span className="flex h-6 w-6 items-center justify-center rounded-md bg-teal-50 text-xs font-bold text-teal-700">04</span>
              <h2 id="family-heading" className="text-lg font-bold text-navy-900 sm:text-xl">Family &amp; Dependents</h2>
            </div>
            <p className="mt-1 text-sm text-slate-500">
              Financial decisions can affect the people you support today, as well as the people you plan to support in the future.
            </p>
          </div>

          <div className="space-y-6">
            <FamilySummary
              members={family.members}
              onEdit={family.startEditing}
              onRemove={family.removeMember}
            />

            <FamilyMemberForm
              member={family.draft}
              errors={family.errors}
              isEditing={Boolean(family.editingMemberId)}
              onChange={family.updateDraft}
              onSave={family.saveMember}
              onCancel={family.cancelEditing}
            />
          </div>
        </section>

        {/* Action Bar */}
        <div className="flex flex-col-reverse items-stretch gap-4 pt-4 sm:flex-row sm:items-center sm:justify-between border-t border-slate-200/80">
          <p className="text-xs leading-5 text-slate-400">
            Step 1 of 6 · Personal information is kept private and secure.
          </p>
          <button
            type="submit"
            form="personal-info-form"
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-7 py-3.5 text-sm font-bold text-white shadow-sm transition hover:bg-navy-800 focus:outline-none focus:ring-4 focus:ring-teal-100 disabled:cursor-not-allowed disabled:opacity-60"
          >
            Continue to Income
            <span aria-hidden="true">&rarr;</span>
          </button>
        </div>

        {isComplete && (
          <p className="rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700" role="status">
            Personal information is complete for this session.
          </p>
        )}
      </div>
    </OnboardingShell>
  );
}
