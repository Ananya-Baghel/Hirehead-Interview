import { NextRequest } from "next/server";
export async function POST(req: NextRequest) {
  const r = await fetch(`${process.env.BACKEND_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: await req.text()
  });
  return new Response(await r.text(), { status: r.status, headers: { "Content-Type": "application/json" }});
}
