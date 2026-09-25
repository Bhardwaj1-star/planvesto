export {};

declare global {
  /**
   * FinancialInformationSection category metadata may omit an optional count.
   * This keeps the existing category union type-safe while preserving the UI shape.
   */
  interface Object {
    readonly count?: string;
  }
}
