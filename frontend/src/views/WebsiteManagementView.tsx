import React, { useState } from 'react';
import {
  Globe,
  Search,
  RotateCcw,
  Shield,
  ExternalLink,
  Plus,
  Play,
  X,
  CheckCircle2,
} from 'lucide-react';
import { Website, IndustrialZone } from '../types';

interface WebsiteManagementViewProps {
  websites: Website[];
  zones: IndustrialZone[];
  onUpdateMode: (websiteId: number, mode: 'new_only' | 'retry_failed' | 'refresh_all') => void;
  onRetry: (websiteId: number) => void;
  onAddWebsite: (payload: { base_url: string; zone_id?: number; crawl_mode?: string }) => void;
  onScrapeWebsite: (websiteId: number) => void;
  isAdding?: boolean;
}

export const WebsiteManagementView: React.FC<WebsiteManagementViewProps> = ({
  websites,
  zones,
  onUpdateMode,
  onRetry,
  onAddWebsite,
  onScrapeWebsite,
  isAdding = false,
}) => {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [modeFilter, setModeFilter] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Form state
  const [newUrl, setNewUrl] = useState('');
  const [newZoneId, setNewZoneId] = useState<string>('');
  const [newCrawlMode, setNewCrawlMode] = useState<'new_only' | 'retry_failed' | 'refresh_all'>('new_only');

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUrl.trim()) return;
    onAddWebsite({
      base_url: newUrl.trim(),
      zone_id: newZoneId ? parseInt(newZoneId, 10) : undefined,
      crawl_mode: newCrawlMode,
    });
    setNewUrl('');
    setIsModalOpen(false);
  };

  const filteredWebsites = websites.filter((w) => {
    const matchesSearch =
      w.domain.toLowerCase().includes(search.toLowerCase()) ||
      w.base_url.toLowerCase().includes(search.toLowerCase()) ||
      (w.zone_name && w.zone_name.toLowerCase().includes(search.toLowerCase()));

    const matchesStatus = !statusFilter || w.status === statusFilter;
    const matchesMode = !modeFilter || w.crawl_mode === modeFilter;

    return matchesSearch && matchesStatus && matchesMode;
  });

  return (
    <div className="space-y-6">
      {/* Header with Register Button */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Globe className="w-5 h-5 text-purple-400" />
            Website Registry & Crawl Policies
          </h2>
          <p className="text-xs text-slate-400">
            Persistent registry tracking visited domains, HTTP status, crawl modes (New Only, Retry Failed, Refresh),
            and robots.txt compliance.
          </p>
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          className="self-start md:self-auto flex items-center gap-2 px-3.5 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-md shadow-blue-600/30 transition"
        >
          <Plus className="w-4 h-4" />
          Add Website Link
        </button>
      </div>

      {/* Crawl Mode Legend Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900/70 border border-slate-800 rounded-lg p-3.5 space-y-1">
          <div className="flex items-center gap-2 text-xs font-semibold text-blue-400">
            <span className="w-2 h-2 rounded-full bg-blue-400" />
            New Websites Only
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Only visits newly discovered OSB directories or company portals that haven't been indexed.
          </p>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 rounded-lg p-3.5 space-y-1">
          <div className="flex items-center gap-2 text-xs font-semibold text-amber-400">
            <span className="w-2 h-2 rounded-full bg-amber-400" />
            Retry Failed
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Re-queues websites that experienced network timeouts, 5xx server errors, or transient rate limits.
          </p>
        </div>

        <div className="bg-slate-900/70 border border-slate-800 rounded-lg p-3.5 space-y-1">
          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            Refresh Existing Data
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Recrawls active member pages to capture updated tax numbers, address relocations, or new emails.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-center gap-3 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search domain or URL..."
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"
          />
        </div>

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="w-full md:w-48 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 transition"
        >
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="queued">Queued</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
        </select>

        <select
          value={modeFilter}
          onChange={(e) => setModeFilter(e.target.value)}
          className="w-full md:w-52 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 transition"
        >
          <option value="">All Crawl Modes</option>
          <option value="new_only">New Only</option>
          <option value="retry_failed">Retry Failed</option>
          <option value="refresh_all">Refresh All</option>
        </select>
      </div>

      {/* Websites Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-800/80 text-slate-400 uppercase text-[10px] font-semibold tracking-wider">
              <tr>
                <th className="py-3 px-4">Domain & Portal</th>
                <th className="py-3 px-4">Associated Entity</th>
                <th className="py-3 px-4">Crawl Status</th>
                <th className="py-3 px-4">Crawl Mode</th>
                <th className="py-3 px-4">Robots / Delay</th>
                <th className="py-3 px-4">Last Visited</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {filteredWebsites.map((w) => (
                <tr key={w.id} className="hover:bg-slate-800/40 transition">
                  <td className="py-3 px-4">
                    <div className="font-semibold text-slate-100 font-mono flex items-center gap-1.5">
                      <Globe className="w-3.5 h-3.5 text-slate-500" />
                      {w.domain}
                      <a
                        href={w.base_url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-slate-500 hover:text-blue-400 transition"
                      >
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                    {w.error_message && (
                      <div className="text-[10px] text-rose-400 mt-1 max-w-xs truncate" title={w.error_message}>
                        Error: {w.error_message}
                      </div>
                    )}
                  </td>

                  <td className="py-3 px-4 text-slate-300">
                    <div>{w.zone_name || w.company_name || 'Bursa OSB Member'}</div>
                    <span className="text-[10px] font-mono text-slate-500">
                      {w.zone_id ? 'OSB Portal' : 'Corporate Site'}
                    </span>
                  </td>

                  <td className="py-3 px-4">
                    <span
                      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono font-medium ${
                        w.status === 'completed'
                          ? 'bg-emerald-950 text-emerald-300 border border-emerald-800/60'
                          : w.status === 'failed'
                          ? 'bg-rose-950 text-rose-300 border border-rose-800/60'
                          : w.status === 'in_progress'
                          ? 'bg-amber-950 text-amber-300 border border-amber-800/60 animate-pulse'
                          : 'bg-slate-800 text-slate-400 border border-slate-700'
                      }`}
                    >
                      {w.status}
                    </span>
                    {w.retry_count > 0 && (
                      <span className="text-[10px] font-mono text-slate-500 ml-1.5">
                        (retries: {w.retry_count})
                      </span>
                    )}
                  </td>

                  <td className="py-3 px-4">
                    <select
                      value={w.crawl_mode}
                      onChange={(e) => onUpdateMode(w.id, e.target.value as any)}
                      className="bg-slate-950 border border-slate-800 rounded px-2 py-1 text-[11px] text-slate-200 focus:outline-none focus:border-blue-500 font-mono"
                    >
                      <option value="new_only">new_only</option>
                      <option value="retry_failed">retry_failed</option>
                      <option value="refresh_all">refresh_all</option>
                    </select>
                  </td>

                  <td className="py-3 px-4 font-mono text-[11px]">
                    <div className="flex items-center gap-1 text-slate-300">
                      <Shield className="w-3 h-3 text-emerald-400" />
                      <span>{w.robots_allowed ? 'Allowed' : 'Disallowed'}</span>
                    </div>
                    <div className="text-[10px] text-slate-500">Delay: {w.crawl_delay}s</div>
                  </td>

                  <td className="py-3 px-4 font-mono text-[11px] text-slate-400">
                    {w.last_visited_at ? (
                      <div>{new Date(w.last_visited_at).toLocaleDateString()}</div>
                    ) : (
                      <span className="text-slate-600">Never</span>
                    )}
                  </td>

                  <td className="py-3 px-4 text-right space-x-1.5">
                    <button
                      onClick={() => onScrapeWebsite(w.id)}
                      className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-blue-600/20 hover:bg-blue-600 hover:text-white text-blue-300 text-[11px] font-medium transition border border-blue-500/30"
                      title="Run discovery scrape on this website now"
                    >
                      <Play className="w-3 h-3 fill-current" />
                      Scrape Now
                    </button>

                    {w.status === 'failed' && (
                      <button
                        onClick={() => onRetry(w.id)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 text-[11px] font-medium transition border border-amber-500/30"
                      >
                        <RotateCcw className="w-3 h-3" />
                        Retry
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Website Modal Dialog */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl max-w-md w-full p-6 space-y-4 shadow-2xl animate-in fade-in duration-150">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Globe className="w-4 h-4 text-blue-400" />
                Register Website for Discovery
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-white transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-400">
              Enter any OSB portal or company website URL. The engine will check robots.txt, catalog pages, discover companies, and extract public business contacts.
            </p>

            <form onSubmit={handleFormSubmit} className="space-y-3 pt-2">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Website URL / Link *
                </label>
                <input
                  type="text"
                  required
                  placeholder="https://bosb.org.tr or https://example-company.com"
                  value={newUrl}
                  onChange={(e) => setNewUrl(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Associated Industrial Zone (Optional)
                </label>
                <select
                  value={newZoneId}
                  onChange={(e) => setNewZoneId(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-mono"
                >
                  <option value="">None / Independent Manufacturer</option>
                  {zones.map((z) => (
                    <option key={z.id} value={z.id}>
                      {z.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Crawl Mode
                </label>
                <select
                  value={newCrawlMode}
                  onChange={(e) => setNewCrawlMode(e.target.value as any)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-mono"
                >
                  <option value="new_only">New Websites Only</option>
                  <option value="retry_failed">Retry Failed</option>
                  <option value="refresh_all">Refresh Existing Data</option>
                </select>
              </div>

              <div className="pt-3 flex items-center justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isAdding || !newUrl.trim()}
                  className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-md shadow-blue-600/30 transition disabled:opacity-50"
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  Register & Start Discovery
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
