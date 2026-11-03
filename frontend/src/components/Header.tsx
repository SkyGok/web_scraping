import React from 'react';
import { Database, RefreshCw, Layers, ShieldCheck } from 'lucide-react';

interface HeaderProps {
  onRefresh: () => void;
  isRefreshing: boolean;
  onSeed: () => void;
  isSeeding: boolean;
  apiHealthy: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  onRefresh,
  isRefreshing,
  onSeed,
  isSeeding,
  apiHealthy,
}) => {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/90 backdrop-blur px-6 flex items-center justify-between sticky top-0 z-20">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Layers className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-slate-100 tracking-wide text-base">INDUSTRIAL INTELLIGENCE</h1>
            <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-blue-900/60 text-blue-300 border border-blue-700/50">
              Bursa Pilot
            </span>
          </div>
          <p className="text-xs text-slate-400">Türkiye Organized Industrial Zones & Business Intelligence</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Backend health status pill */}
        <div className="flex items-center gap-2 px-2.5 py-1 rounded-md bg-slate-800/80 border border-slate-700 text-xs text-slate-300">
          <span className={`w-2 h-2 rounded-full ${apiHealthy ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
          <span className="font-mono">{apiHealthy ? 'API ONLINE' : 'STANDALONE / SYNCING'}</span>
        </div>

        {/* Seed button */}
        <button
          onClick={onSeed}
          disabled={isSeeding}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 border border-slate-700 transition disabled:opacity-50"
          title="Seed initial Bursa Industrial Zones into Database"
        >
          <Database className={`w-3.5 h-3.5 ${isSeeding ? 'animate-spin' : 'text-blue-400'}`} />
          {isSeeding ? 'Seeding OSBs...' : 'Seed Bursa OSBs'}
        </button>

        {/* Refresh button */}
        <button
          onClick={onRefresh}
          disabled={isRefreshing}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-500 text-xs font-medium text-white shadow-sm shadow-blue-500/30 transition disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin' : ''}`} />
          Refresh
        </button>

        <div className="h-4 w-px bg-slate-800 mx-1" />

        <div className="flex items-center gap-1.5 text-xs text-slate-400" title="KVKK / Non-intrusive scraping compliant">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span className="text-[11px] font-mono text-slate-400">KVKK Compliant</span>
        </div>
      </div>
    </header>
  );
};
