export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "14.5"
  }
  public: {
    Tables: {
      asset_owners: {
        Row: {
          asset_id: string
          asset_owner_id: string
          created_at: string
          investor_id: string
          ownership_percentage: number
          updated_at: string
        }
        Insert: {
          asset_id: string
          asset_owner_id?: string
          created_at?: string
          investor_id: string
          ownership_percentage: number
          updated_at?: string
        }
        Update: {
          asset_id?: string
          asset_owner_id?: string
          created_at?: string
          investor_id?: string
          ownership_percentage?: number
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_asset_owner_asset"
            columns: ["asset_id"]
            isOneToOne: false
            referencedRelation: "assets"
            referencedColumns: ["asset_id"]
          },
          {
            foreignKeyName: "fk_asset_owner_investor"
            columns: ["investor_id"]
            isOneToOne: false
            referencedRelation: "investors"
            referencedColumns: ["investor_id"]
          },
        ]
      }
      assets: {
        Row: {
          asset_id: string
          asset_name: string
          created_at: string
          current_value: number
          planning_unit_id: string
          purchase_date: string | null
          purchase_value: number | null
          updated_at: string
        }
        Insert: {
          asset_id?: string
          asset_name: string
          created_at?: string
          current_value: number
          planning_unit_id: string
          purchase_date?: string | null
          purchase_value?: number | null
          updated_at?: string
        }
        Update: {
          asset_id?: string
          asset_name?: string
          created_at?: string
          current_value?: number
          planning_unit_id?: string
          purchase_date?: string | null
          purchase_value?: number | null
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_asset_planning_unit"
            columns: ["planning_unit_id"]
            isOneToOne: false
            referencedRelation: "planning_units"
            referencedColumns: ["planning_unit_id"]
          },
        ]
      }
      commitment_participants: {
        Row: {
          commitment_id: string
          commitment_participant_id: string
          created_at: string
          investor_id: string
          participation_percentage: number
          updated_at: string
        }
        Insert: {
          commitment_id: string
          commitment_participant_id?: string
          created_at?: string
          investor_id: string
          participation_percentage: number
          updated_at?: string
        }
        Update: {
          commitment_id?: string
          commitment_participant_id?: string
          created_at?: string
          investor_id?: string
          participation_percentage?: number
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_commitment_participant_commitment"
            columns: ["commitment_id"]
            isOneToOne: false
            referencedRelation: "commitments"
            referencedColumns: ["commitment_id"]
          },
          {
            foreignKeyName: "fk_commitment_participant_investor"
            columns: ["investor_id"]
            isOneToOne: false
            referencedRelation: "investors"
            referencedColumns: ["investor_id"]
          },
        ]
      }
      commitments: {
        Row: {
          amount: number
          commitment_id: string
          commitment_name: string
          created_at: string
          planning_unit_id: string
          updated_at: string
        }
        Insert: {
          amount: number
          commitment_id?: string
          commitment_name: string
          created_at?: string
          planning_unit_id: string
          updated_at?: string
        }
        Update: {
          amount?: number
          commitment_id?: string
          commitment_name?: string
          created_at?: string
          planning_unit_id?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_commitment_planning_unit"
            columns: ["planning_unit_id"]
            isOneToOne: false
            referencedRelation: "planning_units"
            referencedColumns: ["planning_unit_id"]
          },
        ]
      }
      dependents: {
        Row: {
          created_at: string
          date_of_birth: string | null
          dependent_id: string
          financial_dependency: boolean | null
          include_in_planning: boolean
          name: string
          occupation: string | null
          planning_unit_id: string
          relationship: string | null
          updated_at: string
        }
        Insert: {
          created_at?: string
          date_of_birth?: string | null
          dependent_id?: string
          financial_dependency?: boolean | null
          include_in_planning?: boolean
          name: string
          occupation?: string | null
          planning_unit_id: string
          relationship?: string | null
          updated_at?: string
        }
        Update: {
          created_at?: string
          date_of_birth?: string | null
          dependent_id?: string
          financial_dependency?: boolean | null
          include_in_planning?: boolean
          name?: string
          occupation?: string | null
          planning_unit_id?: string
          relationship?: string | null
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_dependent_planning_unit"
            columns: ["planning_unit_id"]
            isOneToOne: false
            referencedRelation: "planning_units"
            referencedColumns: ["planning_unit_id"]
          },
        ]
      }
      expense_participants: {
        Row: {
          created_at: string
          expense_id: string
          expense_participant_id: string
          investor_id: string
          participation_percentage: number
          updated_at: string
        }
        Insert: {
          created_at?: string
          expense_id: string
          expense_participant_id?: string
          investor_id: string
          participation_percentage: number
          updated_at?: string
        }
        Update: {
          created_at?: string
          expense_id?: string
          expense_participant_id?: string
          investor_id?: string
          participation_percentage?: number
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_expense_participant_expense"
            columns: ["expense_id"]
            isOneToOne: false
            referencedRelation: "expenses"
            referencedColumns: ["expense_id"]
          },
          {
            foreignKeyName: "fk_expense_participant_investor"
            columns: ["investor_id"]
            isOneToOne: false
            referencedRelation: "investors"
            referencedColumns: ["investor_id"]
          },
        ]
      }
      expenses: {
        Row: {
          amount: number
          created_at: string
          expense_id: string
          expense_type: string
          frequency: string
          planning_unit_id: string
          updated_at: string
        }
        Insert: {
          amount: number
          created_at?: string
          expense_id?: string
          expense_type: string
          frequency: string
          planning_unit_id: string
          updated_at?: string
        }
        Update: {
          amount?: number
          created_at?: string
          expense_id?: string
          expense_type?: string
          frequency?: string
          planning_unit_id?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_expense_planning_unit"
            columns: ["planning_unit_id"]
            isOneToOne: false
            referencedRelation: "planning_units"
            referencedColumns: ["planning_unit_id"]
          },
        ]
      }
      goal_funding: {
        Row: {
          allocation_percentage: number
          asset_id: string
          created_at: string
          goal_funding_id: string
          goal_id: string
          updated_at: string
        }
        Insert: {
          allocation_percentage: number
          asset_id: string
          created_at?: string
          goal_funding_id?: string
          goal_id: string
          updated_at?: string
        }
        Update: {
          allocation_percentage?: number
          asset_id?: string
          created_at?: string
          goal_funding_id?: string
          goal_id?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_goal_funding_asset"
            columns: ["asset_id"]
            isOneToOne: false
            referencedRelation: "assets"
            referencedColumns: ["asset_id"]
          },
          {
            foreignKeyName: "fk_goal_funding_goal"
            columns: ["goal_id"]
            isOneToOne: false
            referencedRelation: "goals"
            referencedColumns: ["goal_id"]
          },
        ]
      }
      goals: {
        Row: {
          created_at: string
          flexibility: string | null
          goal_id: string
          goal_name: string
          planning_unit_id: string
          priority: string | null
          target_amount: number
          target_date: string | null
          updated_at: string
        }
        Insert: {
          created_at?: string
          flexibility?: string | null
          goal_id?: string
          goal_name: string
          planning_unit_id: string
          priority?: string | null
          target_amount: number
          target_date?: string | null
          updated_at?: string
        }
        Update: {
          created_at?: string
          flexibility?: string | null
          goal_id?: string
          goal_name?: string
          planning_unit_id?: string
          priority?: string | null
          target_amount?: number
          target_date?: string | null
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_goal_planning_unit"
            columns: ["planning_unit_id"]
            isOneToOne: false
            referencedRelation: "planning_units"
            referencedColumns: ["planning_unit_id"]
          },
        ]
      }
      income: {
        Row: {
          amount: number
          created_at: string
          frequency: string
          growth_assumption: number | null
          income_id: string
          income_type: string
          investor_id: string
          planning_unit_id: string
          updated_at: string
        }
        Insert: {
          amount: number
          created_at?: string
          frequency: string
          growth_assumption?: number | null
          income_id?: string
          income_type: string
          investor_id: string
          planning_unit_id: string
          updated_at?: string
        }
        Update: {
          amount?: number
          created_at?: string
          frequency?: string
          growth_assumption?: number | null
          income_id?: string
          income_type?: string
          investor_id?: string
          planning_unit_id?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_income_investor"
            columns: ["investor_id"]
            isOneToOne: false
            referencedRelation: "investors"
            referencedColumns: ["investor_id"]
          },
          {
            foreignKeyName: "fk_income_planning_unit"
            columns: ["planning_unit_id"]
            isOneToOne: false
            referencedRelation: "planning_units"
            referencedColumns: ["planning_unit_id"]
          },
        ]
      }
      investors: {
        Row: {
          address: string | null
          city: string | null
          country: string | null
          created_at: string
          date_of_birth: string | null
          full_name: string
          gender: string | null
          investor_id: string
          marital_status: string | null
          mobile_number: string | null
          occupation: string | null
          planning_unit_id: string
          state: string | null
          updated_at: string
        }
        Insert: {
          address?: string | null
          city?: string | null
          country?: string | null
          created_at?: string
          date_of_birth?: string | null
          full_name: string
          gender?: string | null
          investor_id?: string
          marital_status?: string | null
          mobile_number?: string | null
          occupation?: string | null
          planning_unit_id: string
          state?: string | null
          updated_at?: string
        }
        Update: {
          address?: string | null
          city?: string | null
          country?: string | null
          created_at?: string
          date_of_birth?: string | null
          full_name?: string
          gender?: string | null
          investor_id?: string
          marital_status?: string | null
          mobile_number?: string | null
          occupation?: string | null
          planning_unit_id?: string
          state?: string | null
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_investor_planning_unit"
            columns: ["planning_unit_id"]
            isOneToOne: false
            referencedRelation: "planning_units"
            referencedColumns: ["planning_unit_id"]
          },
        ]
      }
      liabilities: {
        Row: {
          created_at: string
          emi_amount: number | null
          end_date: string | null
          frequency: string | null
          interest_rate: number | null
          liability_id: string
          liability_name: string
          outstanding_amount: number
          planning_unit_id: string
          updated_at: string
        }
        Insert: {
          created_at?: string
          emi_amount?: number | null
          end_date?: string | null
          frequency?: string | null
          interest_rate?: number | null
          liability_id?: string
          liability_name: string
          outstanding_amount: number
          planning_unit_id: string
          updated_at?: string
        }
        Update: {
          created_at?: string
          emi_amount?: number | null
          end_date?: string | null
          frequency?: string | null
          interest_rate?: number | null
          liability_id?: string
          liability_name?: string
          outstanding_amount?: number
          planning_unit_id?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_liability_planning_unit"
            columns: ["planning_unit_id"]
            isOneToOne: false
            referencedRelation: "planning_units"
            referencedColumns: ["planning_unit_id"]
          },
        ]
      }
      liability_responsibilities: {
        Row: {
          created_at: string
          investor_id: string
          liability_id: string
          liability_responsibility_id: string
          responsibility_percentage: number
          updated_at: string
        }
        Insert: {
          created_at?: string
          investor_id: string
          liability_id: string
          liability_responsibility_id?: string
          responsibility_percentage: number
          updated_at?: string
        }
        Update: {
          created_at?: string
          investor_id?: string
          liability_id?: string
          liability_responsibility_id?: string
          responsibility_percentage?: number
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_liability_responsibility_investor"
            columns: ["investor_id"]
            isOneToOne: false
            referencedRelation: "investors"
            referencedColumns: ["investor_id"]
          },
          {
            foreignKeyName: "fk_liability_responsibility_liability"
            columns: ["liability_id"]
            isOneToOne: false
            referencedRelation: "liabilities"
            referencedColumns: ["liability_id"]
          },
        ]
      }
      planning_units: {
        Row: {
          created_at: string
          planning_unit_id: string
          user_id: string | null
          updated_at: string
        }
        Insert: {
          created_at?: string
          planning_unit_id?: string
          user_id?: string | null
          updated_at?: string
        }
        Update: {
          created_at?: string
          planning_unit_id?: string
          user_id?: string | null
          updated_at?: string
        }
        Relationships: []
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends (DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never) = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends (DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never) = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends (DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never) = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends (DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never) = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends (PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never) = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {},
  },
} as const

