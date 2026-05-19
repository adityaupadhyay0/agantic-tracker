"use client";
import React from 'react';
import { Eye, ShieldCheck, Trash2 } from 'lucide-react';

export default function TransparencyPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h2 className="text-3xl font-bold">Your Privacy Dashboard</h2>
        <p className="text-slate-400">Total transparency into how CORTEX observes your work and builds context.</p>
      </div>

      <div className="bg-emerald-500/10 border border-emerald-500/20 p-6 rounded-xl flex items-start space-x-4">
        <ShieldCheck className="text-emerald-400 w-8 h-8 mt-1" />
        <div>
          <h4 className="font-semibold text-emerald-500">Privacy Commitment</h4>
          <p className="text-sm text-slate-300">
            CORTEX never captures message content or document text. We only analyze metadata and behavioral traces
            to help your AI agents understand your workflow.
          </p>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-xl font-semibold">Active Signals</h3>
        <div className="bg-slate-900 border border-slate-800 rounded-xl divide-y divide-slate-800">
          <SignalToggle label="IDE Activity" description="File edits, navigation, and debugger usage" active={true} />
          <SignalToggle label="Git Metadata" description="Commits, PR reviews, and branch activity" active={true} />
          <SignalToggle label="Communication Metadata" description="Slack thread patterns and response times" active={true} />
          <SignalToggle label="Calendar Metadata" description="Meeting frequency and duration" active={false} />
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-xl font-semibold">Data Control</h3>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex justify-between items-center">
            <div>
              <h4 className="font-medium">Export Behavioral Profile</h4>
              <p className="text-xs text-slate-500">Download a JSON of all BCOs that reference your activity.</p>
            </div>
            <button className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-medium transition-colors">Export Data</button>
          </div>
          <div className="flex justify-between items-center text-red-400">
            <div>
              <h4 className="font-medium">Delete My Data</h4>
              <p className="text-xs text-red-400/60">Permanently remove all your behavioral traces and BCO associations.</p>
            </div>
            <button className="flex items-center space-x-2 px-4 py-2 border border-red-400/30 hover:bg-red-400/10 rounded-lg text-sm font-medium transition-colors">
              <Trash2 size={16} />
              <span>Request Deletion</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function SignalToggle({ label, description, active }) {
  return (
    <div className="p-6 flex justify-between items-center">
      <div>
        <h4 className="font-medium">{label}</h4>
        <p className="text-xs text-slate-500">{description}</p>
      </div>
      <div className={`w-12 h-6 rounded-full p-1 cursor-pointer transition-colors ${active ? 'bg-indigo-600' : 'bg-slate-700'}`}>
        <div className={`w-4 h-4 bg-white rounded-full transition-transform ${active ? 'translate-x-6' : ''}`} />
      </div>
    </div>
  );
}
