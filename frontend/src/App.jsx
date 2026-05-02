import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  TrendingUp, 
  TrendingDown, 
  LayoutDashboard, 
  PieChart, 
  Activity, 
  ChevronRight,
  Target
} from 'lucide-react';

// Components
import StockChart from './components/StockChart';
import PredictionPanel from './components/PredictionPanel';

const API_BASE = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://127.0.0.1:8000' : '');

function App() {
  const [symbols, setSymbols] = useState([]);
  const [selectedSymbol, setSelectedSymbol] = useState('');
  const [topPicks, setTopPicks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initData = async () => {
      try {
        const [symRes, picksRes] = await Promise.all([
          axios.get(`${API_BASE}/companies`),
          axios.get(`${API_BASE}/top-picks`)
        ]);
        setSymbols(symRes.data);
        setTopPicks(picksRes.data);
        if (symRes.data.length > 0) setSelectedSymbol(symRes.data[0]);
        setLoading(false);
      } catch (error) {
        console.error("Failed to fetch initial data", error);
        setLoading(false);
      }
    };
    initData();
  }, []);

  if (loading) return <div style={{ padding: '40px', textAlign: 'center' }}>Loading Intelligence...</div>;

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '40px' }}>
          <div style={{ backgroundColor: 'var(--accent-blue)', padding: '8px', borderRadius: '8px' }}>
            <Activity size={24} color="white" />
          </div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 800 }}>STOCK INTEL</h2>
        </div>

        <nav style={{ flex: 1 }}>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '16px', fontWeight: 600 }}>MARKET SYMBOLS</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {symbols.map(sym => (
              <button
                key={sym}
                onClick={() => setSelectedSymbol(sym)}
                className="hover-effect"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  borderRadius: '8px',
                  border: '1px solid transparent',
                  background: selectedSymbol === sym ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
                  borderColor: selectedSymbol === sym ? 'var(--accent-blue)' : 'transparent',
                  color: selectedSymbol === sym ? 'var(--text-primary)' : 'var(--text-secondary)',
                  cursor: 'pointer',
                  textAlign: 'left',
                  width: '100%'
                }}
              >
                <span style={{ fontWeight: 600 }}>{sym}</span>
                <ChevronRight size={16} style={{ opacity: selectedSymbol === sym ? 1 : 0 }} />
              </button>
            ))}
          </div>
        </nav>

        <div className="card" style={{ marginTop: 'auto', padding: '16px', marginBottom: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <Target size={16} className="text-green" />
            <span style={{ fontSize: '0.75rem', fontWeight: 700 }}>SYSTEM STATUS</span>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            Connected to Supabase Cloud
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
          <div>
            <h1 className="text-xl">{selectedSymbol} Overview</h1>
            <p style={{ color: 'var(--text-secondary)' }}>Market analysis and ML forecasting for {selectedSymbol}</p>
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            {/* Quick stats could go here */}
          </div>
        </header>

        {/* Top Picks Section */}
        <section style={{ marginBottom: '40px' }}>
          <h2 className="card-title">Top Smart Picks</h2>
          <div className="grid-3">
            {topPicks.map(pick => (
              <div key={pick.symbol} className="card hover-effect" style={{ marginBottom: 0 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <span style={{ fontWeight: 800, fontSize: '1.125rem' }}>{pick.symbol}</span>
                  <span className={`badge ${pick.trend === 'UP' ? 'badge-up' : 'badge-down'}`}>
                    {pick.trend}
                  </span>
                </div>
                <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>
                  {pick.score}
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginLeft: '8px', fontWeight: 400 }}>SMART SCORE</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Main Charts Area */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
          <div className="card" style={{ minHeight: '450px' }}>
            <h2 className="card-title">Historical Price & 7-Day Forecast</h2>
            <StockChart symbol={selectedSymbol} />
          </div>
          
          <div className="card">
            <h2 className="card-title">Intelligence Panel</h2>
            <PredictionPanel symbol={selectedSymbol} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
