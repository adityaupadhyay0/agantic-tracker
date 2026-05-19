"use client";
import React from 'react';
import { Activity, Brain, Shield, Zap, Loader2 } from 'lucide-react';
import { useCortexBCOs } from '../hooks/useCortex';

export default function Dashboard() {
  const { bcos, loading } = useCortexBCOs();

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-bold">Organizational Intelligence</h2>
          <p className="text-slate-400">Real-time behavioral context substrate status.</p>
        </div>
        <div className="bg-indigo-500/10 border border-indigo-500/20 px-4 py-2 rounded-lg">
          <span className="text-indigo-400 text-sm font-mono">System Active</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard icon={<Activity className="text-blue-400" />} label="Active Signals" value="--" />
        <StatCard icon={<Brain className="text-purple-400" />} label="BCOs Generated" value={bcos.length} />
        <StatCard icon={<Zap className="text-amber-400" />} label="Context Hits" value="--" />
        <StatCard icon={<Shield className="text-emerald-400" />} label="Privacy Audits" value="100%" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h3 className="text-lg font-semibold mb-4">Recent Behavioral Context Objects</h3>
          <div className="space-y-4">
            {loading ? (
               <div className="flex items-center space-x-2 text-slate-500">
                 <Loader2 className="animate-spin" size={16} />
                 <span>Loading BCOs...</span>
               </div>
            ) : bcos.length === 0 ? (
               <div className="text-slate-500 text-sm">No context objects generated yet.</div>
            ) : (
              bcos.map((bco: any) => (
                <BCOItem key={bco.bco_id} label={bco.label} type={bco.type} confidence={bco.confidence} />
              ))
            )}
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h3 className="text-lg font-semibold mb-4">Telemetry Stream</h3>
          <div className="space-y-3 font-mono text-xs">
            <LogItem time="14:20:11" source="IDE" event="file_edit" />
            <LogItem time="14:19:45" source="Git" event="pr_comment" />
            <LogItem time="14:18:02" source="IDE" event="debug_start" />
            <LogItem time="14:15:30" source="Slack" event="metadata_sync" />
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value }) {
  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-2">
      <div className="flex items-center space-x-2 text-slate-400">
        {icon}
        <span className="text-xs font-medium uppercase tracking-wider">{label}</span>
      </div>
      <div className="text-2xl font-bold">{value}</div>
    </div>
  );
}

function BCOItem({ label, type, confidence }) {
  return (
    <div className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg border border-slate-800">
      <div>
        <div className="font-medium">{label}</div>
        <div className="text-xs text-slate-500 uppercase tracking-tight">{type}</div>
      </div>
      <div className="text-right">
        <div className="text-indigo-400 font-bold">{Math.round(confidence * 100)}%</div>
        <div className="text-[10px] text-slate-500 uppercase">Confidence</div>
      </div>
    </div>
  );
}

function LogItem({ time, source, event }) {
  return (
    <div className="flex space-x-4 text-slate-500">
      <span className="text-slate-600">{time}</span>
      <span className="text-indigo-400 w-12">[{source}]</span>
      <span className="text-slate-300">{event}</span>
    </div>
  );
}
