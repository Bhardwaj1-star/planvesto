import type { Asset, AssetErrors } from "./types";

export function validateAsset(asset: Asset): AssetErrors {
  const errors: AssetErrors = {};
  const currentValue = Number(asset.currentValue);
  const purchaseValue = Number(asset.purchaseValue);

  if (!asset.assetType) errors.assetType = "Select an asset type.";
  if (!asset.description.trim()) errors.description = "Enter a name or description.";
  if (!asset.currentValue) {
    errors.currentValue = "Enter the current value.";
  } else if (!Number.isFinite(currentValue) || currentValue <= 0) {
    errors.currentValue = "Enter a value greater than zero.";
  }
  if (asset.purchaseValue && (!Number.isFinite(purchaseValue) || purchaseValue <= 0)) {
    errors.purchaseValue = "Enter a valid purchase value greater than zero.";
  }
  if (asset.purchaseDate) {
    const today = new Date().toISOString().slice(0, 10);
    if (asset.purchaseDate > today) {
      errors.purchaseDate = "Purchase date cannot be in the future.";
    }
  }

  return errors;
}