import React, { useState, useEffect } from 'react';
import { onBackendStatusChange } from '../services/api';
import { 
  Anchor, 
  LayoutDashboard, 
  TrendingDown, 
  Anchor as PortIcon, 
  BarChart3, 
  CloudSun, 
  Sliders, 
  Bell 
} from 'lucide-react';

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'forecasting', label: 'Freight Forecast', icon: TrendingDown },
  { id: 'ports', label: 'Ports & Draft', icon: PortIcon },
  { id: 'market', label: 'Market & Fleet', icon: BarChart3 },
  { id: 'weather', label: 'Weather Telemetry', icon: CloudSun },
  { id: 'optimization', label: 'OR Optimizer', icon: Sliders },
  { id: 'alerts', label: 'Alerts', icon: Bell },
];

export default function Navbar({ activeTab, setActiveTab, alertCount = 4 }) {
  const [isLive, setIsLive] = useState(false);

  useEffect(() => {
    const unsubscribe = onBackendStatusChange((live) => {
      setIsLive(live);
    });
    return unsubscribe;
  }, []);

  return (
    <header className="bg-slate-900/90 backdrop-blur border-b border-slate-800 sticky top-0 z-50 px-4 lg:px-8 py-3.5">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Brand Header */}
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-tr from-cyan-600 to-blue-600 p-2.5 rounded-xl shadow-lg shadow-cyan-500/20 text-white">
            <Anchor className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-cyan-400 via-sky-300 to-blue-400 bg-clip-text text-transparent">
                HEXAKADAL
              </h1>
              <span className="bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-[10px] font-mono px-2 py-0.5 rounded-full font-semibold">
                v2.0 Spring/React
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium">
              AI Maritime Freight Engine &amp; Commercial DSS for India's East Coast
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto pb-1 md:pb-0 scrollbar-none">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all whitespace-nowrap ${
                  isActive
                    ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm shadow-cyan-500/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
                {item.id === 'alerts' && alertCount > 0 && (
                  <span className="bg-rose-500 text-white text-[10px] font-bold px-1.5 py-0.2 rounded-full">
                    {alertCount}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Backend Status Pill */}
        <div className="hidden xl:flex items-center gap-2 text-xs font-mono bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60">
          {isLive ? (
            <>
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              <span className="text-emerald-400 font-semibold">API LIVE</span>
              <span className="text-slate-500">|</span>
              <span className="text-slate-300">Port 8081</span>
            </>
          ) : (
            <>
              <span className="w-2 h-2 rounded-full bg-amber-400"></span>
              <span className="text-amber-400 font-semibold">OFFLINE (DEMO)</span>
              <span className="text-slate-500">|</span>
              <span className="text-slate-400">Mock Data</span>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
