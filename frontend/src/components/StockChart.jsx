import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Line,
  ComposedChart
} from 'recharts';

const API_BASE = import.meta.env.DEV ? 'http://127.0.0.1:8000' : '';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ 
        backgroundColor: '#161b26', 
        border: '1px solid #2d3748', 
        padding: '12px', 
        borderRadius: '8px',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)'
      }}>
        <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '4px' }}>{label}</p>
        <p style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc' }}>
          ${payload[0].value.toLocaleString()}
        </p>
        {payload[1] && (
          <p style={{ fontSize: '0.75rem', color: '#3b82f6', marginTop: '4px' }}>
            MA7: ${payload[1].value.toLocaleString()}
          </p>
        )}
      </div>
    );
  }
  return null;
};

const StockChart = ({ symbol }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [dataRes, predictRes] = await Promise.all([
          axios.get(`${API_BASE}/data/${symbol}`),
          axios.get(`${API_BASE}/predict/${symbol}`)
        ]);

        const history = dataRes.data;
        const predictions = predictRes.data.predictions;

        // Combine data
        const combined = history.map(item => ({
          name: item.DATE,
          price: item.CLOSE,
          ma7: item.MA_7,
          isPrediction: false
        }));

        // Add predictions
        const lastDate = new Date(history[history.length - 1].DATE);
        predictions.forEach((p, i) => {
          const nextDate = new Date(lastDate);
          nextDate.setDate(nextDate.getDate() + i + 1);
          combined.push({
            name: nextDate.toISOString().split('T')[0],
            prediction: p,
            isPrediction: true
          });
        });

        setData(combined);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching chart data", error);
        setLoading(false);
      }
    };

    if (symbol) fetchData();
  }, [symbol]);

  if (loading) return <div style={{ height: '350px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Loading Chart...</div>;

  return (
    <div style={{ width: '100%', height: 350 }}>
      <ResponsiveContainer>
        <ComposedChart data={data}>
          <defs>
            <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#2d3748" vertical={false} />
          <XAxis 
            dataKey="name" 
            stroke="#94a3b8" 
            fontSize={12} 
            tickLine={false} 
            axisLine={false}
            minTickGap={30}
          />
          <YAxis 
            stroke="#94a3b8" 
            fontSize={12} 
            tickLine={false} 
            axisLine={false} 
            tickFormatter={(val) => `$${val}`}
            domain={['auto', 'auto']}
          />
          <Tooltip content={<CustomTooltip />} />
          
          {/* Historical Data */}
          <Area 
            type="monotone" 
            dataKey="price" 
            stroke="#3b82f6" 
            strokeWidth={3}
            fillOpacity={1} 
            fill="url(#colorPrice)" 
          />
          
          {/* MA7 Overlay */}
          <Line 
            type="monotone" 
            dataKey="ma7" 
            stroke="#10b981" 
            strokeWidth={2} 
            dot={false} 
            strokeDasharray="5 5"
          />

          {/* Predictions */}
          <Line 
            type="monotone" 
            dataKey="prediction" 
            stroke="#f59e0b" 
            strokeWidth={3} 
            strokeDasharray="5 5" 
            dot={{ r: 4, fill: '#f59e0b', strokeWidth: 0 }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};

export default StockChart;
