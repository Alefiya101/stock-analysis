import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  ShieldCheck, 
  Zap, 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  Info,
  HelpCircle
} from 'lucide-react';

const API_BASE = '';

const PredictionPanel = ({ symbol }) => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPrediction = async () => {
      setLoading(true);
      try {
        const res = await axios.get(`${API_BASE}/predict/${symbol}`);
        setPrediction(res.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching prediction", error);
        setLoading(false);
      }
    };
    if (symbol) fetchPrediction();
  }, [symbol]);

  if (loading) return <div style={{ height: '350px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Analyzing Intelligence...</div>;
  if (!prediction) return null;

  // Convert explanation object to array for mapping
  const drivers = Object.entries(prediction.explanation || {}).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Trend Badge */}
      <div style={{ 
        padding: '24px', 
        borderRadius: '12px', 
        backgroundColor: prediction.trend === 'UP' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
        border: `1px solid ${prediction.trend === 'UP' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)'}`,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '12px'
      }}>
        {prediction.trend === 'UP' ? (
          <TrendingUp size={48} className="text-green" />
        ) : (
          <TrendingDown size={48} className="text-red" />
        )}
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-secondary)', marginBottom: '4px' }}>7-DAY OUTLOOK</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: prediction.trend === 'UP' ? 'var(--accent-green)' : 'var(--accent-red)' }}>
            MARKET {prediction.trend}
          </div>
        </div>
      </div>

      {/* SHAP Key Drivers Section */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <HelpCircle size={16} color="var(--accent-blue)" />
          <h2 className="card-title" style={{ margin: 0 }}>Why this prediction?</h2>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {drivers.map(([label, impact]) => (
            <div key={label} style={{ fontSize: '0.8125rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span style={{ color: 'var(--text-secondary)' }}>{label}</span>
                <span style={{ fontWeight: 700, color: impact >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}>
                  {impact >= 0 ? '+' : ''}{impact}
                </span>
              </div>
              {/* Simple Bar Visualization */}
              <div style={{ height: '4px', width: '100%', backgroundColor: 'var(--bg-color)', borderRadius: '2px', overflow: 'hidden' }}>
                <div style={{ 
                  height: '100%', 
                  width: `${Math.min(Math.abs(impact) * 2, 100)}%`, 
                  backgroundColor: impact >= 0 ? 'var(--accent-green)' : 'var(--accent-red)',
                  marginLeft: impact < 0 ? 'auto' : '0' 
                }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Metrics List */}
      <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldCheck size={18} color="var(--accent-blue)" />
            <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>Model Confidence</span>
          </div>
          <span className="badge" style={{ backgroundColor: 'var(--bg-color)', border: '1px solid var(--border-color)' }}>
            {prediction.confidence}
          </span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <BarChart3 size={18} color="var(--text-secondary)" />
            <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>R² Accuracy</span>
          </div>
          <span style={{ fontSize: '0.875rem', fontWeight: 700 }}>{prediction.r2_score}</span>
        </div>
      </div>
    </div>
  );
};

export default PredictionPanel;
