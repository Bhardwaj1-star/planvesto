export const assetTypes = [
  "Bank / Cash",
  "Fixed Deposits",
  "Mutual Funds",
  "Stocks / Equity",
  "Bonds / Debt",
  "EPF / PPF",
  "NPS",
  "Gold",
  "Real Estate",
  "Business Ownership",
  "Vehicle",
  "Other",
] as const;
export type AssetType = (typeof assetTypes)[number];

export type Asset = {
  id: string;
  assetType: AssetType | "";
  description: string;
  currentValue: string;
  purchaseValue: string;
  purchaseDate: string;
};

export type AssetField = keyof Omit<Asset, "id">;
export type AssetErrors = Partial<Record<AssetField, string>>;

export const emptyAsset: Omit<Asset, "id"> = {
  assetType: "",
  description: "",
  currentValue: "",
  purchaseValue: "",
  purchaseDate: "",
};