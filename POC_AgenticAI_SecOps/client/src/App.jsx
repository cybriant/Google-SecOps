import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./app.css";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <div className="">
      <Router>
        <Routes>
          <Route path="/" element={<Dashboard />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
