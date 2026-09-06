export type Commitment = {
  id: string;
  name: string;
  amount: string;
};

export type CommitmentField = keyof Omit<Commitment, "id">;
export type CommitmentErrors = Partial<Record<CommitmentField, string>>;

export const emptyCommitment: Omit<Commitment, "id"> = {
  name: "",
  amount: "",
};
