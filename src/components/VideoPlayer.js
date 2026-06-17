import React from "react";

function VideoPlayer() {
  return (
    <div className="flex h-full min-h-[420px] flex-col gap-3">
      <h2 className="text-xl font-semibold">Live Video Feed</h2>
      <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-slate-900 p-4">
        <div className="h-[360px] w-full bg-slate-800 text-slate-500 flex items-center justify-center">
          <p>Video stream placeholder</p>
        </div>
      </div>
    </div>
  );
}

export default VideoPlayer;
