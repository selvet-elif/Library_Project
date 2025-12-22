import { useState } from "react";
import { Toaster } from "react-hot-toast";
import { Dashboard } from "./components/Dashboard";
import { AddBookForm } from "./components/AddBookForm";

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleBookAdded = () => {
    // Trigger refresh by changing key
    setRefreshKey((k) => k + 1);
  };

  return (
    <>
      <Toaster position="top-right" />
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <AddBookForm onBookAdded={handleBookAdded} />
          <Dashboard key={refreshKey} />
        </div>
      </div>
    </>
  );
}

export default App;
