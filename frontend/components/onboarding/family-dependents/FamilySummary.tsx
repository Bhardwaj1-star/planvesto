import type { FamilyMember } from "../../../lib/onboarding/family-dependents/types";
import FamilyMemberCard from "./FamilyMemberCard";

type Props = { members: FamilyMember[]; onEdit: (member: FamilyMember) => void; onRemove: (id: string) => void };

export default function FamilySummary({ members, onEdit, onRemove }: Props) {
  if (members.length === 0) {
    return <div className="rounded-[28px] border border-dashed border-slate-300 bg-white px-6 py-10 text-center sm:px-8"><div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-teal-50 text-teal-700" aria-hidden="true">+</div><h2 className="mt-4 text-lg font-extrabold text-navy-900">No family members added yet</h2><p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">You can continue without adding anyone. Add a family member when someone else&apos;s needs belong in your financial plan.</p></div>;
  }

  return <div className="space-y-3">{members.map((member) => <FamilyMemberCard key={member.id} member={member} onEdit={() => onEdit(member)} onRemove={() => onRemove(member.id)} />)}</div>;
}