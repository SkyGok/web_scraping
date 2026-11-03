import React, { useState } from 'react';
import {
  Factory,
  Globe,
  ExternalLink,
  Search,
  Play,
  Building2,
  Contact2,
  Database,
  CheckCircle2,
} from 'lucide-react';
import { IndustrialZone } from '../types';

interface IndustrialZonesViewProps {
  zones: IndustrialZone[];
  onSeed: () => void;
  isSeeding: boolean;
  onStartJob: (zoneId: number, zoneName: string) => void;
}

export const IndustrialZonesView: React.FC<IndustrialZonesViewProps> = ({
  zones,
  onSeed,
  isSeeding,
  onStartJob,
}) => {
  const [search, setSearch] = useState('');
  const [districtFilter, setDistrictFilter] = useState('');

  const districts = Array.from(
    new Set(zones.map((z) => z.district).filter(Boolean))
  ) as string[];

  const filteredZones = zones.filter((zone) => {
    const matchesSearch =
      zone.name.toLowerCase().includes(search.toLowerCase()) ||
      (zone.description && zone.description.toLowerCase().includes(search.toLowerCase())) ||
      (zone.district && zone.district.toLowerCase().includes(search.toLowerCase()));

    const matchesDistrict = !districtFilter || zone.district === districtFilter;
    return matchesSearch && matchesDistrict;
  });

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Factory className="w-5 h-5 text-blue-400" />
            Organized Industrial Zones (OSB) Registry
          </h2>
          <p className="text-xs text-slate-400">
            Catalog of industrial zones in Bursa with official directories, member registries, and portal endpoints.
          </p>
        </div>

        <button
          onClick={onSeed}
          disabled={isSeeding}
          className="self-start md:self-auto flex items-center gap-2 px-3.5 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white shadow-md shadow-blue-600/30 transition disabled:opacity-50"
        >
          <Database className={`w-3.5 h-3.5 ${isSeeding ? 'animate-spin' : ''}`} />
          {isSeeding ? 'Seeding Bursa OSBs...' : 'Seed Bursa OSBs'}
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-center gap-3 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by OSB name, district, or sector description..."
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"
          />
        </div>

        <select
          value={districtFilter}
          onChange={(e) => setDistrictFilter(e.target.value)}
          className="w-full md:w-56 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 transition"
        >
          <option value="">All Districts ({zones.length})</option>
          {districts.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
      </div>

      {/* Zone Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredZones.map((zone) => (
          <div
            key={zone.id}
            className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 flex flex-col justify-between hover:border-slate-700 transition group"
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-2">
                <div>
                  <span className="text-[10px] font-mono uppercase tracking-wider text-blue-400 font-semibold px-2 py-0.5 rounded bg-blue-950 border border-blue-900/50">
                    {zone.district || 'Bursa'}
                  </span>
                  <h3 className="font-bold text-sm text-slate-100 mt-2 group-hover:text-blue-300 transition">
                    {zone.name}
                  </h3>
                </div>
                <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0">
                  <Factory className="w-4 h-4 text-slate-400 group-hover:text-blue-400 transition" />
                </div>
              </div>

              <p className="text-xs text-slate-400 line-clamp-3 leading-relaxed">
                {zone.description || 'Organized industrial zone located in Bursa.'}
              </p>

              {zone.official_website && (
                <div className="flex items-center gap-1.5 text-xs text-slate-400">
                  <Globe className="w-3.5 h-3.5 text-slate-500" />
                  <a
                    href={zone.official_website}
                    target="_blank"
                    rel="noreferrer"
                    className="hover:text-blue-400 transition truncate underline decoration-slate-700"
                  >
                    {zone.official_website.replace(/^https?:\/\//, '')}
                  </a>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </div>
              )}
            </div>

            <div className="mt-5 pt-4 border-t border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-4 text-xs font-mono">
                <div className="flex items-center gap-1 text-slate-300" title="Companies Discovered">
                  <Building2 className="w-3.5 h-3.5 text-slate-500" />
                  <span>{zone.company_count}</span>
                </div>
                <div className="flex items-center gap-1 text-emerald-400" title="Contacts Extracted">
                  <Contact2 className="w-3.5 h-3.5 text-emerald-600" />
                  <span>{zone.contact_count}</span>
                </div>
              </div>

              <button
                onClick={() => onStartJob(zone.id, zone.name)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-500 text-xs font-medium text-white shadow-sm shadow-blue-600/30 transition"
              >
                <Play className="w-3 h-3 fill-current" />
                Start Discovery
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredZones.length === 0 && (
        <div className="text-center py-12 border border-dashed border-slate-800 rounded-xl space-y-2">
          <Factory className="w-8 h-8 text-slate-600 mx-auto" />
          <h4 className="text-sm font-semibold text-slate-300">No industrial zones match your filters</h4>
          <p className="text-xs text-slate-500">Try adjusting your search criteria or click 'Seed Bursa OSBs' above.</p>
        </div>
      )}
    </div>
  );
};
