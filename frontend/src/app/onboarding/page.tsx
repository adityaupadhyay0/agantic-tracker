"use client";
import React from 'react';
import { Users, Settings, BarChart3, Database } from 'lucide-react';

export default function SetupPage() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold">Organizational Setup</h2>
        <p className="text-slate-400">Configure CORTEX for your engineering and cross-functional teams.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex items-center space-x-2 text-indigo-400 mb-2">
                <Users size={20} />
                <h3 className="text-lg font-semibold text-slate-50">Team Management</h3>
            </div>
            <p className="text-sm text-slate-400">Define team boundaries and assign leads for scoped context enrichment.</p>
            <div className="space-y-2">
                <TeamItem name="Engineering - Alpha" members={12} lead="Sarah Chen" />
                <TeamItem name="Product Design" members={5} lead="Marco Ross" />
                <TeamItem name="Platform Ops" members={8} lead="Elena Gruff" />
            </div>
            <button className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-sm font-medium transition-colors mt-4">Add New Team</button>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex items-center space-x-2 text-purple-400 mb-2">
                <Settings size={20} />
                <h3 className="text-lg font-semibold text-slate-50">Ontology Customization</h3>
            </div>
            <p className="text-sm text-slate-400">Extend the CORTEX Ontology with domain-specific work states.</p>
            <div className="space-y-3">
                <OntologyItem label="deep_focus" status="Core" />
                <OntologyItem label="design_focus" status="Active" />
                <OntologyItem label="market_analysis" status="Active" />
                <div className="pt-2">
                    <button className="text-xs text-indigo-400 hover:underline">+ Define custom work state</button>
                </div>
            </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex items-center space-x-2 text-amber-400 mb-2">
                <Database size={20} />
                <h3 className="text-lg font-semibold text-slate-50">Managed Integrations</h3>
            </div>
            <p className="text-sm text-slate-400">Manage telemetry sources and ingestion health.</p>
            <div className="grid grid-cols-2 gap-3">
                <IntegrationBadge name="VS Code" status="Healthy" />
                <IntegrationBadge name="GitHub" status="Healthy" />
                <IntegrationBadge name="Slack" status="Healthy" />
                <IntegrationBadge name="Figma" status="Connected" />
                <IntegrationBadge name="Calendar" status="Pending" />
                <IntegrationBadge name="Notion" status="Connected" />
            </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
            <div className="flex items-center space-x-2 text-emerald-400 mb-2">
                <BarChart3 size={20} />
                <h3 className="text-lg font-semibold text-slate-50">Enterprise Governance</h3>
            </div>
            <p className="text-sm text-slate-400">Audit context consumption and manage data residency.</p>
            <div className="space-y-4 text-xs text-slate-500">
                <div className="flex justify-between border-b border-slate-800 pb-2">
                    <span>Last Privacy Audit</span>
                    <span className="text-slate-300 font-mono">2026-05-19 09:12 UTC</span>
                </div>
                <div className="flex justify-between border-b border-slate-800 pb-2">
                    <span>Data Residency</span>
                    <span className="text-slate-300">US-East (Managed)</span>
                </div>
                <div className="flex justify-between">
                    <span>Active RBAC Policy</span>
                    <span className="text-indigo-400">v2.1-Standard</span>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
}

function TeamItem({ name, members, lead }) {
    return (
        <div className="flex justify-between items-center p-3 bg-slate-800/30 rounded-lg border border-slate-800">
            <div>
                <div className="text-sm font-medium text-slate-200">{name}</div>
                <div className="text-[10px] text-slate-500 italic">Lead: {lead}</div>
            </div>
            <div className="text-xs text-slate-400">{members} members</div>
        </div>
    )
}

function OntologyItem({ label, status }) {
    return (
        <div className="flex justify-between items-center text-sm">
            <code className="text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded text-xs">{label}</code>
            <span className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">{status}</span>
        </div>
    )
}

function IntegrationBadge({ name, status }) {
    return (
        <div className="flex flex-col p-3 bg-slate-800/50 rounded-lg border border-slate-800 items-center justify-center space-y-1">
            <div className="text-xs font-semibold text-slate-300">{name}</div>
            <div className={`text-[9px] uppercase font-bold ${status === 'Healthy' ? 'text-emerald-500' : 'text-amber-500'}`}>{status}</div>
        </div>
    )
}
