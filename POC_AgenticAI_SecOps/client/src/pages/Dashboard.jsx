import UnifiedChat from "./UnifiedChat";

function Dashboard() {

  return (
    <div className="h-[100dvh] w-[100dvw] overflow-hidden">
      <div className="w-full h-[100dvh] overflow-auto flex">
        <div className="w-full md:flex-1 bg-black p-4 overflow-auto z-50">
          <UnifiedChat />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
