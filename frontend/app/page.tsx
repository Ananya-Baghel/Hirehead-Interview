"use client";
import { useRef, useState } from "react";

export default function Page() {
  const [session, setSession] = useState<any>(null);
  const [question, setQuestion] = useState<string>("");
  const [answer, setAnswer] = useState<string>("");
  const [analysis, setAnalysis] = useState<any>(null);
  const [culture, setCulture] = useState<any>(null);
  const [neg, setNeg] = useState<any>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const [wsData, setWsData] = useState<any>(null);

  const start = async () => {
    const res = await fetch("/api/interview/start", {
      method: "POST",
      body: JSON.stringify({ industry: "software", personas: ["hr","tech","manager"], difficulty: "easy", stressLevel: 1 })
    });
    const data = await res.json();
    setSession({ id: data.sessionId, stress: data.stress });
    setQuestion(data.question);
  };

  const nextQ = async () => {
    const res = await fetch("/api/interview/next", {
      method: "POST",
      body: JSON.stringify({ sessionId: session.id, lastAnswer: answer, durationSeconds: 45 })
    });
    const data = await res.json();
    setQuestion(data.question);
    setSession({ ...session, stress: data.stress });
    setAnswer("");
  };

  const analyze = async () => {
    const res = await fetch("/api/interview/analyze", { method: "POST", body: JSON.stringify({ transcript: answer, durationSeconds: 45 }) });
    setAnalysis(await res.json());
  };

  const startWS = () => {
    if (wsRef.current) wsRef.current.close();
    const ws = new WebSocket(process.env.NEXT_PUBLIC_WS || (location.origin.replace(/^http/,"ws") + "/ws/stream").replace("/api",""));
    ws.onmessage = (e) => setWsData(JSON.parse(e.data));
    wsRef.current = ws;
  };
  const sendWS = (text: string) => wsRef.current?.send(JSON.stringify({ text }));

  const cultureFit = async () => {
    const res = await fetch("/api/culturefit/score", { method: "POST", body: JSON.stringify({ transcript: answer })});
    setCulture(await res.json());
  };

  const startNeg = async () => {
    const res = await fetch("/api/negotiation/start", { method: "POST", body: JSON.stringify({ role: "Software Engineer", candidateAnchor: 24.0 }) });
    setNeg(await res.json());
  };
  const respondNeg = async (msg: string) => {
    const res = await fetch("/api/negotiation/respond", { method: "POST", body: JSON.stringify({ sessionId: neg.sessionId, candidateMessage: msg }) });
    setNeg({ ...neg, last: await res.json() });
  };

  return (
    <main className="p-6 max-w-3xl mx-auto flex flex-col gap-3">
      <h1 className="text-2xl font-bold">Interview Bot — Full</h1>

      <button className="border px-3 py-2 rounded" onClick={start}>Start Interview</button>
      {question && <div className="p-3 border rounded bg-gray-50">Q: {question}</div>}

      <textarea className="border rounded p-2 min-h-[120px]" placeholder="Your answer…" value={answer} onChange={e=>{ setAnswer(e.target.value); if (wsRef.current) sendWS(e.target.value); }} />

      <div className="flex gap-2">
        <button className="border px-3 py-2 rounded" onClick={analyze}>Analyze</button>
        <button className="border px-3 py-2 rounded" onClick={nextQ}>Next Question</button>
        <button className="border px-3 py-2 rounded" onClick={cultureFit}>Culture Fit</button>
        <button className="border px-3 py-2 rounded" onClick={startWS}>Start Live Monitor</button>
      </div>

      {analysis && <pre className="bg-gray-100 p-3 rounded text-sm overflow-auto">{JSON.stringify(analysis,null,2)}</pre>}
      {wsData && <pre className="bg-gray-100 p-3 rounded text-sm overflow-auto">Live: {JSON.stringify(wsData,null,2)}</pre>}
      {culture && <pre className="bg-gray-100 p-3 rounded text-sm overflow-auto">{JSON.stringify(culture,null,2)}</pre>}

      <h2 className="font-semibold mt-4">Negotiation</h2>
      <div className="flex gap-2">
        <button className="border px-3 py-2 rounded" onClick={startNeg}>Start Negotiation</button>
        {neg?.sessionId && <button className="border px-3 py-2 rounded" onClick={()=>respondNeg("Can you do 26 LPA and WFH 3 days?")}>Respond</button>}
      </div>
      {neg && <pre className="bg-gray-100 p-3 rounded text-sm overflow-auto">{JSON.stringify(neg,null,2)}</pre>}
    </main>
  );
}
