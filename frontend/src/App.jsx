import { useState } from "react";
import SearchPage from "./pages/SearchPage";
import AdminPage from "./pages/AdminPage";

export default function App() {
  const [tab, setTab] = useState("search");

  return (
    <div>
      <nav>
        <button onClick={() => setTab("search")}>Search</button>
        <button onClick={() => setTab("admin")}>Admin</button>
      </nav>
      {tab === "search" ? <SearchPage /> : <AdminPage />}
    </div>
  );
}
