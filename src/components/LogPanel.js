import React from "react";

function LogPanel({ logs, connectionStatus }) {
  return (
    <div className="rounded-3xl bg-slate-900 p-5 shadow-xl">
      <div className="mb-4 flex items-center justify-between gap-4">
        <h2 className="text-xl font-semibold">Threat & Connection Log</h2>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-300">
          {connectionStatus}
        </span>
      </div>
      <div className="max-h-[340px] overflow-y-auto rounded-3xl bg-slate-950 p-4 text-sm leading-6 text-slate-300">
        {logs.length === 0 ? (
          <p className="text-slate-500">No messages yet.</p>
        ) : (
          logs.map((entry, index) => (
            <div key={index} className="mb-3 border-b border-slate-800 pb-3 last:border-none last:pb-0">
              <p>{entry}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default LogPanel;
