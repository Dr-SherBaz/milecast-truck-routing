import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Milecast — Weather-aware truck routing",
  description: "Choose the safest freight corridor by weather risk, load weight, and travel time.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
