import React, { useState } from 'react';
import {
  Contact2,
  Search,
  Mail,
  Phone,
  User,
  ShieldCheck,
  CheckCircle,
  Copy,
  ExternalLink,
  Check,
} from 'lucide-react';
import { Contact } from '../types';

interface ContactsViewProps {
  contacts: Contact[];
  onToggleVerify: (contactId: number) => void;
}

export const ContactsView: React.FC<ContactsViewProps> = ({
  contacts,
  onToggleVerify,
}) => {
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [verifiedFilter, setVerifiedFilter] = useState<'all' | 'verified' | 'unverified'>('all');
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const contactTypes = Array.from(new Set(contacts.map((c) => c.contact_type)));

  const handleCopy = (id: number, val: string) => {
    navigator.clipboard.writeText(val);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 1500);
  };

  const filteredContacts = contacts.filter((c) => {
    const matchesSearch =
      c.value.toLowerCase().includes(search.toLowerCase()) ||
      (c.company_name && c.company_name.toLowerCase().includes(search.toLowerCase())) ||
      (c.person_name && c.person_name.toLowerCase().includes(search.toLowerCase())) ||
      (c.department && c.department.toLowerCase().includes(search.toLowerCase()));

    const matchesType = !typeFilter || c.contact_type === typeFilter;

    let matchesVerified = true;
    if (verifiedFilter === 'verified') matchesVerified = c.is_verified;
    if (verifiedFilter === 'unverified') matchesVerified = !c.is_verified;

    return matchesSearch && matchesType && matchesVerified;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Contact2 className="w-5 h-5 text-emerald-400" />
          Public Business Contacts Directory
        </h2>
        <p className="text-xs text-slate-400">
          Professional and business contacts extracted exclusively from publicly disclosed pages with source provenance.
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
            placeholder="Search email, phone, executive name, or company..."
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"
          />
        </div>

        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="w-full md:w-48 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 transition"
        >
          <option value="">All Contact Types</option>
          {contactTypes.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>

        <select
          value={verifiedFilter}
          onChange={(e) => setVerifiedFilter(e.target.value as any)}
          className="w-full md:w-44 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 transition"
        >
          <option value="all">All Statuses</option>
          <option value="verified">Verified Only</option>
          <option value="unverified">Unverified Only</option>
        </select>
      </div>

      {/* Contacts Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-800/80 text-slate-400 uppercase text-[10px] font-semibold tracking-wider">
              <tr>
                <th className="py-3 px-4">Contact Value</th>
                <th className="py-3 px-4">Type / Label</th>
                <th className="py-3 px-4">Company & Zone</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4">Provenance</th>
                <th className="py-3 px-4 text-center">Verify</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {filteredContacts.map((c) => {
                const isEmail = c.contact_type.includes('email');
                const isPhone = c.contact_type.includes('phone') || c.contact_type.includes('fax');

                return (
                  <tr key={c.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        {isEmail && <Mail className="w-3.5 h-3.5 text-blue-400 shrink-0" />}
                        {isPhone && <Phone className="w-3.5 h-3.5 text-emerald-400 shrink-0" />}
                        {!isEmail && !isPhone && <User className="w-3.5 h-3.5 text-purple-400 shrink-0" />}
                        <span className="font-mono text-slate-100 font-semibold">{c.value}</span>
                        <button
                          onClick={() => handleCopy(c.id, c.value)}
                          className="text-slate-500 hover:text-slate-200 transition"
                          title="Copy to clipboard"
                        >
                          {copiedId === c.id ? (
                            <Check className="w-3 h-3 text-emerald-400" />
                          ) : (
                            <Copy className="w-3 h-3" />
                          )}
                        </button>
                      </div>
                      {c.person_name && (
                        <div className="text-[11px] text-slate-400 mt-0.5">
                          {c.person_name} {c.department && `• ${c.department}`}
                        </div>
                      )}
                    </td>

                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300 border border-slate-700">
                        {c.contact_type}
                      </span>
                      {c.label && <div className="text-[10px] text-slate-400 mt-0.5">{c.label}</div>}
                    </td>

                    <td className="py-3 px-4">
                      <div className="font-medium text-slate-200">{c.company_name || 'Bursa Manufacturer'}</div>
                      <div className="text-[10px] text-slate-500">{c.zone_name || 'Bursa OSB'}</div>
                    </td>

                    <td className="py-3 px-4 font-mono">
                      <div className="flex items-center gap-1.5">
                        <div className="w-12 bg-slate-800 rounded-full h-1.5 overflow-hidden">
                          <div
                            className="bg-emerald-500 h-1.5 rounded-full"
                            style={{ width: `${Math.round(c.confidence_score * 100)}%` }}
                          />
                        </div>
                        <span className="text-[11px] text-slate-300">
                          {Math.round(c.confidence_score * 100)}%
                        </span>
                      </div>
                    </td>

                    <td className="py-3 px-4 text-xs">
                      {c.source_url ? (
                        <a
                          href={c.source_url}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 text-slate-400 hover:text-blue-400 text-[11px] truncate max-w-[150px]"
                          title={c.source_url}
                        >
                          <span className="truncate">{c.source_url.replace(/^https?:\/\//, '')}</span>
                          <ExternalLink className="w-3 h-3 shrink-0" />
                        </a>
                      ) : (
                        <span className="text-slate-600 text-[11px]">OSB Portal</span>
                      )}
                      <div className="text-[10px] text-slate-500 font-mono">
                        {new Date(c.retrieved_at).toLocaleDateString()}
                      </div>
                    </td>

                    <td className="py-3 px-4 text-center">
                      <button
                        onClick={() => onToggleVerify(c.id)}
                        className={`inline-flex items-center gap-1 px-2.5 py-1 rounded text-[11px] font-medium transition ${
                          c.is_verified
                            ? 'bg-emerald-950 text-emerald-300 border border-emerald-800/60 hover:bg-emerald-900'
                            : 'bg-slate-800 text-slate-400 border border-slate-700 hover:bg-slate-700 hover:text-slate-200'
                        }`}
                      >
                        <ShieldCheck className={`w-3.5 h-3.5 ${c.is_verified ? 'text-emerald-400' : 'text-slate-500'}`} />
                        {c.is_verified ? 'Verified' : 'Verify'}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {filteredContacts.length === 0 && (
          <div className="text-center py-12 space-y-2">
            <Contact2 className="w-8 h-8 text-slate-600 mx-auto" />
            <h4 className="text-sm font-semibold text-slate-300">No contacts found</h4>
            <p className="text-xs text-slate-500">
              {contacts.length === 0
                ? "Scraping jobs will extract public emails, phone numbers, and executive contacts from verified OSB portals."
                : "Try adjusting your search criteria."}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
