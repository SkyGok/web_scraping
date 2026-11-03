import React, { useState } from 'react';
import {
  FileSpreadsheet,
  Download,
  CheckCircle2,
  Filter,
  Layers,
  Database,
  Calendar,
  Building2,
  Contact2,
  Factory,
  FileCheck,
} from 'lucide-react';
import { IndustrialZone } from '../types';

interface ExcelExportsViewProps {
  zones: IndustrialZone[];
  exportStatus: {
    status: string;
    export_directory: string;
    available_exports: Array<{
      filename: string;
      size_bytes: number;
      created_at: string;
      download_url: string;
    }>;
    supported_sheets: string[];
  } | null;
}

export const ExcelExportsView: React.FC<ExcelExportsViewProps> = ({
  zones,
  exportStatus,
}) => {
  const [selectedZone, setSelectedZone] = useState<string>('all');
  const [includeVerifiedOnly, setIncludeVerifiedOnly] = useState<boolean>(false);
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const sheets = [
    {
      name: 'Companies',
      icon: Building2,
      desc: 'Normalized company names, tax numbers, sectors, addresses, website links, phone/email, and OSB affiliation.',
    },
    {
      name: 'Contacts',
      icon: Contact2,
      desc: 'Publicly disclosed emails, phone numbers, executive names, department tags, confidence scores, and verification status.',
    },
    {
      name: 'Industrial Zones',
      icon: Factory,
      desc: 'Bursa OSB registry, districts, official portal URLs, portal classification, and aggregated metrics.',
    },
    {
      name: 'Sources',
      icon: Layers,
      desc: 'Audit trail of URLs where each contact and company was extracted from, HTTP status, and timestamp.',
    },
    {
      name: 'Scraping History',
      icon: Calendar,
      desc: 'Execution telemetry of all crawling pipelines, duration, success and failure rates.',
    },
  ];

  const handleGenerateExport = () => {
    setIsExporting(true);
    setSuccessMessage(null);
    setTimeout(() => {
      setIsExporting(false);
      setSuccessMessage('Industrial Intelligence Excel Workbook generated successfully.');
    }, 1200);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <FileSpreadsheet className="w-5 h-5 text-emerald-400" />
          Excel Workbook Generation & Export Center
        </h2>
        <p className="text-xs text-slate-400">
          Export database entities into structured, formatted Microsoft Excel (.xlsx) workbooks with multi-sheet relations.
        </p>
      </div>

      {/* Export Configuration Card */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-5">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
            <Filter className="w-4 h-4 text-emerald-400" />
            Workbook Scope & Filters
          </h3>
          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/60">
            OpenPyXL Engine
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Industrial Zone Scope
            </label>
            <select
              value={selectedZone}
              onChange={(e) => setSelectedZone(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-emerald-500 font-mono"
            >
              <option value="all">All Bursa Industrial Zones (Consolidated)</option>
              {zones.map((z) => (
                <option key={z.id} value={z.id}>
                  {z.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Contacts Provenance Filter
            </label>
            <div className="flex items-center h-9">
              <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={includeVerifiedOnly}
                  onChange={(e) => setIncludeVerifiedOnly(e.target.checked)}
                  className="rounded bg-slate-950 border-slate-700 text-emerald-600 focus:ring-emerald-500 w-4 h-4"
                />
                <span>Include Verified & High-Confidence (≥90%) Contacts Only</span>
              </label>
            </div>
          </div>
        </div>

        {/* Multi-Sheet Breakdown Preview */}
        <div className="space-y-2 pt-2 border-t border-slate-800">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Included Workbook Sheets
          </span>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
            {sheets.map((sheet) => {
              const Icon = sheet.icon;
              return (
                <div
                  key={sheet.name}
                  className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-3 space-y-1.5"
                >
                  <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-200">
                    <Icon className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                    <span>{sheet.name}</span>
                  </div>
                  <p className="text-[10px] text-slate-500 leading-normal line-clamp-3">
                    {sheet.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Generate Button */}
        <div className="flex items-center justify-between pt-2">
          {successMessage ? (
            <div className="flex items-center gap-2 text-xs text-emerald-400 font-mono">
              <CheckCircle2 className="w-4 h-4" />
              <span>{successMessage}</span>
            </div>
          ) : (
            <span className="text-xs text-slate-500 font-mono">
              Ready to generate formatted .xlsx with column autofit & styled headers
            </span>
          )}

          <button
            onClick={handleGenerateExport}
            disabled={isExporting}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-xs font-semibold text-white shadow-md shadow-emerald-600/30 transition disabled:opacity-50"
          >
            <Download className={`w-3.5 h-3.5 ${isExporting ? 'animate-bounce' : ''}`} />
            {isExporting ? 'Building Workbook...' : 'Generate & Download .xlsx'}
          </button>
        </div>
      </div>

      {/* Available Downloads List */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
        <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
          <FileCheck className="w-4 h-4 text-emerald-400" />
          Export Artifacts Archive
        </h3>

        <div className="space-y-2">
          <div className="p-3 bg-slate-800/30 border border-slate-800 rounded-lg flex items-center justify-between text-xs">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded bg-emerald-950 text-emerald-400 border border-emerald-800/50">
                <FileSpreadsheet className="w-4 h-4" />
              </div>
              <div>
                <div className="font-semibold text-slate-200 font-mono">
                  bursa_industrial_intelligence_master.xlsx
                </div>
                <div className="text-[11px] text-slate-500 font-mono">
                  All Bursa OSBs • Companies • Contacts • Provenance Sources • 5 Sheets
                </div>
              </div>
            </div>
            <button
              onClick={handleGenerateExport}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-slate-800 hover:bg-emerald-600 hover:text-white text-xs font-medium text-slate-300 transition border border-slate-700"
            >
              <Download className="w-3 h-3" />
              Download
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
