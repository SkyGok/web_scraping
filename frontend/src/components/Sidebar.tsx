import React from 'react';
import {
  LayoutDashboard,
  Factory,
  Building2,
  Contact2,
  Globe,
  Clock,
  FileSpreadsheet,
} from 'lucide-react';
import { ViewType } from '../types';

interface SidebarProps {
  currentView: ViewType;
  onViewChange: (view: ViewType) => void;
  counts?: {
    zones: number;
    companies: number;
    contacts: number;
    websites: number;
    activeJobs: number;
  };
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentView,
  onViewChange,
  counts,
}) => {
  const navItems = [
    {
      id: 'overview' as ViewType,
      label: 'Overview',
      icon: LayoutDashboard,
      badge: null,
    },
    {
      id: 'zones' as ViewType,
      label: 'Industrial Zones',
      icon: Factory,
      badge: counts?.zones ? `${counts.zones}` : null,
    },
    {
      id: 'companies' as ViewType,
      label: 'Companies',
      icon: Building2,
      badge: counts?.companies ? `${counts.companies}` : null,
    },
    {
      id: 'contacts' as ViewType,
      label: 'Contacts',
      icon: Contact2,
      badge: counts?.contacts ? `${counts.contacts}` : null,
    },
    {
      id: 'websites' as ViewType,
      label: 'Website Registry',
      icon: Globe,
      badge: counts?.websites ? `${counts.websites}` : null,
    },
    {
      id: 'jobs' as ViewType,
      label: 'Scraping History',
      icon: Clock,
      badge: counts?.activeJobs && counts.activeJobs > 0 ? `${counts.activeJobs} active` : null,
      badgeColor: counts?.activeJobs && counts.activeJobs > 0 ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' : undefined,
    },
    {
      id: 'exports' as ViewType,
      label: 'Excel Exports',
      icon: FileSpreadsheet,
      badge: '.xlsx',
      badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
    },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/50 flex flex-col justify-between p-3 shrink-0">
      <div className="space-y-1">
        <div className="px-3 py-2 text-[11px] font-semibold tracking-wider uppercase text-slate-500">
          Platform Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onViewChange(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition ${
                isActive
                  ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <Icon className={`w-4 h-4 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[11px] px-1.5 py-0.5 rounded font-mono border ${
                    item.badgeColor || 'bg-slate-800 text-slate-300 border-slate-700'
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 text-xs space-y-1.5">
        <div className="flex items-center justify-between text-slate-400">
          <span>Target Region:</span>
          <span className="font-semibold text-slate-200">Bursa, Türkiye</span>
        </div>
        <div className="flex items-center justify-between text-slate-400">
          <span>Target Types:</span>
          <span className="font-mono text-slate-300">OSB Portals</span>
        </div>
        <div className="flex items-center justify-between text-slate-400">
          <span>Scraper Engine:</span>
          <span className="font-mono text-blue-400">HTTPX / BS4 / Playwright</span>
        </div>
      </div>
    </aside>
  );
};
