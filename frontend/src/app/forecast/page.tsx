"use client";
import React from 'react';
import { AlertTriangle, TrendingUp, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function ForecastView() {
  return (
    <div className="space-y-8">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-bold">Behavioral Forecast</h2>
          <p className="text-slate-400">Predictive organizational dynamics and risk modeling.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        <PredictionCard
            type="COORDINATION_RISK"
            label="High Risk of Coordination Breakdown"
            probability={0.82}
            window="Next 7 Days"
            impact="High"
            evidence={["Recurring PR review bottlenecks", "Increasing coordination/implementation ratio"]}
            remediation={["Shift to async status updates", "Reduce weekly recurring meetings by 20%"]}
        />

        <PredictionCard
            type="EXPERTISE_GAP"
            label="Emerging Gap in Cloud Infrastructure"
            probability={0.65}
            window="Next 30 Days"
            impact="Medium"
            evidence={["Declining implementation signals in infra domain", "Primary contributor shift to design states"]}
            remediation={["Schedule knowledge transfer session", "Cross-train backend engineers on Terraform"]}
        />
      </div>
    </div>
  );
}

function PredictionCard({ type, label, probability, window, impact, evidence, remediation }) {
    const colorClass = probability > 0.75 ? 'border-red-500/30 bg-red-500/5' : 'border-amber-500/30 bg-amber-500/5';
    const iconClass = probability > 0.75 ? 'text-red-400' : 'text-amber-400';

    return (
        <div className={`border rounded-xl p-6 space-y-6 ${colorClass}`}>
            <div className="flex justify-between items-start">
                <div className="flex items-center space-x-3">
                    {probability > 0.75 ? <ShieldAlert className={iconClass} /> : <AlertTriangle className={iconClass} />}
                    <div>
                        <h3 className="text-xl font-bold text-slate-100">{label}</h3>
                        <div className="text-xs font-medium uppercase tracking-wider text-slate-500">{type.replace('_', ' ')} · {window}</div>
                    </div>
                </div>
                <div className="text-right">
                    <div className={`text-2xl font-bold ${iconClass}`}>{Math.round(probability * 100)}%</div>
                    <div className="text-[10px] uppercase text-slate-500 font-bold">Probability</div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-3">
                    <h4 className="text-xs font-bold uppercase text-slate-500 flex items-center space-x-2">
                        <TrendingUp size={14} />
                        <span>Supporting Evidence</span>
                    </h4>
                    <ul className="space-y-2">
                        {evidence.map((e, i) => (
                            <li key={i} className="text-sm text-slate-300 flex items-start space-x-2">
                                <span className="text-indigo-400 font-bold">•</span>
                                <span>{e}</span>
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="space-y-3">
                    <h4 className="text-xs font-bold uppercase text-slate-500 flex items-center space-x-2">
                        <CheckCircle2 size={14} />
                        <span>Recommended Remediation</span>
                    </h4>
                    <div className="space-y-2">
                        {remediation.map((r, i) => (
                            <div key={i} className="bg-slate-900/50 border border-slate-800 p-2 rounded text-sm text-slate-300 italic">
                                {r}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
