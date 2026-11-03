import React from 'react';
import {
  Factory,
  Building2,
  Contact2,
  Globe,
  Clock,
  ExternalLink,
  Play,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { StatCard } from '../components/StatCard';
import { OverviewResponse, ViewType } from '../types';

interface OverviewViewProps {
  data: OverviewResponse | null;
  onNavigate: (view: ViewType) => void;
  onStartJob: (zoneId: number, zoneName: string) => void;
}

export const OverviewView: React.FC<OverviewViewProps> = ({
  data,
  onNavigate,
  onStartJob,
}) => {
  const m = data?.metrics;

  return (
    <div className="space-y-6">
      {/* Top Banner / Mission Statement */}
      <div className="bg-gradient-to-r from-blue-950/40 via-slate-900 to-slate-900 border border-blue-900/40 rounded-xl p-5 flex items-center justify-between">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
              PHASE 1 OPERATIONAL
            </span>
            <h2 className="text-lg font-bold text-white">Bursa Industrial Intelligence Hub</h2>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl">
            Discovering Bursa Organized Industrial Zones (OSBs), cataloging manufacturing companies,
            extracting publicly disclosed business contacts with full provenance, and generating multi-sheet workbooks.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => onNavigate('zones')}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-md shadow-blue-600/20 transition"
          >
            Explore OSBs <ArrowRight className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => onNavigate('exports')}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition"
          >
            Export .xlsx
          </button>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          title="Industrial Zones"
          value={m?.total_zones ?? 0}
          subtitle="Bursa OSBs registered"
          icon={Factory}
          color="blue"
          badge="Bursa Target"
        />
        <StatCard
          title="Companies"
          value={m?.total_companies ?? 0}
          subtitle="Unique manufacturers discovered"
          icon={Building2}
          color="cyan"
          badge="Normalized"
        />
        <StatCard
          title="Business Contacts"
          value={m?.total_contacts ?? 0}
          subtitle={`${m?.verified_contacts_count ?? 0} verified with source URL`}
          icon={Contact2}
          color="emerald"
          badge="KVKK Public"
        />
        <StatCard
          title="Website Registry"
          value={m?.total_websites ?? 0}
          subtitle="Monitored OSB & corporate domains"
          icon={Globe}
          color="purple"
          badge="Robots Compliant"
        />
        <StatCard
          title="Scraping Jobs"
          value={m?.active_jobs ?? 0}
          subtitle={`${m?.completed_jobs ?? 0} finished, ${m?.failed_jobs ?? 0} failed`}
          icon={Clock}
          color={m?.active_jobs && m.active_jobs > 0 ? 'amber' : 'blue'}
          badge={m?.active_jobs && m.active_jobs > 0 ? 'RUNNING' : 'IDLE'}
        />
      </div>

      {/* Two-Column Layout: OSB Registry Summary & Recent Scraping Jobs */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* OSB Registry Table (2 cols) */}
        <div className="lg:col-span-2 bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-sm text-slate-100 flex items-center gap-2">
                <Factory className="w-4 h-4 text-blue-400" />
                Bursa Organized Industrial Zones (OSBs)
              </h3>
              <p className="text-xs text-slate-400">Official zone directories and status</p>
            </div>
            <button
              onClick={() => onNavigate('zones')}
              className="text-xs text-blue-400 hover:text-blue-300 font-medium flex items-center gap-1"
            >
              View All ({data?.osb_summaries.length ?? 0}) <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-800/60 text-slate-400 uppercase text-[10px] font-semibold tracking-wider">
                <tr>
                  <th className="py-2.5 px-3 rounded-l">Zone Name</th>
                  <th className="py-2.5 px-3">District</th>
                  <th className="py-2.5 px-3">Companies</th>
                  <th className="py-2.5 px-3">Contacts</th>
                  <th className="py-2.5 px-3">Status</th>
                  <th className="py-2.5 px-3 text-right rounded-r">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300 font-sans">
                {data?.osb_summaries.slice(0, 7).map((osb) => (
                  <tr key={osb.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-2.5 px-3 font-medium text-slate-100">
                      {osb.name}
                    </td>
                    <td className="py-2.5 px-3 text-slate-400">{osb.district || 'Bursa'}</td>
                    <td className="py-2.5 px-3 font-mono">{osb.company_count}</td>
                    <td className="py-2.5 px-3 font-mono text-emerald-400">{osb.contact_count}</td>
                    <td className="py-2.5 px-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-blue-900/30 text-blue-400 border border-blue-800/40">
                        {osb.website_status}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-right">
                      <button
                        onClick={() => onStartJob(osb.id, osb.name)}
                        className="inline-flex items-center gap-1 px-2 py-1 rounded bg-slate-800 hover:bg-blue-600 hover:text-white text-[11px] font-medium text-slate-300 transition border border-slate-700"
                        title="Discover Companies from this OSB"
                      >
                        <Play className="w-3 h-3 text-blue-400" />
                        Scrape
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent Scraping Jobs & Activity (1 col) */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-sm text-slate-100 flex items-center gap-2">
                <Clock className="w-4 h-4 text-amber-400" />
                Scraping Activity
              </h3>
              <p className="text-xs text-slate-400">Queue & worker execution logs</p>
            </div>
            <button
              onClick={() => onNavigate('jobs')}
              className="text-xs text-blue-400 hover:text-blue-300 font-medium flex items-center gap-1"
            >
              History <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="space-y-2.5">
            {(!data?.recent_jobs || data.recent_jobs.length === 0) ? (
              <div className="p-6 text-center text-slate-500 text-xs border border-dashed border-slate-800 rounded-lg">
                No active or previous scraping jobs found. Ready to initiate initial OSB directory discovery.
              </div>
            ) : (
              data.recent_jobs.slice(0, 5).map((job) => (
                <div
                  key={job.id}
                  className="p-3 rounded-lg bg-slate-800/40 border border-slate-800 hover:border-slate-700 transition flex items-center justify-between text-xs"
                >
                  <div className="space-y-0.5">
                    <div className="font-medium text-slate-200">
                      {job.zone_name || `Job #${job.id}`}
                    </div>
                    <div className="text-[11px] text-slate-400 font-mono">
                      {job.job_type} • mode: {job.crawl_mode}
                    </div>
                  </div>
                  <div className="text-right">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-mono font-medium ${
                        job.status === 'completed'
                          ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/60'
                          : job.status === 'running'
                          ? 'bg-amber-950 text-amber-400 border border-amber-800/60 animate-pulse'
                          : 'bg-slate-800 text-slate-400 border border-slate-700'
                      }`}
                    >
                      {job.status}
                    </span>
                    <div className="text-[10px] text-slate-500 mt-1 font-mono">
                      {job.success_count}/{job.total_targets || 0} items
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="p-3 bg-slate-950/60 rounded-lg border border-slate-800/80 text-[11px] text-slate-400 space-y-1">
            <div className="flex items-center gap-1.5 font-medium text-slate-300">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              Scraping Ethics & Protocol
            </div>
            <p className="text-[10px] leading-relaxed text-slate-500">
              Only publicly listed corporate directories are accessed with adaptive backoff rate limiting.
              Personal phone numbers and private addresses are excluded.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
