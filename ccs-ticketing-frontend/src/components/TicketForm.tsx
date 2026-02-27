"use client";

import { useState } from 'react';

// 1. Define strict Type Signature
type InfrastructureData = {
  [floor: string]: {
    [lab: string]: string[];
  };
};

// 2. Mock Data
const ccsInfrastructure: InfrastructureData = {
  "Floor 2": {
    "Lab 201 (Mac Lab)": ["iMac-01", "iMac-02", "iMac-03"],
    "Lab 202 (Networking)": ["Cisco-PC-01", "Cisco-PC-02"],
  },
  "Floor 3": {
    "Lab 305 (Programming)": ["Dell-Prog-01", "Dell-Prog-02", "Dell-Prog-03"],
  }
};

export default function TicketForm() {
  // --- STATE MANAGEMENT ---
  const [selectedFloor, setSelectedFloor] = useState<string>('');
  const [selectedLab, setSelectedLab] = useState<string>('');
  const [selectedPC, setSelectedPC] = useState<string>('');
  const [issueDescription, setIssueDescription] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [feedbackMessage, setFeedbackMessage] = useState<string>('');

  // --- HANDLERS ---
  const handleFloorChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedFloor(e.target.value);
    setSelectedLab('');
    setSelectedPC('');
  };

  const handleLabChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedLab(e.target.value);
    setSelectedPC('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setFeedbackMessage('Sending ticket to AI Triage...');

    const payload = {
      location: `${selectedFloor} - ${selectedLab} - ${selectedPC}`,
      description: issueDescription
    };

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tickets`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error(`Server responded with status: ${response.status}`);

      const data = await response.json();
      setFeedbackMessage(`Success! Ticket ID #${data.id} created. AI Priority Score: ${data.priority_score}/10.`);
      
      setSelectedFloor('');
      setSelectedLab('');
      setSelectedPC('');
      setIssueDescription('');

    } catch (error) {
      console.error("Submission error:", error);
      setFeedbackMessage('Failed to submit. Ensure backend is running.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // --- DYNAMIC OPTIONS ---
  const floors = Object.keys(ccsInfrastructure);
  const labs = selectedFloor ? Object.keys(ccsInfrastructure[selectedFloor]) : [];
  const pcs = selectedFloor && selectedLab ? ccsInfrastructure[selectedFloor][selectedLab] || [] : [];

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Submit IT Incident</h2>

      {feedbackMessage && (
        <div className={`mb-4 p-3 rounded-md text-sm ${feedbackMessage.includes('Success') ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>
          {feedbackMessage}
        </div>
      )}

      {/* Floor Selection - Added text-gray-900 and bg-white */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">CCS Floor</label>
        <select 
          value={selectedFloor} 
          onChange={handleFloorChange} 
          className="mt-1 block w-full p-2 border border-gray-300 rounded-md text-gray-900 bg-white focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Select Floor</option>
          {floors.map(floor => <option key={floor} value={floor}>{floor}</option>)}
        </select>
      </div>

      {/* Lab Selection - Added text-gray-900 and bg-white */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Computer Lab</label>
        <select 
          value={selectedLab} 
          onChange={handleLabChange} 
          disabled={!selectedFloor} 
          className="mt-1 block w-full p-2 border border-gray-300 rounded-md text-gray-900 bg-white disabled:bg-gray-100 disabled:text-gray-500 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Select Lab</option>
          {labs.map(lab => <option key={lab} value={lab}>{lab}</option>)}
        </select>
      </div>

      {/* PC Selection - Added text-gray-900 and bg-white */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Specific PC / Asset</label>
        <select 
          value={selectedPC} 
          onChange={(e) => setSelectedPC(e.target.value)} 
          disabled={!selectedLab} 
          className="mt-1 block w-full p-2 border border-gray-300 rounded-md text-gray-900 bg-white disabled:bg-gray-100 disabled:text-gray-500 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Select PC</option>
          {pcs.map((pc: string) => <option key={pc} value={pc}>{pc}</option>)}
        </select>
      </div>

      {/* Issue Description - Added text-gray-900 and bg-white */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Describe the Issue</label>
        <textarea 
          value={issueDescription} 
          onChange={(e) => setIssueDescription(e.target.value)} 
          placeholder="E.g., The mouse is broken and I have a mid-term exam right now!"
          className="mt-1 block w-full p-2 border border-gray-300 rounded-md h-24 text-gray-900 bg-white focus:ring-blue-500 focus:border-blue-500 placeholder-gray-400"
          required
        />
      </div>

      <button 
        type="submit" 
        disabled={isSubmitting || !selectedPC || !issueDescription} 
        className="w-full bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {isSubmitting ? 'AI is Processing...' : 'Submit Ticket to AI Triage'}
      </button>
    </form>
  );
}