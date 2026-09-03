import "./globals.css";
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Planvesto',
  description: 'Planvesto — Financial Planning and Decision Platform'
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body style={{ margin: 0, padding: 0 }}>{children}</body>
    </html>
  );
}
