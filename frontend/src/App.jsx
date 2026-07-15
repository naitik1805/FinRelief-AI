import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import FinancialHealth from "./pages/FinancialHealth";
import SettlementPredictor from "./pages/SettlementPredictor";
import NegotiationEmail from "./pages/NegotiationEmail";
import KnowYourRights from "./pages/KnowYourRights";
import History from "./pages/History";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/financial-health" element={<FinancialHealth />} />
          <Route path="/settlement-predictor" element={<SettlementPredictor />} />
          <Route path="/negotiation-email" element={<NegotiationEmail />} />
          <Route path="/know-your-rights" element={<KnowYourRights />} />
          <Route path="/history" element={<History />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
