import type { Asset, AssetType } from "./types";

const financialAssetTypes: AssetType[] = ["Bank / Cash", "Fixed Deposits", "Mutual Funds", "Stocks / Equity", "Bonds / Debt", "EPF / PPF", "NPS"];
const physicalAssetTypes: AssetType[] = ["Gold", "Real Estate", "Business Ownership", "Vehicle", "Other"];
const purchaseValueAssetTypes: AssetType[] = ["Fixed Deposits", "Mutual Funds", "Stocks / Equity", "Bonds / Debt", "EPF / PPF", "NPS", "Gold", "Real Estate", "Business Ownership", "Vehicle", "Other"];

export function createAssetId() {
  return `asset-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

export function annualAssetValue(asset: Asset) {
  return Number(asset.currentValue);
}

export function getTotalAssets(assets: Asset[]) {
  return assets.reduce((total, asset) => total + annualAssetValue(asset), 0);
}

export function isFinancialAsset(asset: Asset) {
  return financialAssetTypes.includes(asset.assetType as AssetType);
}

export function isPhysicalAsset(asset: Asset) {
  return physicalAssetTypes.includes(asset.assetType as AssetType);
}

export function supportsPurchaseValue(assetType: AssetType | "") {
  return purchaseValueAssetTypes.includes(assetType as AssetType);
}

export function formatCurrency(amount: number) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(amount);
}