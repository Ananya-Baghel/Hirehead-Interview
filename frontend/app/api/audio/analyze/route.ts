export async function POST(req: Request) {
  const r = await fetch(`${process.env.BACKEND_URL}/audio/analyze`, {
    method: "POST",
    body: await req.formData()
  });
  return new Response(await r.text(), { status: r.status, headers: { "Content-Type": "application/json" }});
}
