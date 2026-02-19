export type FindingsSummary = {
  low: number;
  medium: number;
  high: number;
  critical: number;
};

export type SecurityFinding = {
  finding_uid: string;
  standard: string;
  schema_version: string;
  status: string;
  severity_id: number;
  severity: string;
  risk_score: number;
  title: string;
  description: string;
  category_name: string;
  class_name: string;
  type_name: string;
  domain: string;
  activity_name: string;
  time: string;
  source: string;
  resource: {
    uid: string;
    name: string;
    type: string;
    platform: string;
  };
  references: {
    cve: string[];
    cwe: string[];
    owasp: string[];
    mitre_attack: string[];
  };
  raw_data: Record<string, unknown>;
};
