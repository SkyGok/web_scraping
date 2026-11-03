import React, { useState, useEffect, useCallback } from 'react';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { OverviewView } from './views/OverviewView';
import { IndustrialZonesView } from './views/IndustrialZonesView';
import { CompaniesView } from './views/CompaniesView';
import { ContactsView } from './views/ContactsView';
import { WebsiteManagementView } from './views/WebsiteManagementView';
import { ScrapingHistoryView } from './views/ScrapingHistoryView';
import { ExcelExportsView } from './views/ExcelExportsView';
import { api } from './services/api';
import {
  ViewType,
  OverviewResponse,
  IndustrialZone,
  Company,
  Contact,
  Website,
  ScrapingJob,
} from './types';

export const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<ViewType>('overview');
  const [overviewData, setOverviewData] = useState<OverviewResponse | null>(null);
  const [zones, setZones] = useState<IndustrialZone[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [websites, setWebsites] = useState<Website[]>([]);
  const [jobs, setJobs] = useState<ScrapingJob[]>([]);
  const [exportStatus, setExportStatus] = useState<any>(null);

  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [isSeeding, setIsSeeding] = useState<boolean>(false);
  const [isTriggeringJob, setIsTriggeringJob] = useState<boolean>(false);
  const [apiHealthy, setApiHealthy] = useState<boolean>(true);
  const [notification, setNotification] = useState<string | null>(null);

  const showNotification = (msg: string) => {
    setNotification(msg);
    setTimeout(() => setNotification(null), 3500);
  };

  // Fetch all state
  const loadAllData = useCallback(async () => {
    setIsRefreshing(true);
    try {
      // Check health
      await api.getHealth().catch(() => setApiHealthy(false));
      setApiHealthy(true);

      const [ov, zList, cList, ctList, wList, jList, exp] = await Promise.all([
        api.getOverview().catch(() => null),
        api.getZones().catch(() => []),
        api.getCompanies().catch(() => []),
        api.getContacts().catch(() => []),
        api.getWebsites().catch(() => []),
        api.getJobs().catch(() => []),
        api.getExportStatus().catch(() => null),
      ]);

      if (ov) setOverviewData(ov);
      setZones(zList);
      setCompanies(cList);
      setContacts(ctList);
      setWebsites(wList);
      setJobs(jList);
      setExportStatus(exp);
    } catch (err: any) {
      console.warn('Backend load error:', err);
    } finally {
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadAllData();
  }, [loadAllData]);

  // Handle Seeding
  const handleSeed = async () => {
    setIsSeeding(true);
    try {
      const res = await api.seedZones();
      showNotification(res.message);
      await loadAllData();
    } catch (err: any) {
      showNotification(`Seeding error: ${err.message}`);
    } finally {
      setIsSeeding(false);
    }
  };

  // Handle Crawl Mode Update
  const handleUpdateWebsiteMode = async (
    websiteId: number,
    mode: 'new_only' | 'retry_failed' | 'refresh_all'
  ) => {
    try {
      await api.updateWebsiteCrawlMode(websiteId, mode);
      showNotification(`Website crawl mode set to: ${mode}`);
      const updatedWebsites = await api.getWebsites();
      setWebsites(updatedWebsites);
    } catch (err: any) {
      showNotification(`Mode update failed: ${err.message}`);
    }
  };

  // Handle Retry Website
  const handleRetryWebsite = async (websiteId: number) => {
    try {
      await api.retryWebsite(websiteId);
      showNotification('Website re-queued for scraping with backoff.');
      const updatedWebsites = await api.getWebsites();
      setWebsites(updatedWebsites);
    } catch (err: any) {
      showNotification(`Retry failed: ${err.message}`);
    }
  };

  // Handle Trigger Job
  const handleTriggerJob = async (payload: {
    zone_id?: number;
    job_type: string;
    crawl_mode: string;
  }) => {
    setIsTriggeringJob(true);
    try {
      const job = await api.createJob(payload);
      showNotification(`Job #${job.id} queued successfully in RQ worker!`);
      const updatedJobs = await api.getJobs();
      setJobs(updatedJobs);
      setCurrentView('jobs');
    } catch (err: any) {
      showNotification(`Failed to queue job: ${err.message}`);
    } finally {
      setIsTriggeringJob(false);
    }
  };

  // Handle Quick Job Start from OSB table
  const handleStartJobForZone = (zoneId: number, zoneName: string) => {
    handleTriggerJob({
      zone_id: zoneId,
      job_type: 'company_discovery',
      crawl_mode: 'new_only',
    });
  };

  // Handle Contact Verification Toggle
  const handleToggleVerifyContact = async (contactId: number) => {
    try {
      const updated = await api.toggleVerifyContact(contactId);
      setContacts((prev) =>
        prev.map((c) => (c.id === contactId ? { ...c, is_verified: updated.is_verified } : c))
      );
      showNotification(`Contact marked as ${updated.is_verified ? 'Verified' : 'Unverified'}`);
    } catch (err: any) {
      showNotification(`Verification toggle failed: ${err.message}`);
    }
  };

  // Handle Cancel Job
  const handleCancelJob = async (jobId: number) => {
    try {
      await api.cancelJob(jobId);
      showNotification(`Job #${jobId} cancelled.`);
      const updatedJobs = await api.getJobs();
      setJobs(updatedJobs);
    } catch (err: any) {
      showNotification(`Cancellation error: ${err.message}`);
    }
  };

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-slate-950 text-slate-100">
      <Header
        onRefresh={loadAllData}
        isRefreshing={isRefreshing}
        onSeed={handleSeed}
        isSeeding={isSeeding}
        apiHealthy={apiHealthy}
      />

      {notification && (
        <div className="bg-blue-600 text-white text-xs px-4 py-2 font-mono flex items-center justify-between shadow-lg sticky top-16 z-30 animate-in fade-in slide-in-from-top duration-200">
          <span>{notification}</span>
          <button
            onClick={() => setNotification(null)}
            className="text-blue-200 hover:text-white ml-4 font-bold"
          >
            ✕
          </button>
        </div>
      )}

      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          currentView={currentView}
          onViewChange={setCurrentView}
          counts={{
            zones: zones.length,
            companies: companies.length,
            contacts: contacts.length,
            websites: websites.length,
            activeJobs: jobs.filter((j) => j.status === 'running').length,
          }}
        />

        <main className="flex-1 overflow-y-auto p-6 bg-slate-950/90">
          {currentView === 'overview' && (
            <OverviewView
              data={overviewData}
              onNavigate={setCurrentView}
              onStartJob={handleStartJobForZone}
            />
          )}

          {currentView === 'zones' && (
            <IndustrialZonesView
              zones={zones}
              onSeed={handleSeed}
              isSeeding={isSeeding}
              onStartJob={handleStartJobForZone}
            />
          )}

          {currentView === 'companies' && (
            <CompaniesView companies={companies} zones={zones} />
          )}

          {currentView === 'contacts' && (
            <ContactsView
              contacts={contacts}
              onToggleVerify={handleToggleVerifyContact}
            />
          )}

          {currentView === 'websites' && (
            <WebsiteManagementView
              websites={websites}
              onUpdateMode={handleUpdateWebsiteMode}
              onRetry={handleRetryWebsite}
            />
          )}

          {currentView === 'jobs' && (
            <ScrapingHistoryView
              jobs={jobs}
              zones={zones}
              onTriggerJob={handleTriggerJob}
              onCancelJob={handleCancelJob}
              isTriggering={isTriggeringJob}
            />
          )}

          {currentView === 'exports' && (
            <ExcelExportsView zones={zones} exportStatus={exportStatus} />
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
