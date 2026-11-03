import React, { useState } from 'react';
import {
  Clock,
  Play,
  XCircle,
  CheckCircle2,
  AlertOctagon,
  RefreshCw,
  Search,
  ChevronDown,
  ChevronRight,
  Terminal,
} from 'lucide-react';
import { ScrapingJob, IndustrialZone } from '../types';

interface ScrapingHistoryViewProps {
  jobs: ScrapingJob[];
  zones: IndustrialZone[];
  onTriggerJob: (payload: {
    zone_id?: number;
    job_type: string;
    crawl_mode: string;
  }) => void;
  onCancelJob: (jobId: number) => void;
  isTriggering: boolean;
}

export const ScrapingHistoryView: React.FC<ScrapingHistoryViewProps> = ({
  jobs,
  zones,
  onTriggerJob,
  onCancelJob,
  isTriggering,
}) => {
  const [selectedZone, setSelectedZone] = useState<string>('');
  const [jobType, setJobType] = useState<string>('zone_discovery');
  const [crawlMode, setCrawlMode] = useState<string>('new_only');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [expandedJobId, setExpandedJobId] = useState<number | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onTriggerJob({
      zone_id: selectedZone ? parseInt(selectedZone, 10) : undefined,
      job_type: jobType,
      crawl_mode: crawlMode,
    });
  };

  const filteredJobs = jobs.filter((j) => {
    if (!statusFilter) return true;
    return j.status === statusFilter;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Clock className="w-5 h-5 text-amber-400" />
          Background Scraping Jobs & Queue Tracker
        </h2>
        <p className="text-xs text-slate-400">
          Monitor asynchronous worker pipelines executing OSB directory crawling, company discovery, and contact extraction.
        </p>
      </div>

      {/* Trigger New Job Card */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
          <Play className="w-4 h-4 text-blue-400" />
          Dispatch New Discovery Pipeline
        </h3>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-4 gap-3">
          <div>
            <label className="block text-[11px] font-medium text-slate-400 mb-1">Target Industrial Zone</label>
            <select
              value={selectedZone}
              onChange={(e) => setSelectedZone(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-mono"
            >
              <option value="">All Bursa Industrial Zones</option>
              {zones.map((z) => (
                <option key={z.id} value={z.id}>
                  {z.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-medium text-slate-400 mb-1">Pipeline Type</label>
            <select
              value={jobType}
              onChange={(e) => setJobType(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-mono"
            >
              <option value="zone_discovery">Zone & Portal Discovery</option>
              <option value="company_discovery">Company Discovery</option>
              <option value="contact_extraction">Contact Extraction</option>
              <option value="full_crawl">Full Deep Crawl</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-medium text-slate-400 mb-1">Crawl Mode</label>
            <select
              value={crawlMode}
              onChange={(e) => setCrawlMode(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-mono"
            >
              <option value="new_only">New Websites Only</option>
              <option value="retry_failed">Retry Failed Only</option>
              <option value="refresh_all">Refresh Existing Data</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              type="submit"
              disabled={isTriggering}
              className="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-md shadow-blue-600/30 transition disabled:opacity-50"
            >
              <Play className={`w-3.5 h-3.5 ${isTriggering ? 'animate-spin' : 'fill-current'}`} />
              {isTriggering ? 'Queueing Job...' : 'Queue Job in Redis'}
            </button>
          </div>
        </form>
      </div>

      {/* Filter Bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {['', 'running', 'completed', 'failed', 'pending'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition font-mono ${
                statusFilter === st
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              {st === '' ? 'all_statuses' : st}
            </button>
          ))}
        </div>
        <div className="text-xs text-slate-500 font-mono">
          Showing {filteredJobs.length} execution record(s)
        </div>
      </div>

      {/* Jobs List */}
      <div className="space-y-3">
        {filteredJobs.map((job) => {
          const isExpanded = expandedJobId === job.id;
          const progressPct =
            job.total_targets > 0
              ? Math.min(100, Math.round((job.processed_targets / job.total_targets) * 100))
              : job.status === 'completed'
              ? 100
              : 0;

          return (
            <div
              key={job.id}
              className="bg-slate-900/70 border border-slate-800 rounded-xl overflow-hidden hover:border-slate-700 transition"
            >
              <div className="p-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex items-start gap-3">
                  <button
                    onClick={() => setExpandedJobId(isExpanded ? null : job.id)}
                    className="p-1 rounded hover:bg-slate-800 text-slate-400 mt-0.5"
                  >
                    {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                  </button>

                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-slate-100 text-sm">
                        Job #{job.id}
                      </span>
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-blue-950 text-blue-300 border border-blue-900/60">
                        {job.job_type}
                      </span>
                      <span className="text-[11px] text-slate-400 font-mono">
                        mode: {job.crawl_mode}
                      </span>
                    </div>

                    <div className="text-xs text-slate-400">
                      Target: <span className="font-semibold text-slate-200">{job.zone_name || 'Bursa Industrial Ecosystem'}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  {/* Progress Bar */}
                  <div className="w-36 space-y-1 font-mono text-[11px]">
                    <div className="flex justify-between text-slate-400">
                      <span>Progress</span>
                      <span>{progressPct}%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-1.5 rounded-full ${
                          job.status === 'failed'
                            ? 'bg-rose-500'
                            : job.status === 'completed'
                            ? 'bg-emerald-500'
                            : 'bg-blue-500'
                        }`}
                        style={{ width: `${progressPct}%` }}
                      />
                    </div>
                  </div>

                  {/* Status Badge */}
                  <span
                    className={`px-2.5 py-1 rounded text-xs font-mono font-medium ${
                      job.status === 'completed'
                        ? 'bg-emerald-950 text-emerald-300 border border-emerald-800/60'
                        : job.status === 'running'
                        ? 'bg-amber-950 text-amber-300 border border-amber-800/60 animate-pulse'
                        : job.status === 'failed'
                        ? 'bg-rose-950 text-rose-300 border border-rose-800/60'
                        : 'bg-slate-800 text-slate-400 border border-slate-700'
                    }`}
                  >
                    {job.status}
                  </span>

                  {/* Actions */}
                  {job.status === 'running' && (
                    <button
                      onClick={() => onCancelJob(job.id)}
                      className="px-2.5 py-1 rounded bg-rose-950 hover:bg-rose-900 text-rose-300 border border-rose-800 text-xs font-medium transition"
                    >
                      Cancel
                    </button>
                  )}
                </div>
              </div>

              {/* Collapsible Logs Drawer */}
              {isExpanded && (
                <div className="bg-slate-950 p-4 border-t border-slate-800 space-y-2 text-xs font-mono">
                  <div className="flex items-center gap-2 text-slate-400">
                    <Terminal className="w-3.5 h-3.5 text-blue-400" />
                    <span>Job Execution Telemetry</span>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-slate-400 pt-1">
                    <div>Success Targets: <span className="text-emerald-400 font-bold">{job.success_count}</span></div>
                    <div>Error Count: <span className="text-rose-400 font-bold">{job.error_count}</span></div>
                    <div>Started: <span className="text-slate-300">{job.started_at ? new Date(job.started_at).toLocaleTimeString() : 'N/A'}</span></div>
                    <div>Finished: <span className="text-slate-300">{job.finished_at ? new Date(job.finished_at).toLocaleTimeString() : 'N/A'}</span></div>
                  </div>
                  {job.error_log && (
                    <div className="mt-3 p-3 rounded bg-rose-950/40 border border-rose-900/50 text-rose-300 whitespace-pre-wrap text-[11px]">
                      {job.error_log}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}

        {filteredJobs.length === 0 && (
          <div className="text-center py-12 border border-dashed border-slate-800 rounded-xl space-y-2">
            <Clock className="w-8 h-8 text-slate-600 mx-auto" />
            <h4 className="text-sm font-semibold text-slate-300">No jobs match criteria</h4>
            <p className="text-xs text-slate-500">Dispatch a new discovery job using the form above.</p>
          </div>
        )}
      </div>
    </div>
  );
};
