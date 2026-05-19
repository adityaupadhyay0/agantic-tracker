"use client";
import React, { useEffect, useState } from 'react';
import { ShoppingBag, Star, Download, Filter, RefreshCw } from 'lucide-react';

export default function MarketplacePage() {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/marketplace/')
      .then(res => res.json())
      .then(data => {
          setTemplates(data);
          setLoading(false);
      });
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-bold">BCO Template Marketplace</h2>
          <p className="text-slate-400">Pre-built behavioral context templates for common workflows.</p>
        </div>
        <div className="flex space-x-2">
            <button className="flex items-center space-x-2 px-4 py-2 bg-slate-800 rounded-lg text-sm font-medium hover:bg-slate-700">
                <Filter size={16} />
                <span>Filter</span>
            </button>
        </div>
      </div>

      {loading ? (
          <div className="h-64 flex items-center justify-center">
              <RefreshCw className="animate-spin text-indigo-400" />
          </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {templates.map((t, i) => (
                <TemplateCard
                    key={i}
                    name={t.name}
                    description={t.description}
                    scope={t.scope}
                    category={t.type}
                    stars={4.7 + (i * 0.1)}
                    downloads={`${1.2 + i}k`}
                />
            ))}
        </div>
      )}
    </div>
  );
}

function TemplateCard({ name, description, scope, category, stars, downloads }) {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between space-y-4 hover:border-indigo-500/50 transition-colors">
            <div className="space-y-2">
                <div className="flex justify-between items-start">
                    <span className="text-[10px] font-bold uppercase tracking-widest text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded">{category}</span>
                    <div className="flex items-center space-x-1 text-amber-400 text-xs">
                        <Star size={12} fill="currentColor" />
                        <span className="font-bold">{stars}</span>
                    </div>
                </div>
                <h3 className="text-lg font-bold text-slate-100">{name}</h3>
                <p className="text-sm text-slate-400 line-clamp-2">{description}</p>
            </div>

            <div className="pt-4 border-t border-slate-800 flex justify-between items-center">
                <div className="flex flex-col">
                    <span className="text-[10px] text-slate-500 uppercase font-bold tracking-tight">Scope</span>
                    <span className="text-xs text-slate-300">{scope}</span>
                </div>
                <button className="flex items-center space-x-2 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-md text-xs font-bold transition-colors">
                    <Download size={14} />
                    <span>Install</span>
                </button>
            </div>
        </div>
    )
}
