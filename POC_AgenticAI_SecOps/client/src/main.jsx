import "./index.css";

import App from "./App.jsx";
import { createRoot } from "react-dom/client";
import { HeroUIProvider } from "@heroui/react";

createRoot(document.getElementById("root")).render(
  <HeroUIProvider>
    <main className="dark w-[100dvw] h-[100dvh] light text-foreground bg-background">
      <App />
    </main>
  </HeroUIProvider>
);
