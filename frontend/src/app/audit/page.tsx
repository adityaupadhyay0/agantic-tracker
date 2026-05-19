"use client";
import React, { useEffect, useState } from 'react';
import { Shield, Clock, User, Activity, RefreshCw } from 'lucide-react';

export default function AuditDashboard() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/audit/', {
        headers: { 'X-API-Key': 'admin_key' }
      });
      const data = await res.json();
      setLogs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold flex items-center space-x-3">
            <Shield className="text-indigo-400" />
            <span>Compliance & Audit Log</span>
        </h2>
        <p className="text-slate-400">Full audit trail of all data ingestion, BCO enrichment, and AI system access.</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden min-h-[400px] flex flex-col">
        {loading ? (
            <div className="flex-1 flex items-center justify-center">
                <RefreshCw className="animate-spin text-indigo-400" />
            </div>
        ) : (
            <table className="w-full text-left">
            <thead className="bg-slate-800/50 text-xs font-bold uppercase text-slate-500">
                <tr>
                <th className="p-4">Timestamp</th>
                <th className="p-4">Action</th>
                <th className="p-4">Actor</th>
                <th className="p-4">Resource</th>
                <th className="p-4">Scope</th>
                </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
                {logs.length === 0 && (
                    <tr>
                        <td colSpan={5} className="p-8 text-center text-slate-500 text-sm italic">
                            No audit logs found. Ingest telemetry or access BCOs to generate logs.
                        </td>
                    </tr>
                )}
                {logs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="p-4 text-xs font-mono text-slate-400">{log.timestamp}</td>
                    <td className="p-4">
                    <span className="bg-indigo-500/10 text-indigo-400 px-2 py-1 rounded text-[10px] font-bold">
                        {log.action}
                    </span>
                    </td>
                    <td className="p-4 text-sm flex items-center space-x-2">
                        <User size={14} className="text-slate-500" />
                        <span>{log.actor_id}</span>
                    </td>
                    <td className="p-4 text-sm text-slate-300 truncate max-w-[200px]">{log.resource_id}</td>
                    <td className="p-4">
                    <span className="capitalize text-[10px] bg-slate-800 px-2 py-1 rounded font-medium text-slate-400">
                        {log.scope}
                    </span>
                    </td>
                </tr>
                ))}
            </tbody>
            </table>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <StatCard icon={<Activity />} label="Total Events Logged" value="1.2M" />
          <StatCard icon={<Shield />} label="Security Incidents" value="0" />
          <StatCard icon={<Clock />} label="Log Retention" value="90 Days" />
      </div>
    </div>
  );
}

function StatCard({ icon, label, value }) {
    return (
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-2">
            <div className="text-indigo-400">{icon}</div>
            <div className="text-xs font-bold uppercase text-slate-500">{label}</div>
            <div className="text-2xl font-bold">{value}</div>
        </div>
    )
}
