export type ViewType =
  | 'overview'
  | 'zones'
  | 'companies'
  | 'contacts'
  | 'websites'
  | 'jobs'
  | 'exports';

export interface MetricStats {
  total_zones: number;
  total_companies: number;
  total_contacts: number;
  total_websites: number;
  active_jobs: number;
  completed_jobs: number;
  failed_jobs: number;
  scraped_pages: number;
  verified_contacts_count: number;
}

export interface OSBSummary {
  id: number;
  name: string;
  province: string;
  district?: string;
  company_count: number;
  contact_count: number;
  website_status: string;
  portal_type: string;
}

export interface RecentJobSummary {
  id: number;
  job_type: string;
  status: string;
  crawl_mode: string;
  zone_name?: string;
  total_targets: number;
  processed_targets: number;
  success_count: number;
  error_count: number;
  started_at?: string;
  finished_at?: string;
}

export interface OverviewResponse {
  metrics: MetricStats;
  osb_summaries: OSBSummary[];
  recent_jobs: RecentJobSummary[];
}

export interface IndustrialZone {
  id: number;
  name: string;
  slug: string;
  province: string;
  district?: string;
  official_website?: string;
  portal_type: string;
  description?: string;
  is_active: boolean;
  company_count: number;
  contact_count: number;
  created_at: string;
  updated_at: string;
}

export interface Company {
  id: number;
  zone_id: number;
  zone_name?: string;
  name: string;
  normalized_name?: string;
  slug: string;
  registration_number?: string;
  tax_number?: string;
  sector?: string;
  address?: string;
  city: string;
  district?: string;
  description?: string;
  primary_website?: string;
  phone?: string;
  email?: string;
  is_active: boolean;
  contact_count: number;
  created_at: string;
  updated_at: string;
}

export interface Contact {
  id: number;
  company_id: number;
  company_name?: string;
  zone_name?: string;
  contact_type: string;
  value: string;
  label?: string;
  person_name?: string;
  department?: string;
  source_url?: string;
  confidence_score: number;
  is_verified: boolean;
  is_public: boolean;
  retrieved_at: string;
  created_at: string;
  updated_at: string;
}

export interface Website {
  id: number;
  domain: string;
  base_url: string;
  zone_id?: number;
  zone_name?: string;
  company_id?: number;
  company_name?: string;
  status: 'pending' | 'queued' | 'in_progress' | 'completed' | 'failed' | 'paused';
  crawl_mode: 'new_only' | 'retry_failed' | 'refresh_all';
  crawl_delay: number;
  robots_allowed: boolean;
  pages_count: number;
  last_visited_at?: string;
  last_success_at?: string;
  error_message?: string;
  http_status?: number;
  retry_count: number;
  created_at: string;
  updated_at: string;
}

export interface ScrapingJob {
  id: number;
  zone_id?: number;
  zone_name?: string;
  website_id?: number;
  website_domain?: string;
  job_type: string;
  status: string;
  crawl_mode: string;
  total_targets: number;
  processed_targets: number;
  success_count: number;
  error_count: number;
  started_at?: string;
  finished_at?: string;
  error_log?: string;
  created_at: string;
  updated_at: string;
}
