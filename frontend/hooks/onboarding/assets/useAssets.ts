"use client";

import { useState } from "react";
import { useOnboardingNavigation, useOnboardingStore } from "../../../components/onboarding/OnboardingProvider";
import { createAssetId } from "../../../lib/onboarding/assets/assets";
import { emptyAsset, type Asset, type AssetErrors } from "../../../lib/onboarding/assets/types";
import { validateAsset } from "../../../lib/onboarding/assets/validation";

export function useAssets() {
  const { assets, setAssets, saveAssets } = useOnboardingStore();
  const { completeStep, goNext, goPrevious } = useOnboardingNavigation(4);
  const [draft, setDraft] = useState<Asset>({ id: createAssetId(), ...emptyAsset });
  const [editingAssetId, setEditingAssetId] = useState<string | null>(null);
  const [errors, setErrors] = useState<AssetErrors>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  function startAdding() {
    setDraft({ id: createAssetId(), ...emptyAsset });
    setEditingAssetId(null);
    setErrors({});
    setIsSubmitted(false);
  }

  function startEditing(asset: Asset) {
    setDraft({ ...asset });
    setEditingAssetId(asset.id);
    setErrors({});
    setIsSubmitted(false);
  }

  function cancelEditing() {
    startAdding();
  }

  function updateDraft(changes: Partial<Asset>) {
    const nextDraft = { ...draft, ...changes };
    setDraft(nextDraft);
    setIsComplete(false);
    if (isSubmitted) setErrors(validateAsset(nextDraft));
  }

  async function saveAsset(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const nextErrors = validateAsset(draft);
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      document.getElementById(Object.keys(nextErrors)[0])?.focus();
      return false;
    }

    const nextAssets = editingAssetId
      ? assets.map((asset) => asset.id === editingAssetId ? draft : asset)
      : [...assets, draft];
    setAssets(nextAssets);
    try {
      const data = await saveAssets(nextAssets);
      setAssets(data.assets);
    } catch {
      return false;
    }
    startAdding();
    return true;
  }

  async function removeAsset(id: string) {
    const nextAssets = assets.filter((asset) => asset.id !== id);
    setAssets(nextAssets);
    try {
      const data = await saveAssets(nextAssets);
      setAssets(data.assets);
    } catch {
      return;
    }
    if (editingAssetId === id) startAdding();
    setIsComplete(false);
  }

  async function handleContinue(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const assetErrors = assets.map((asset) => validateAsset(asset));
    const invalidIndex = assetErrors.findIndex((assetErrorsForItem) => Object.keys(assetErrorsForItem).length > 0);
    if (invalidIndex >= 0) {
      setEditingAssetId(assets[invalidIndex].id);
      setDraft(assets[invalidIndex]);
      setErrors(assetErrors[invalidIndex]);
      return;
    }
    try {
      const data = await saveAssets(assets);
      setAssets(data.assets);
    } catch {
      return;
    }
    setIsComplete(true);
    completeStep(4);
    goNext();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return {
    assets,
    draft,
    editingAssetId,
    errors,
    isComplete,
    startEditing,
    updateDraft,
    saveAsset,
    removeAsset,
    cancelEditing,
    handleContinue,
    goPrevious,
  };
}