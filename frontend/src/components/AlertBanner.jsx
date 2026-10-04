import React from 'react';
import { AlertTriangle, CheckCircle, ShieldAlert, Info } from 'lucide-react';

export default function AlertBanner({ signal = 'WAIT / DEFER FIXING', reason = '' }) {
  const safeSignal = signal || 'WAIT / DEFER FIXING';
  let isPositive = safeSignal.includes('FIX IMMEDIATELY') || safeSignal.includes('FIX NOW');
  let isWarning = safeSignal.includes('WAIT') || safeSignal.includes('DEFER');
  let isDanger = safeSignal.includes('REROUTE') || safeSignal.includes('VIOLATION');

  let badgeColor = isDanger
    ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
    : isWarning
    ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
    : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';

  let bannerBg = isDanger
    ? 'from-rose-950/40 via-slate-900 to-slate-900 border-rose-500/30'
    : isWarning
    ? 'from-amber-950/40 via-slate-900 to-slate-900 border-amber-500/30'
    : 'from-emerald-950/40 via-slate-900 to-slate-900 border-emerald-500/30';

  let Icon = isDanger ? ShieldAlert : isWarning ? AlertTriangle : CheckCircle;

  return (
    <div className={`bg-gradient-to-r ${bannerBg} border rounded-2xl p-5 md:p-6 shadow-xl relative overflow-hidden my-6`}>
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-start gap-4">
          <div className={`p-3 rounded-xl border ${badgeColor} shrink-0`}>
            <Icon className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400">
                EXECUTIVE ACTION SIGNAL
              </span>
            </div>
            <h2 className="text-xl md:text-2xl font-extrabold font-mono text-white tracking-wide">
              {signal}
            </h2>
            {reason && (
              <p className="text-sm text-slate-300 mt-2 leading-relaxed flex items-start gap-2">
                <Info className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                <span><strong className="text-cyan-300">Explainable AI (XAI) Rationale:</strong> {reason}</span>
              </p>
            )}
          </div>
        </div>

        <div className="shrink-0 self-end md:self-center">
          <span className={`inline-flex items-center px-4 py-2 rounded-xl text-xs font-mono font-bold border ${badgeColor}`}>
            ACTIONABLE INTEL
          </span>
        </div>
      </div>
    </div>
  );
}
