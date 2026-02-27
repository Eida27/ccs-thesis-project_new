"use client";

import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// --- TYPE DEFINITIONS ---
type Ticket = {
  id: number;
  location: string;
  ai_category: string;
  priority_score: number;
  status: string;
};

type ForecastData = {
  day: string;
  predicted_tickets: number;
};

export default function AdminDashboard() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [forecast, setForecast] = useState<ForecastData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // --- DATA FETCHING (On Component Mount) ---
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch both endpoints simultaneously for performance
        const [ticketRes, forecastRes] = await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tickets`),
          fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/forecast`)
        ]);

        const ticketData = await ticketRes.json();
        const forecastData = await forecastRes.json();

        setTickets(ticketData);

        // Map the raw ARIMA integers into a format the Chart library understands
        const formattedForecast = forecastData.data.forecast.map((val: number, index: number) => ({
          day: `Day ${index + 1}`,
          predicted_tickets: val
        }));
        
        setForecast(formattedForecast);
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (isLoading) return <div className="p-10 text-center text-xl font-bold">Loading Predictive Models...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-extrabold text-gray-900 mb-8">CCS ITSM Command Center</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* LEFT COLUMN: ARIMA Forecast Chart */}
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-xl font-bold mb-4 text-gray-800">7-Day Demand Forecast (ARIMA)</h2>
          <p className="text-sm text-gray-500 mb-6">Predictive ticket volume based on historical archival records.</p>
          
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={forecast}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="predicted_tickets" stroke="#2563eb" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* RIGHT COLUMN: AI-Prioritized Ticket Queue */}
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Live Incident Queue</h2>
          <p className="text-sm text-gray-500 mb-6">Automatically sorted by AI Sentiment & Priority Score.</p>
          
          <div className="overflow-y-auto h-72 pr-2">
            {tickets.length === 0 ? (
              <p className="text-gray-500 italic">No open tickets. The infrastructure is stable.</p>
            ) : (
              tickets.map((ticket) => (
                <div key={ticket.id} className="mb-3 p-4 border-l-4 border-blue-600 bg-gray-50 rounded-r-md flex justify-between items-center">
                  <div>
                    <span className="text-xs font-bold text-gray-500 uppercase">{ticket.ai_category}</span>
                    <p className="font-semibold text-gray-800">{ticket.location}</p>
                  </div>
                  <div className="text-right">
                    <span className="inline-block bg-red-100 text-red-800 text-sm px-2 py-1 rounded-full font-bold">
                      Priority: {ticket.priority_score}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

      </div>
    </div>
  );
}