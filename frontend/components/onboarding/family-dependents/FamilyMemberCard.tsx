import { getDependencySummary } from "../../../lib/onboarding/family-dependents/familyDependents";
import type { FamilyMember } from "../../../lib/onboarding/family-dependents/types";

type Props = { member: FamilyMember; onEdit: () => void; onRemove: () => void };

export default function FamilyMemberCard({ member, onEdit, onRemove }: Props) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-extrabold text-navy-900">{member.name}</h3>
          <p className="mt-1 text-sm text-slate-500">{member.relationship}{member.occupation ? ` • ${member.occupation}` : ""}</p>
        </div>
        <div className="flex shrink-0 gap-3 text-sm font-bold">
          <button type="button" onClick={onEdit} className="text-teal-700 underline decoration-teal-200 underline-offset-4 hover:text-teal-800">Edit</button>
          <button type="button" onClick={onRemove} className="text-slate-500 underline decoration-slate-200 underline-offset-4 hover:text-red-600">Remove</button>
        </div>
      </div>
      <div className="mt-4 flex flex-wrap gap-2 text-xs font-semibold text-slate-600">
        <span className="rounded-full bg-slate-100 px-3 py-1">Born {member.dateOfBirth}</span>
        <span className="rounded-full bg-teal-50 px-3 py-1 text-teal-700">{getDependencySummary(member)}</span>
        {member.includeInPlanning && (
          <span className="rounded-full bg-navy-50 px-3 py-1 font-bold text-navy-800">In Planning</span>
        )}
      </div>
    </article>
  );
}