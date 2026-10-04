import React, { useState, useEffect } from 'react';
import KpiCard from '../components/KpiCard';
import AlertBanner from '../components/AlertBanner';
import { fetchDashboard, postOptimization } from '../services/api';
import { DollarSign, TrendingUp, AlertOctagon, Clock, Ship, Anchor, Waves, RefreshCw } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cargoQty, setCargoQty] = useState(150000);
  const [destinationPort, setDestinationPort] = useState('Paradip Port');
  const [demurrageRate, setDemurrageRate] = useState(30000);

  const loadDashboard = async () => {
    setLoading(true);
    try {
      const optRes = await postOptimization({
        cargoQuantity: cargoQty,
        destinationPort: destinationPort,
        demurrageRateOverride: demurrageRate
      });
      
      const dash = await fetchDashboard();
      setData({
        ...dash,
        ndv: optRes.netDecisionValue,
        freightSavings: optRes.potentialFreightSavings,
        demurrageLoss: optRes.demurrageCost,
        executiveSignal: optRes.executiveSignal,
        xaiReason: optRes.xaiReason,
        selectedVessel: optRes.selectedVessel,
        vesselDraft: optRes.vesselDraft,
        portMaxDraft: optRes.portMaxDraft
      });
    } catch (err) {
      console.error('Error fetching dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, [cargoQty, destinationPort, demurrageRate]);

  const sampleTrendData = [
    { day: 'Day -10', rate: 19.80 },
    { day: 'Day -7', rate: 19.20 },
    { day: 'Day -5', rate: 18.90 },
    { day: 'Day -2', rate: 18.65 },
    { day: 'Today (Spot)', rate: data?.currentSpotRate ?? 18.50 },
    { day: 'Day +5 (FC)', rate: 17.80 },
    { day: 'Day +10 (FC)', rate: 16.90 },
    { day: 'Day +15 (FC)', rate: data?.targetForecastRate ?? 16.28 }
  ];

  if (loading && !data) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <RefreshCw className="w-10 h-10 text-cyan-400 animate-spin" />
        <span className="text-sm font-mono text-slate-400">Loading Maritime Decision Support Engine...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Parameters Control Bar */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 md:p-5 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <Ship className="w-5 h-5 text-cyan-400" />
          <h2 className="text-sm font-bold font-mono text-slate-200">Voyage &amp; Procurement Parameters</h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 w-full md:w-auto text-xs">
          <div>
            <label className="block text-slate-400 mb-1 font-mono">Cargo Quantity (MT)</label>
            <input
              type="number"
              step="5000"
              value={cargoQty}
              onChange={(e) => setCargoQty(Number(e.target.value))}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-cyan-300 font-mono w-full focus:outline-none focus:border-cyan-500"
            />
          </div>

          <div>
            <label className="block text-slate-400 mb-1 font-mono">Destination Port</label>
            <select
              value={destinationPort}
              onChange={(e) => setDestinationPort(e.target.value)}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-cyan-300 font-mono w-full focus:outline-none focus:border-cyan-500"
            >
              <option value="Paradip Port">Paradip Port (17.5m)</option>
              <option value="Visakhapatnam Port">Visakhapatnam Port (16.1m)</option>
              <option value="Dhamra Port">Dhamra Port (18.0m)</option>
              <option value="Haldia Port">Haldia Port (8.5m)</option>
              <option value="Gopalpur Port">Gopalpur Port (14.5m)</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-400 mb-1 font-mono">Daily Demurrage ($ USD/day)</label>
            <input
              type="number"
              step="1000"
              value={demurrageRate}
              onChange={(e) => setDemurrageRate(Number(e.target.value))}
              className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-1.5 text-cyan-300 font-mono w-full focus:outline-none focus:border-cyan-500"
            />
          </div>
        </div>
      </div>

      {/* Executive Action Banner */}
      <AlertBanner signal={data?.executiveSignal} reason={data?.xaiReason} />

      {/* Key Financial Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          title="Net Decision Value (NDV)"
          value={`$${(data?.ndv || 0).toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}`}
          subtitle="Net Expected Charter Savings"
          icon={DollarSign}
          color={data?.ndv > 0 ? 'emerald' : 'rose'}
          trend={data?.ndv > 0 ? '+SAVINGS' : '-RISK'}
        />

        <KpiCard
          title="Freight Savings (USD)"
          value={`$${(data?.freightSavings || 0).toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}`}
          subtitle={`Forecasted $${((data?.currentSpotRate ?? 18.50) - (data?.targetForecastRate ?? 16.28)).toFixed(2)}/MT drop`}
          icon={TrendingUp}
          color="cyan"
        />

        <KpiCard
          title="Demurrage Loss Risk"
          value={`$${(data?.demurrageLoss || 0).toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}`}
          subtitle={`Based on ${data?.totalCongestionQueueHours || 25.7}h anchorage queue`}
          icon={AlertOctagon}
          color="amber"
        />

        <KpiCard
          title="Total Congestion Queue"
          value={`${data?.totalCongestionQueueHours || 25.7} Hours`}
          subtitle={`~${data?.waitingVesselsCount || 9} vessels waiting in queue`}
          icon={Clock}
          color="blue"
        />
      </div>

      {/* 3 Feeder Module Status Panels */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Module 1 */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            <TrendingUp className="w-5 h-5 text-cyan-400" />
            <h3 className="font-mono font-bold text-sm text-slate-200">Module 1: Rate Forecaster</h3>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between text-slate-400">
              <span>Current Spot Rate:</span>
              <span className="font-mono text-white font-semibold">${(data?.currentSpotRate ?? 18.50).toFixed(2)} / MT</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>15-Day XGBoost Target:</span>
              <span className="font-mono text-cyan-400 font-semibold">${(data?.targetForecastRate ?? 16.28).toFixed(2)} / MT</span>
            </div>
            <div className="flex justify-between text-slate-400 text-xs">
              <span>Model Confidence:</span>
              <span className="font-mono text-emerald-400 font-bold">94.2% XGBoost4J</span>
            </div>
          </div>
        </div>

        {/* Module 2 */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            <Anchor className="w-5 h-5 text-blue-400" />
            <h3 className="font-mono font-bold text-sm text-slate-200">Module 2: Draft Clearance</h3>
          </div>
          <div className="space-y-2 text-sm">
            <div className="text-slate-300 font-semibold text-xs truncate">
              {data?.selectedVessel || 'MV CAPESIZE HERO (180k DWT)'}
            </div>
            <div className="flex justify-between text-slate-400 text-xs">
              <span>Vessel Draft: <strong className="text-white">{data?.vesselDraft ?? 16.5} m</strong></span>
              <span>Port Max Draft: <strong className="text-cyan-400">{data?.portMaxDraft ?? 17.5} m</strong></span>
            </div>
            <div className="pt-1">
              {(data?.vesselDraft ?? 16.5) <= (data?.portMaxDraft ?? 17.5) ? (
                <span className="inline-block bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-mono font-bold px-2.5 py-1 rounded-lg">
                  ✅ Safe Draft Clearance
                </span>
              ) : (
                <span className="inline-block bg-rose-500/10 text-rose-400 border border-rose-500/30 text-xs font-mono font-bold px-2.5 py-1 rounded-lg">
                  ⚠️ Draft Violation Risk!
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Module 3 */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            <Waves className="w-5 h-5 text-amber-400" />
            <h3 className="font-mono font-bold text-sm text-slate-200">Module 3: Weather Telemetry</h3>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between text-slate-400">
              <span>Live Wave Height:</span>
              <span className="font-mono text-amber-300 font-semibold">{data?.liveWaveHeight ?? 2.4} m</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Sea Status:</span>
              <span className="font-mono text-slate-200">{data?.weatherStatus || 'Moderate Swell'}</span>
            </div>
            <div className="flex justify-between text-slate-400 text-xs">
              <span>Telemetry Source:</span>
              <span className="font-mono text-cyan-400 font-semibold">Open-Meteo Marine API</span>
            </div>
          </div>
        </div>
      </div>

      {/* Forecast Trend Chart */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-base font-bold font-mono text-slate-100">Baltic Freight Index &amp; 15-Day XGBoost Projection</h3>
            <p className="text-xs text-slate-400">Historical Baltic Capesize index trend vs Machine Learning predicted spot trajectory</p>
          </div>
          <span className="bg-slate-800 text-cyan-400 border border-slate-700 text-xs font-mono px-3 py-1 rounded-lg">
            USD / Metric Ton
          </span>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={sampleTrendData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="rateColor" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="day" stroke="#64748b" tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <YAxis domain={['auto', 'auto']} stroke="#64748b" tick={{ fill: '#94a3b8', fontSize: 12 }} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                itemStyle={{ color: '#38bdf8' }}
              />
              <Area type="monotone" dataKey="rate" stroke="#06b6d4" strokeWidth={3} fillOpacity={1} fill="url(#rateColor)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
