import { NextRequest } from "next/server";
export async function POST(req: NextRequest) {
  const body = await req.json();
  const r = await fetch(`${process.env.BACKEND_URL}/interview/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return new Response(await r.text(), { status: r.status, headers: { "Content-Type": "application/json" }});
}
