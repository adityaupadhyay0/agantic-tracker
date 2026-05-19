"use client";
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Calendar, Users, Target } from 'lucide-react';

const data = [
  { name: 'Mon', deep_focus: 4, coordination: 2, implementation: 6 },
  { name: 'Tue', deep_focus: 5, coordination: 3, implementation: 7 },
  { name: 'Wed', deep_focus: 2, coordination: 6, implementation: 4 },
  { name: 'Thu', deep_focus: 6, coordination: 1, implementation: 8 },
  { name: 'Fri', deep_focus: 3, coordination: 4, implementation: 5 },
];

export default function TrendsDashboard() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold">Organizational Health Trends</h2>
        <p className="text-slate-400">Longitudinal behavioral analysis and drift detection.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div className="flex justify-between items-center mb-6">
             <h3 className="text-lg font-semibold flex items-center space-x-2">
                <Target className="text-indigo-400" size={18} />
                <span>Work State Distribution (Weekly)</span>
             </h3>
             <div className="text-xs text-slate-500 font-mono">Last 7 Days</div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <defs>
                  <linearGradient id="colorFocus" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#818cf8" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#818cf8" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc' }}
                    itemStyle={{ color: '#818cf8' }}
                />
                <Area type="monotone" dataKey="deep_focus" stroke="#818cf8" fillOpacity={1} fill="url(#colorFocus)" />
                <Area type="monotone" dataKey="implementation" stroke="#34d399" fillOpacity={0} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <div className="flex justify-between items-center mb-6">
             <h3 className="text-lg font-semibold flex items-center space-x-2">
                <Users className="text-amber-400" size={18} />
                <span>Coordination Velocity</span>
             </h3>
             <div className="text-xs text-slate-500 font-mono">Vs. Implementation</div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc' }}
                />
                <Line type="monotone" dataKey="coordination" stroke="#fbbf24" strokeWidth={2} dot={{ fill: '#fbbf24' }} />
                <Line type="monotone" dataKey="implementation" stroke="#10b981" strokeWidth={2} strokeDasharray="5 5" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center space-x-2">
            <Calendar className="text-purple-400" size={18} />
            <span>Temporal Drift Analysis</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <DriftMetric label="Deep Focus Baseline" delta="-12%" status="Declining" color="text-red-400" />
            <DriftMetric label="Onboarding Velocity" delta="+4.2%" status="Improving" color="text-emerald-400" />
            <DriftMetric label="Coordination Latency" delta="+15%" status="Critical" color="text-red-400" />
        </div>
      </div>
    </div>
  );
}

function DriftMetric({ label, delta, status, color }) {
    return (
        <div className="p-4 bg-slate-800/30 rounded-lg border border-slate-800 space-y-1">
            <div className="text-xs font-medium text-slate-500 uppercase tracking-wider">{label}</div>
            <div className="flex justify-between items-end">
                <div className={`text-xl font-bold ${color}`}>{delta}</div>
                <div className="text-[10px] text-slate-400 font-bold uppercase">{status}</div>
            </div>
        </div>
    )
}
