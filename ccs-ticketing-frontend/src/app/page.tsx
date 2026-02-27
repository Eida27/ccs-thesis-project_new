import TicketForm from "../components/TicketForm";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        
        {/* Header Section */}
        <div className="text-center mb-12">
          <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            CCS IT Service Management
          </h1>
          <p className="mt-3 max-w-2xl mx-auto text-xl text-gray-500 sm:mt-4">
            Predictive Resource Allocation via Sentiment-Based Incident Ticketing
          </p>
        </div>

        {/* Form Component Injection */}
        <TicketForm />
        
      </div>
    </main>
  );
}