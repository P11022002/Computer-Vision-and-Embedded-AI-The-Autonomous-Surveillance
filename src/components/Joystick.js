import React from "react";

function Joystick({ onControl }) {
  return (
    <div className="rounded-3xl bg-slate-900 p-5 shadow-xl">
      <h2 className="text-xl font-semibold mb-4">Control Panel</h2>
      <div className="grid gap-3 sm:grid-cols-3">
        {[
          ["forward", "Forward"],
          ["left", "Left"],
          ["right", "Right"],
          ["backward", "Backward"],
          ["stop", "Stop"],
          ["autonomous", "Autonomous"],
        ].map(([action, label]) => (
          <button
            key={action}
            type="button"
            onClick={() => onControl(action)}
            className="rounded-2xl bg-slate-700 px-4 py-3 text-sm font-semibold transition hover:bg-slate-600"
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default Joystick;
