"use client";
import { useState } from "react";

export default function Home() {
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    const res = await fetch("/api/interview/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript: answer, durationSeconds: 45 }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <main className="p-10 max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-10 bg-gradient-to-r from-purple-500 to-indigo-600 bg-clip-text text-transparent">
        Interview Bot — Full
      </h1>

      <div className="bg-white shadow-xl rounded-2xl p-6 space-y-6">
        <textarea
          className="w-full border rounded-lg p-4 h-40 focus:ring-2 focus:ring-indigo-400 outline-none"
          placeholder="Type or paste your interview answer..."
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
        />

        <button
          onClick={handleAnalyze}
          disabled={loading || !answer}
          className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold shadow hover:scale-105 transition"
        >
          {loading ? "Analyzing..." : "Analyze Answer"}
        </button>

        {result && (
          <div className="border-t pt-6 space-y-4">
            <h2 className="text-2xl font-semibold text-indigo-700">
              Analysis Result
            </h2>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-indigo-50 p-4 rounded-lg shadow-sm">
                <h3 className="font-semibold text-indigo-800">Sentiment</h3>
                <p className="text-gray-700">
                  {result.sentiment?.label} ({Math.round(result.sentiment?.confidence * 100)}%)
                </p>
              </div>

              <div className="bg-purple-50 p-4 rounded-lg shadow-sm">
                <h3 className="font-semibold text-purple-800">Confidence</h3>
                <p className="text-gray-700">
                  {result.confidence?.label} ({Math.round(result.confidence?.confidence * 100)}%)
                </p>
              </div>
            </div>

            <div className="bg-green-50 p-4 rounded-lg shadow-sm">
              <h3 className="font-semibold text-green-700 mb-2">Suggestions</h3>
              <ul className="list-disc list-inside text-gray-700">
                {result.suggestions?.tips?.map((tip: string, i: number) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>
            </div>

            <div className="bg-yellow-50 p-4 rounded-lg shadow-sm">
              <h3 className="font-semibold text-yellow-700 mb-2">Next Questions</h3>
              <ul className="list-disc list-inside text-gray-700">
                {result.suggestions?.next_questions?.map((q: string, i: number) => (
                  <li key={i}>{q}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
