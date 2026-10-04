import axios from 'axios';

const API_BASE_URL = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 2500, // Fast timeout to fail over quickly to mock data if backend is offline
});

// Track backend connection status
let backendConnected = false;
let listeners = [];

export const onBackendStatusChange = (callback) => {
  listeners.push(callback);
  callback(backendConnected);
  return () => {
    listeners = listeners.filter(cb => cb !== callback);
  };
};

const setBackendStatus = (status) => {
  if (backendConnected !== status) {
    backendConnected = status;
    listeners.forEach(cb => cb(backendConnected));
  }
};

export const isBackendLive = () => backendConnected;

// -------------------------------------------------------------
// HIGH-FIDELITY MOCK / FALLBACK DATASETS
// Based on actual CSV data: baltic.csv, ports.csv, vessels.csv, congestion.csv
// -------------------------------------------------------------

const PORT_DRAFT_MAP = {
  'Paradip Port': 17.50,
  'Visakhapatnam Port': 16.10,
  'Dhamra Port': 18.00,
  'Haldia Port': 8.50,
  'Gopalpur Port': 14.50,
  'Hay Point (Australia)': 19.00,
  'Newcastle (Australia)': 15.20,
  'Saldanha Bay (South Africa)': 20.50,
  'Port Hedland (Australia)': 20.00
};

const MOCK_PORTS = [
  { country: 'India', portName: 'Paradip Port', locode: 'INPRT', maxDraft: 17.50, latitude: 20.26, longitude: 86.67 },
  { country: 'India', portName: 'Visakhapatnam Port', locode: 'INVTZ', maxDraft: 16.10, latitude: 17.68, longitude: 83.21 },
  { country: 'India', portName: 'Dhamra Port', locode: 'INDHM', maxDraft: 18.00, latitude: 20.81, longitude: 86.97 },
  { country: 'India', portName: 'Haldia Port', locode: 'INHAL', maxDraft: 8.50, latitude: 22.02, longitude: 88.06 },
  { country: 'India', portName: 'Gopalpur Port', locode: 'INGPR', maxDraft: 14.50, latitude: 19.31, longitude: 84.91 },
  { country: 'Australia', portName: 'Hay Point (Australia)', locode: 'AUHPT', maxDraft: 19.00, latitude: -21.27, longitude: 149.30 },
  { country: 'Australia', portName: 'Newcastle (Australia)', locode: 'AUNCL', maxDraft: 15.20, latitude: -32.92, longitude: 151.78 },
  { country: 'South Africa', portName: 'Saldanha Bay (South Africa)', locode: 'ZASLD', maxDraft: 20.50, latitude: -33.01, longitude: 17.95 },
  { country: 'Australia', portName: 'Port Hedland (Australia)', locode: 'AUPHE', maxDraft: 20.00, latitude: -20.31, longitude: 118.57 }
];

const MOCK_HISTORICAL_RATES = [
  { date: '2026-09-01', price: 19.80, open: 19.60, high: 20.10, low: 19.40, volume: '45k', changePercent: '-0.5%' },
  { date: '2026-09-04', price: 19.45, open: 19.70, high: 19.90, low: 19.30, volume: '52k', changePercent: '-1.8%' },
  { date: '2026-09-07', price: 19.20, open: 19.40, high: 19.55, low: 19.05, volume: '60k', changePercent: '-1.3%' },
  { date: '2026-09-10', price: 19.00, open: 19.15, high: 19.30, low: 18.90, volume: '48k', changePercent: '-1.0%' },
  { date: '2026-09-13', price: 18.85, open: 19.00, high: 19.10, low: 18.75, volume: '55k', changePercent: '-0.8%' },
  { date: '2026-09-16', price: 18.65, open: 18.80, high: 18.90, low: 18.55, volume: '61k', changePercent: '-1.1%' },
  { date: '2026-09-19', price: 18.55, open: 18.60, high: 18.70, low: 18.45, volume: '58k', changePercent: '-0.5%' },
  { date: '2026-09-22', price: 18.50, open: 18.55, high: 18.65, low: 18.40, volume: '64k', changePercent: '-0.3%' },
  { date: '2026-09-25', price: 18.50, open: 18.50, high: 18.60, low: 18.45, volume: '59k', changePercent: '0.0%' }
];

const MOCK_FLEET = [
  { company: 'Vale S.A.', shipName: 'MV ORE BRASIL', builtYear: 2018, grossTonnage: 203953, deadweightTonnage: 400000, lengthMeters: 362, widthMeters: 65, estimatedDraft: 18.0 },
  { company: 'Oldendorff Carriers', shipName: 'MV CAPESIZE HERO', builtYear: 2019, grossTonnage: 100000, deadweightTonnage: 180000, lengthMeters: 290, widthMeters: 45, estimatedDraft: 16.5 },
  { company: 'Star Bulk Carriers', shipName: 'MV PANAMAX STAR', builtYear: 2017, grossTonnage: 45000, deadweightTonnage: 75000, lengthMeters: 225, widthMeters: 32, estimatedDraft: 12.0 },
  { company: 'Pacific Basin', shipName: 'MV SUPRAMAX OCEAN', builtYear: 2016, grossTonnage: 32000, deadweightTonnage: 55000, lengthMeters: 190, widthMeters: 32, estimatedDraft: 9.0 },
  { company: 'Berge Bulk', shipName: 'MV BERGE EVEREST', builtYear: 2020, grossTonnage: 195000, deadweightTonnage: 388000, lengthMeters: 360, widthMeters: 65, estimatedDraft: 18.0 },
  { company: 'Golden Ocean', shipName: 'MV GOLDEN SAGITTARIUS', builtYear: 2021, grossTonnage: 108000, deadweightTonnage: 208000, lengthMeters: 300, widthMeters: 50, estimatedDraft: 16.8 }
];

const MOCK_CONGESTION = [
  { economy: 'India', market: 'Dry Bulk', medianTimeInPortDays: 2.8, averageAgeYears: 11.4, averageDwt: 74200, timePeriod: '2026-Q1' },
  { economy: 'China', market: 'Dry Bulk', medianTimeInPortDays: 1.9, averageAgeYears: 9.8, averageDwt: 92400, timePeriod: '2026-Q1' },
  { economy: 'Australia', market: 'Dry Bulk', medianTimeInPortDays: 1.5, averageAgeYears: 8.5, averageDwt: 145000, timePeriod: '2026-Q1' },
  { economy: 'Brazil', market: 'Dry Bulk', medianTimeInPortDays: 3.2, averageAgeYears: 10.1, averageDwt: 168000, timePeriod: '2026-Q1' },
  { economy: 'South Africa', market: 'Dry Bulk', medianTimeInPortDays: 2.1, averageAgeYears: 11.0, averageDwt: 132000, timePeriod: '2026-Q1' }
];

const MOCK_ALERTS = [
  {
    id: 'ALT-001',
    title: 'XGBoost Rate Drop Signal',
    message: 'Freight spot rate forecasted to drop from $18.50/MT to $16.28/MT (-12.0%) over 15-day horizon.',
    severity: 'INFO',
    category: 'ML_FORECAST',
    timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
  },
  {
    id: 'ALT-002',
    title: 'Moderate Swell Advisory',
    message: 'Live wave height at Paradip Port recorded at 2.4m. Operational delay multiplier applied: +1.4x.',
    severity: 'WARNING',
    category: 'WEATHER',
    timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
  },
  {
    id: 'ALT-003',
    title: 'Draft Clearance Notice',
    message: 'Capesize vessel draft (16.5m) within safe operational margin for Paradip berth limit (17.5m).',
    severity: 'SUCCESS',
    category: 'DRAFT',
    timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
  },
  {
    id: 'ALT-004',
    title: 'OR-Tools Executive Decision',
    message: 'Net Decision Value (NDV) calculated at +$307,300 USD. Recommendation: DEFER FIXING CHARTERPARTY.',
    severity: 'CRITICAL',
    category: 'OPTIMIZATION',
    timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
  }
];

// Helper to simulate optimization calculation locally
export const calculateMockOptimization = ({ cargoQuantity = 150000, destinationPort = 'Paradip Port', demurrageRateOverride = 30000 }) => {
  const portMaxDraft = PORT_DRAFT_MAP[destinationPort] || 15.0;
  
  let selectedVessel = 'MV CAPESIZE HERO (180k DWT Capesize)';
  let vesselDraft = 16.5;
  if (cargoQuantity < 60000) {
    selectedVessel = 'MV SUPRAMAX OCEAN (55k DWT Supramax)';
    vesselDraft = 9.0;
  } else if (cargoQuantity < 120000) {
    selectedVessel = 'MV PANAMAX STAR (75k DWT Panamax)';
    vesselDraft = 12.0;
  }

  const isSafeDraft = vesselDraft <= portMaxDraft;
  const spotRate = 18.50;
  const forecastRate = 16.28;
  const rateDelta = Math.max(0, spotRate - forecastRate);
  const potentialSavings = cargoQuantity * rateDelta;

  const queueHoursMap = {
    'Paradip Port': 25.7,
    'Visakhapatnam Port': 18.2,
    'Dhamra Port': 14.5,
    'Haldia Port': 32.0,
    'Gopalpur Port': 12.0
  };
  const queueHours = queueHoursMap[destinationPort] || 20.0;
  const demurrageCost = (demurrageRateOverride / 24.0) * queueHours;
  const netDecisionValue = potentialSavings - demurrageCost;

  let executiveSignal = 'DEFER FIXING CHARTERPARTY (RECOMMENDED)';
  let xaiReason = `Forecasted market drop of -$${rateDelta.toFixed(2)}/MT yields $${potentialSavings.toLocaleString()} savings, offsetting demurrage risk ($${Math.round(demurrageCost).toLocaleString()} for ${queueHours}h queue). Net expected benefit is +$${Math.round(netDecisionValue).toLocaleString()} USD.`;

  if (!isSafeDraft) {
    executiveSignal = 'DRAFT VIOLATION RISK - REROUTE RECOMMENDED';
    xaiReason = `Vessel draft (${vesselDraft}m) exceeds ${destinationPort} max draft limit (${portMaxDraft}m). Reroute to Dhamra (18.0m) or reduce cargo parcel size.`;
  } else if (netDecisionValue <= 0) {
    executiveSignal = 'FIX IMMEDIATELY (SPOT CHARTER)';
    xaiReason = `Demurrage cost risk ($${Math.round(demurrageCost).toLocaleString()}) outweighs expected rate drop savings ($${Math.round(potentialSavings).toLocaleString()}). Charter vessel today on spot rate.`;
  }

  return {
    ndv: netDecisionValue,
    netDecisionValue,
    freightSavings: potentialSavings,
    potentialFreightSavings: potentialSavings,
    demurrageLoss: demurrageCost,
    demurrageCost,
    executiveSignal,
    xaiReason,
    selectedVessel,
    vesselDraft,
    portMaxDraft,
    currentSpotRate: spotRate,
    targetForecastRate: forecastRate,
    totalCongestionQueueHours: queueHours,
    liveWaveHeight: 2.4,
    weatherStatus: 'Moderate Swell',
    waitingVesselsCount: 9,
    activeAlerts: MOCK_ALERTS
  };
};

// -------------------------------------------------------------
// API EXPORT METHODS WITH AUTOMATIC FAILOVER
// -------------------------------------------------------------

export const fetchDashboard = async () => {
  try {
    const response = await api.get('/dashboard');
    setBackendStatus(true);
    return response.data;
  } catch (err) {
    console.warn('Backend unavailable (/api/dashboard), serving offline fallback mock data.');
    setBackendStatus(false);
    return calculateMockOptimization({});
  }
};

export const postForecast = async (requestData = {}) => {
  try {
    const response = await api.post('/forecast', requestData);
    setBackendStatus(true);
    return response.data;
  } catch (err) {
    console.warn('Backend unavailable (/api/forecast), serving offline fallback mock forecast.');
    setBackendStatus(false);
    const days = requestData.forecastDays || 15;
    const drop = days === 7 ? 0.95 : days === 15 ? 2.22 : 3.80;
    const currentSpotRate = 18.50;
    const forecastSpotRate = +(currentSpotRate - drop).toFixed(2);
    const rateDelta = +(currentSpotRate - forecastSpotRate).toFixed(2);
    const percentageChange = +((rateDelta / currentSpotRate) * 100).toFixed(1);

    const trend = [];
    const step = drop / days;
    for (let d = 1; d <= days; d += Math.max(1, Math.floor(days / 6))) {
      trend.push({
        label: `Day +${d}`,
        value: +(currentSpotRate - (step * d)).toFixed(2)
      });
    }

    return {
      currentSpotRate,
      forecastSpotRate,
      rateDelta,
      percentageChange,
      modelUsed: 'XGBoost4J Regression (Time-Series)',
      confidenceScore: 94.2,
      forecastTrend: trend
    };
  }
};

export const fetchHistoricalRates = async () => {
  try {
    const response = await api.get('/forecast/history');
    setBackendStatus(true);
    return response.data;
  } catch (err) {
    console.warn('Backend unavailable (/api/forecast/history), serving offline fallback.');
    setBackendStatus(false);
    return MOCK_HISTORICAL_RATES;
  }
};

export const postOptimization = async (requestData) => {
  try {
    const response = await api.post('/optimization', requestData);
    setBackendStatus(true);
    return response.data;
  } catch (err) {
    console.warn('Backend unavailable (/api/optimization), executing local solver mock.');
    setBackendStatus(false);
    return calculateMockOptimization(requestData || {});
  }
};

export const fetchPorts = async () => {
  try {
    const response = await api.get('/ports');
    setBackendStatus(true);
    return response.data;
  } catch (err) {
    console.warn('Backend unavailable (/api/ports), serving offline ports catalog.');
    setBackendStatus(false);
    return MOCK_PORTS;
  }
};

export const fetchMarketFleet = async () => {
  try {
    const response = await api.get('/market/fleet');
    setBackendStatus(true);
    return response.data;
  } catch (err) {
    console.warn('Backend unavailable (/api/market/fleet), serving offline vessel fleet.');
    setBackendStatus(false);
    return MOCK_FLEET;
  }
};

export const fetchMarketCongestion = async () => {
  try {
    const response = await api.get('/market/congestion');
    setBackendStatus(true);
    return response.data;
  } catch (err) {
    console.warn('Backend unavailable (/api/market/congestion), serving offline congestion data.');
    setBackendStatus(false);
    return MOCK_CONGESTION;
  }
};

export const fetchWeather = async (portName = 'Paradip Port', vesselDraft = 16.5) => {
  try {
    const response = await api.get(`/weather?portName=${encodeURIComponent(portName)}&vesselDraft=${vesselDraft}`);
    setBackendStatus(true);
    return response.data;
  } catch (err) {
    console.warn('Backend unavailable (/api/weather), serving offline marine telemetry.');
    setBackendStatus(false);
    const queueHoursMap = {
      'Paradip Port': 25.7,
      'Visakhapatnam Port': 18.2,
      'Dhamra Port': 14.5,
      'Haldia Port': 32.0,
      'Gopalpur Port': 12.0
    };
    const totalHours = queueHoursMap[portName] || 20.0;
    const baseQueue = Math.round(totalHours * 0.7 * 10) / 10;
    const tidalDelay = Math.round((totalHours - baseQueue) * 10) / 10;

    return {
      portName,
      waveHeight: 2.4,
      weatherStatus: 'Moderate Swell',
      weatherMultiplier: 1.4,
      baseQueueHours: baseQueue,
      tidalDelayHours: tidalDelay,
      totalAnchorageQueueHours: totalHours,
      waitingVessels: Math.round(totalHours / 2.8)
    };
  }
};

export const fetchAlerts = async () => {
  try {
    const response = await api.get('/alerts');
    setBackendStatus(true);
    return response.data;
  } catch (err) {
    console.warn('Backend unavailable (/api/alerts), serving offline operational alerts.');
    setBackendStatus(false);
    return MOCK_ALERTS;
  }
};

export default api;
