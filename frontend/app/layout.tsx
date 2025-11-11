export const metadata = {
  title: "Interview Bot",
  description: "AI Interview Assistant",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body
        style={{
          fontFamily: "sans-serif",
          margin: 0,
          padding: 0,
          background: "#f9fafb",
        }}
      >
        {children}
      </body>
    </html>
  );
}
