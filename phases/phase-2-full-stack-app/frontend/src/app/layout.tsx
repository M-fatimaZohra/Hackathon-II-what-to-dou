import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Oswald } from "next/font/google";
import { Satisfy } from "next/font/google";
import "./globals.css";
import Navigation from "@/components/Navigation";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

const oswald = Oswald({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

const satisfy = Satisfy({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

export const metadata: Metadata = {
  title: "AI Native Todo App",
  description: "A modern todo application with AI capabilities",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.className} antialiased bg-[#FFFBED]`}
        style={inter.style}
      >
        <Navigation />
        <main className="pt-16">
          {children}
        </main>
      </body>
    </html>
  );
}
