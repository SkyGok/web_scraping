import {
  OverviewResponse,
  IndustrialZone,
  Company,
  Contact,
  Website,
  ScrapingJob,
} from '../types';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP Error ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

export const api = {
  // Overview
  async getOverview(): Promise<OverviewResponse> {
    return fetchJson<OverviewResponse>('/overview');
  },

  // Health
  async getHealth(): Promise<{ status: string; service: string; database: string }> {
    return fetchJson<{ status: string; service: string; database: string }>('/health');
  },

  // Zones
  async getZones(province?: string, search?: string): Promise<IndustrialZone[]> {
    const params = new URLSearchParams();
    if (province) params.append('province', province);
    if (search) params.append('search', search);
    const qs = params.toString() ? `?${params.toString()}` : '';
    return fetchJson<IndustrialZone[]>(`/zones${qs}`);
  },

  async seedZones(): Promise<{ message: string; seeded: number }> {
    return fetchJson<{ message: string; seeded: number }>('/zones/seed', {
      method: 'POST',
    });
  },

  // Companies
  async getCompanies(params?: {
    zone_id?: number;
    sector?: string;
    search?: string;
    has_contacts?: boolean;
    limit?: number;
    offset?: number;
  }): Promise<Company[]> {
    const urlParams = new URLSearchParams();
    if (params?.zone_id) urlParams.append('zone_id', params.zone_id.toString());
    if (params?.sector) urlParams.append('sector', params.sector);
    if (params?.search) urlParams.append('search', params.search);
    if (params?.has_contacts !== undefined) urlParams.append('has_contacts', params.has_contacts.toString());
    if (params?.limit) urlParams.append('limit', params.limit.toString());
    if (params?.offset) urlParams.append('offset', params.offset.toString());
    const qs = urlParams.toString() ? `?${urlParams.toString()}` : '';
    return fetchJson<Company[]>(`/companies${qs}`);
  },

  // Contacts
  async getContacts(params?: {
    company_id?: number;
    zone_id?: number;
    contact_type?: string;
    is_verified?: boolean;
    search?: string;
    limit?: number;
    offset?: number;
  }): Promise<Contact[]> {
    const urlParams = new URLSearchParams();
    if (params?.company_id) urlParams.append('company_id', params.company_id.toString());
    if (params?.zone_id) urlParams.append('zone_id', params.zone_id.toString());
    if (params?.contact_type) urlParams.append('contact_type', params.contact_type);
    if (params?.is_verified !== undefined) urlParams.append('is_verified', params.is_verified.toString());
    if (params?.search) urlParams.append('search', params.search);
    if (params?.limit) urlParams.append('limit', params.limit.toString());
    if (params?.offset) urlParams.append('offset', params.offset.toString());
    const qs = urlParams.toString() ? `?${urlParams.toString()}` : '';
    return fetchJson<Contact[]>(`/contacts${qs}`);
  },

  async toggleVerifyContact(contactId: number): Promise<Contact> {
    return fetchJson<Contact>(`/contacts/${contactId}/verify`, {
      method: 'PUT',
    });
  },

  // Websites
  async getWebsites(params?: {
    status?: string;
    crawl_mode?: string;
    search?: string;
  }): Promise<Website[]> {
    const urlParams = new URLSearchParams();
    if (params?.status) urlParams.append('status', params.status);
    if (params?.crawl_mode) urlParams.append('crawl_mode', params.crawl_mode);
    if (params?.search) urlParams.append('search', params.search);
    const qs = urlParams.toString() ? `?${urlParams.toString()}` : '';
    return fetchJson<Website[]>(`/websites${qs}`);
  },

  async updateWebsiteCrawlMode(websiteId: number, crawlMode: string): Promise<Website> {
    return fetchJson<Website>(`/websites/${websiteId}/crawl-mode`, {
      method: 'PUT',
      body: JSON.stringify({ crawl_mode: crawlMode }),
    });
  },

  async retryWebsite(websiteId: number): Promise<Website> {
    return fetchJson<Website>(`/websites/${websiteId}/retry`, {
      method: 'POST',
    });
  },

  // Jobs
  async getJobs(params?: {
    status?: string;
    job_type?: string;
    zone_id?: number;
  }): Promise<ScrapingJob[]> {
    const urlParams = new URLSearchParams();
    if (params?.status) urlParams.append('status', params.status);
    if (params?.job_type) urlParams.append('job_type', params.job_type);
    if (params?.zone_id) urlParams.append('zone_id', params.zone_id.toString());
    const qs = urlParams.toString() ? `?${urlParams.toString()}` : '';
    return fetchJson<ScrapingJob[]>(`/jobs${qs}`);
  },

  async createJob(payload: {
    zone_id?: number;
    website_id?: number;
    job_type: string;
    crawl_mode: string;
  }): Promise<ScrapingJob> {
    return fetchJson<ScrapingJob>('/jobs', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  async cancelJob(jobId: number): Promise<ScrapingJob> {
    return fetchJson<ScrapingJob>(`/jobs/${jobId}/cancel`, {
      method: 'POST',
    });
  },

  // Exports
  async getExportStatus(): Promise<{
    status: string;
    export_directory: string;
    available_exports: Array<{
      filename: string;
      size_bytes: number;
      created_at: string;
      download_url: string;
    }>;
    supported_sheets: string[];
  }> {
    return fetchJson('/exports/status');
  },
};
