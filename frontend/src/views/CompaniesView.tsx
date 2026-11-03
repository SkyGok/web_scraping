import React, { useState } from 'react';
import {
  Building2,
  Search,
  Globe,
  Phone,
  Mail,
  MapPin,
  ExternalLink,
  Contact2,
  Filter,
} from 'lucide-react';
import { Company, IndustrialZone } from '../types';

interface CompaniesViewProps {
  companies: Company[];
  zones: IndustrialZone[];
  onSelectCompany?: (company: Company) => void;
}

export const CompaniesView: React.FC<CompaniesViewProps> = ({
  companies,
  zones,
}) => {
  const [search, setSearch] = useState('');
  const [selectedZone, setSelectedZone] = useState<string>('');
  const [contactFilter, setContactFilter] = useState<'all' | 'with' | 'without'>('all');

  const filteredCompanies = companies.filter((c) => {
    const matchesSearch =
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      (c.sector && c.sector.toLowerCase().includes(search.toLowerCase())) ||
      (c.description && c.description.toLowerCase().includes(search.toLowerCase()));

    const matchesZone = !selectedZone || c.zone_id.toString() === selectedZone;

    let matchesContact = true;
    if (contactFilter === 'with') matchesContact = c.contact_count > 0;
    if (contactFilter === 'without') matchesContact = c.contact_count === 0;

    return matchesSearch && matchesZone && matchesContact;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Building2 className="w-5 h-5 text-cyan-400" />
          Manufacturing Companies Directory
        </h2>
        <p className="text-xs text-slate-400">
          Cataloged industrial companies, corporate websites, tax numbers, and verified business contacts.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-center gap-3 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search company by name, sector, or keywords..."
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"
          />
        </div>

        <select
          value={selectedZone}
          onChange={(e) => setSelectedZone(e.target.value)}
          className="w-full md:w-60 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 transition"
        >
          <option value="">All Industrial Zones</option>
          {zones.map((z) => (
            <option key={z.id} value={z.id}>
              {z.name}
            </option>
          ))}
        </select>

        <select
          value={contactFilter}
          onChange={(e) => setContactFilter(e.target.value as any)}
          className="w-full md:w-44 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 transition"
        >
          <option value="all">All Companies</option>
          <option value="with">With Contacts Only</option>
          <option value="without">Without Contacts</option>
        </select>
      </div>

      {/* Companies Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-800/80 text-slate-400 uppercase text-[10px] font-semibold tracking-wider">
              <tr>
                <th className="py-3 px-4">Company Name</th>
                <th className="py-3 px-4">Industrial Zone</th>
                <th className="py-3 px-4">Sector</th>
                <th className="py-3 px-4">Primary Contact</th>
                <th className="py-3 px-4">Website</th>
                <th className="py-3 px-4 text-center">Contacts</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {filteredCompanies.map((company) => (
                <tr key={company.id} className="hover:bg-slate-800/40 transition">
                  <td className="py-3 px-4">
                    <div className="font-semibold text-slate-100">{company.name}</div>
                    {company.tax_number && (
                      <div className="text-[10px] font-mono text-slate-500">
                        VKN: {company.tax_number}
                      </div>
                    )}
                  </td>
                  <td className="py-3 px-4 text-slate-300">
                    <span className="px-2 py-0.5 rounded text-[11px] bg-slate-800 border border-slate-700">
                      {company.zone_name || 'Bursa OSB'}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-950/60 text-cyan-300 border border-cyan-800/40">
                      {company.sector || 'Genel İmalat'}
                    </span>
                  </td>
                  <td className="py-3 px-4 space-y-1">
                    {company.phone && (
                      <div className="flex items-center gap-1.5 text-slate-300 font-mono text-[11px]">
                        <Phone className="w-3 h-3 text-slate-500" />
                        <span>{company.phone}</span>
                      </div>
                    )}
                    {company.email && (
                      <div className="flex items-center gap-1.5 text-slate-300 font-mono text-[11px]">
                        <Mail className="w-3 h-3 text-slate-500" />
                        <span className="truncate max-w-[180px]">{company.email}</span>
                      </div>
                    )}
                    {!company.phone && !company.email && (
                      <span className="text-slate-600 italic text-[11px]">Pending discovery</span>
                    )}
                  </td>
                  <td className="py-3 px-4">
                    {company.primary_website ? (
                      <a
                        href={company.primary_website}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-blue-400 hover:text-blue-300 transition text-[11px] underline decoration-blue-900"
                      >
                        <Globe className="w-3 h-3" />
                        <span className="truncate max-w-[140px]">
                          {company.primary_website.replace(/^https?:\/\//, '')}
                        </span>
                        <ExternalLink className="w-2.5 h-2.5" />
                      </a>
                    ) : (
                      <span className="text-slate-600 text-[11px]">No website</span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span
                      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-mono font-medium ${
                        company.contact_count > 0
                          ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/50'
                          : 'bg-slate-800 text-slate-500 border border-slate-700'
                      }`}
                    >
                      <Contact2 className="w-3 h-3" />
                      {company.contact_count}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredCompanies.length === 0 && (
          <div className="text-center py-12 space-y-2">
            <Building2 className="w-8 h-8 text-slate-600 mx-auto" />
            <h4 className="text-sm font-semibold text-slate-300">No companies found</h4>
            <p className="text-xs text-slate-500">
              {companies.length === 0
                ? "Start a scraping discovery job on an OSB directory to populate company records."
                : "Try broadening your search or filter settings."}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
