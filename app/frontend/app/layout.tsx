import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Routewise | Weather-aware truck routing",
  description: "Compare truck routes using ETA-aware weather risk intelligence.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
