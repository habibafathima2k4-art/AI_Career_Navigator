import { Route, Routes } from "react-router-dom";
import AppShell from "./layouts/AppShell";
import AdminPage from "./pages/AdminPage";
import AssessmentPage from "./pages/AssessmentPage";
import CareerDetailPage from "./pages/CareerDetailPage";
import HistoryPage from "./pages/HistoryPage";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ResultsPage from "./pages/ResultsPage";

export default function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/assessment" element={<AssessmentPage />} />
        <Route path="/careers/:careerId" element={<CareerDetailPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/results/:assessmentId" element={<ResultsPage />} />
      </Route>
    </Routes>
  );
}
